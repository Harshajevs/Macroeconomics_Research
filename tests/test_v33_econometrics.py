"""Regression behavioural tests for the v3.3 post-results correction."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.stats import f as f_dist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import estimate_baseline as m


def main():
    # June-2013 exposure guard uses the actual maximum lag, not a hard-coded rule.
    for start in ('2013-07', '2013-08', '2013-09'):
        try:
            m.design(q=3, p=3, start=start)
            raise AssertionError(f'June exposure was allowed for start {start}')
        except ValueError:
            pass
    y, X = m.design(q=3, p=3, start='2013-10')
    assert str(y.index.min()) == '2013-10'
    y6, X6 = m.design(q=6, p=6, start='2014-01')
    assert np.isclose(X6.loc[pd.Period('2014-01', 'M'), 'x_l6'],
                      m.D.loc[pd.Period('2013-07', 'M'), 'infl_food_log'])

    # BIC candidates for q=1/p=0..3 use the same maximum lag exposure window.
    covid_counts = []
    for p in range(4):
        _, xx = m.design(q=1, p=p, start='2014-01', covid_lag_horizon=3)
        covid_counts.append(int(xx['covid_affected_window'].sum()))
    assert len(set(covid_counts)) == 1 and covid_counts[0] == 10

    # Core outcome is the operational food-and-fuel-excluded measure.
    yc, Xc = m.design(q=3, p=1, start='2013-10', direction='food_to_core')
    assert np.isclose(yc.loc[pd.Period('2014-01', 'M')], m.D.loc[pd.Period('2014-01', 'M'), 'infl_core_log'])
    assert 'x_l3' in Xc.columns

    # Ljung-Box must pass model_df=p to statsmodels.
    original_lb = m.acorr_ljungbox
    original_bg = m.acorr_breusch_godfrey
    m.acorr_breusch_godfrey = lambda res, nlags: (0.0, 0.5, 0.0, 0.5)
    captured = {}
    def fake_lb(resid, lags, model_df, return_df):
        captured['model_df'] = model_df
        return pd.DataFrame({'lb_pvalue': [0.5]}, index=lags)
    m.acorr_ljungbox = fake_lb
    class FakeRes:
        resid = np.arange(40, dtype=float)
    m.residual_tests(FakeRes(), p=2)
    m.acorr_ljungbox = original_lb
    m.acorr_breusch_godfrey = original_bg
    assert captured['model_df'] == 2

    # BG alone and LB alone must not trigger; both at same horizon must.
    bg_alone = {'BG_p_lag6': .01, 'BG_p_lag12': .40,
                'LB_p_lag6_model_df_p': .20, 'LB_p_lag12_model_df_p': .20}
    lb_alone = {'BG_p_lag6': .20, 'BG_p_lag12': .20,
                'LB_p_lag6_model_df_p': .01, 'LB_p_lag12_model_df_p': .20}
    both_same = {'BG_p_lag6': .01, 'BG_p_lag12': .40,
                 'LB_p_lag6_model_df_p': .02, 'LB_p_lag12_model_df_p': .30}
    both_different = {'BG_p_lag6': .01, 'BG_p_lag12': .40,
                      'LB_p_lag6_model_df_p': .20, 'LB_p_lag12_model_df_p': .01}
    assert not m.fallback_trigger(bg_alone)
    assert not m.fallback_trigger(lb_alone)
    assert m.fallback_trigger(both_same)
    assert not m.fallback_trigger(both_different)

    # F-reference must use F(df_restrictions, df_resid), not repeat chi-square p.
    rr = m.fit_model(y, X)
    hac = rr.get_robustcov_results(cov_type='HAC', maxlags=6, use_correction=True, use_t=False)
    R = m.restriction_matrix(list(X.columns), ['x_l1', 'x_l2', 'x_l3'])
    stats = m.contrast_wald(rr, hac, R)
    expected = f_dist.sf(stats['F'], stats['df'], rr.df_resid)
    assert np.isclose(stats['F_p'], expected)
    assert not np.isclose(stats['F_p'], stats['chi2_p'])

    # BIC must actually select the minimum, with a deterministic p tie-break.
    rows = [{'p': 0, 'BIC': 4.0}, {'p': 1, 'BIC': 2.0},
            {'p': 2, 'BIC': 2.0}, {'p': 3, 'BIC': 3.0}]
    assert m.select_bic_candidate(rows)['p'] == 1

    # Delayed estimand is beta1..min(q,3), not every available q lag.
    y6, X6 = m.design(q=6, p=1, start='2014-01')
    r6 = m.fit_model(y6, X6)
    h6 = r6.get_robustcov_results(cov_type='HAC', maxlags=6, use_correction=True, use_t=False)
    smry6 = m.delayed_sum(r6, h6, q=6)
    expected3 = sum(float(r6.params[f'x_l{i}']) for i in (1,2,3))
    expected6 = sum(float(r6.params[f'x_l{i}']) for i in range(1,7))
    assert np.isclose(smry6['primary_comparable_delayed_sum'], expected3)
    assert np.isclose(smry6['full_distributed_lag_sum'], expected6)

    # The fast bootstrap HAC statistic matches statsmodels' Bartlett HAC Wald.
    y0, X0 = m.design(q=3, p=1, start='2013-10')
    r0 = m.fit_model(y0, X0)
    h0 = r0.get_robustcov_results(cov_type='HAC', maxlags=6, use_correction=True, use_t=False)
    R0 = m.restriction_matrix(list(X0.columns), ['x_l1','x_l2','x_l3'])
    sm_stat = float(h0.wald_test(R0, use_f=False, scalar=True).statistic)
    fast_stat = m.hac_wald_statistic(y0, X0, R0, nlags=6)
    assert np.isclose(sm_stat, fast_stat, atol=1e-9)

    # Partial sup-F only tests the selected food-lag coefficients.
    ps = m.supf_partial_statistic(y0, X0, ['x_l1','x_l2','x_l3'])
    assert np.isfinite(ps) and ps > 0

    print('ALL V3.3 ECONOMETRIC BEHAVIOURAL TESTS PASSED')

if __name__ == '__main__':
    main()
