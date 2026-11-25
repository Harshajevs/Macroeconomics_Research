"""Behavioural tests for the post-results v3.2 econometric implementation."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import estimate_baseline as model


def main():
    # (1) The October q=3/p<=3 window is valid, and all candidate p values
    # use the same outcome dates.
    samples = []
    for p in range(4):
        y, X = model.design(q=3, p=p, start='2013-10')
        samples.append(tuple(y.index))
    assert all(s == samples[0] for s in samples)
    assert str(pd.PeriodIndex(samples[0], freq='M').min()) == '2013-10'

    # (2) Any >3-lag configuration is prevented from starting in Oct 2013.
    try:
        model.design(q=3, p=6, start='2013-10')
        raise AssertionError('June-2013 exposure guard did not reject p=6')
    except ValueError as exc:
        assert '2014-01' in str(exc)

    # (3) At Jan-2014, the sixth lag reaches July 2013, not June 2013.
    y6, X6 = model.design(q=6, p=6, start='2014-01')
    raw = model.D
    jan = pd.Period('2014-01', freq='M')
    assert np.isclose(X6.loc[jan, 'x_l6'], raw.loc[pd.Period('2013-07', freq='M'), 'infl_food_log'])
    assert np.isclose(X6.loc[jan, 'y_l6'], raw.loc[pd.Period('2013-07', freq='M'), 'infl_nonfood_log'])

    # (4) COVID event period and the downstream lag-exposure window extend
    # through Mar-2021 for a six-month lag horizon.
    assert np.isclose(X6.loc[pd.Period('2020-06', freq='M'), 'covid_affected_window'], 1.0)
    assert np.isclose(X6.loc[pd.Period('2021-03', freq='M'), 'covid_affected_window'], 1.0)
    assert np.isclose(X6.loc[pd.Period('2021-04', freq='M'), 'covid_affected_window'], 0.0)
    # The one-lag configuration has an eight-month affected period through Oct-2020,
    # not a singleton tail dummy.
    y1, X1 = model.design(q=1, p=1, start='2014-01')
    assert np.isclose(X1.loc[pd.Period('2020-10', freq='M'), 'covid_affected_window'], 1.0)
    assert np.isclose(X1.loc[pd.Period('2020-11', freq='M'), 'covid_affected_window'], 0.0)

    # (5) Exclusion sensitivity masks outcome rows after full-calendar lags;
    # zero event indicators are removed and the lag at Jan-2022 remains aligned.
    mask = model.COVID_EXCLUSION
    ym, Xm = model.design(q=6, p=6, start='2014-01', mask_months=mask,
                          include_covid_controls=False)
    assert not any('covid_' in c or 'pulse_' in c for c in Xm.columns)
    jan22 = pd.Period('2022-01', freq='M')
    assert jan22 in ym.index
    assert np.isclose(Xm.loc[jan22, 'x_l6'], raw.loc[pd.Period('2021-07', freq='M'), 'infl_food_log'])
    assert not any(pd.Period('2020-03', freq='M') <= d <= pd.Period('2021-12', freq='M') for d in ym.index)

    # (6) Ljung-Box is adjusted for AR degrees of freedom and reports NA if
    # the requested diagnostic lag has no residual degrees of freedom.
    r6 = model.fit_model(y6, X6)
    t6 = model.residual_tests(r6, p=6)
    assert np.isnan(t6['LB_p_lag6_model_df_p'])
    assert np.isfinite(t6['LB_p_lag12_model_df_p'])

    # (7) Synthetic diagnostics exercise the pre-declared fallback trigger.
    synthetic_reject = {'BG_p_lag6': 0.01, 'BG_p_lag12': 0.40,
                        'LB_p_lag6_model_df_p': 0.02, 'LB_p_lag12_model_df_p': 0.30}
    synthetic_no_reject = {'BG_p_lag6': 0.20, 'BG_p_lag12': 0.30,
                           'LB_p_lag6_model_df_p': 0.10, 'LB_p_lag12_model_df_p': 0.20}
    assert model.fallback_trigger(synthetic_reject)
    assert not model.fallback_trigger(synthetic_no_reject)

    # (8) The fallback selection rule is deterministic, including the case
    # where no candidate clears all diagnostics.
    rows = [
        {'p': 2, 'BIC': 100.0, 'clears_all_valid_BG_LB_horizons': False, 'failed_valid_diagnostic_count': 2},
        {'p': 4, 'BIC': 110.0, 'clears_all_valid_BG_LB_horizons': True, 'failed_valid_diagnostic_count': 0},
        {'p': 5, 'BIC': 90.0, 'clears_all_valid_BG_LB_horizons': True, 'failed_valid_diagnostic_count': 0},
    ]
    selected, rule = model.choose_fallback_candidate(rows)
    assert selected['p'] == 4 and rule.startswith('smallest_p')
    no_clear = [dict(r, clears_all_valid_BG_LB_horizons=False) for r in rows]
    no_clear[0]['failed_valid_diagnostic_count'] = 0
    no_clear[1]['failed_valid_diagnostic_count'] = 1
    no_clear[2]['failed_valid_diagnostic_count'] = 1
    selected, rule = model.choose_fallback_candidate(no_clear)
    assert selected['p'] == 2 and rule.startswith('no_clear_candidate')

    # (9) Pooled event controls avoid singleton perfect-fit pulse columns;
    # HC3 covariance is finite in the primary actual-data design.
    y3, X3 = model.design(q=3, p=1, start='2013-10')
    r3 = model.fit_model(y3, X3)
    hc3 = r3.get_robustcov_results(cov_type='HC3', use_t=False)
    assert np.isfinite(hc3.cov_params()).all()
    assert np.linalg.matrix_rank(X3.to_numpy()) == X3.shape[1]

    # (10) Chi-square and F reporting use the same Wald quadratic form but
    # their distinct reference distributions and scaling are explicit.
    hac, _, _, R, result = model.robust_tests(r3, ['x_l1', 'x_l2', 'x_l3'])
    assert np.isclose(result['HAC6_joint_F'], result['HAC6_joint_chi2'] / 3)
    assert 0 <= result['HAC6_joint_chi2_p'] <= 1
    assert 0 <= result['HAC6_joint_F_p'] <= 1

    print('ALL POST-REVIEW ECONOMETRIC BEHAVIOURAL TESTS PASSED')


if __name__ == '__main__':
    main()
