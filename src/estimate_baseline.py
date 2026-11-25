"""Post-results revision of the monthly food/non-food dynamic regression.

The original v3.1 and v3.2 packages are preserved. This script implements the
v3.3 post-results revision following independent inference review. All
estimates are conditional associations, not causal effects. Lags are always
constructed on the uninterrupted calendar.
"""
from pathlib import Path
import sys
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import chi2, f as f_dist, t as t_dist, probplot
from statsmodels.stats.diagnostic import (
    acorr_breusch_godfrey, acorr_ljungbox, het_arch, het_breuschpagan,
    linear_reset, breaks_cusumolsresid,
)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'model_results'
FIG = ROOT / 'outputs' / 'figures' / 'model_diagnostics'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
D = pd.read_csv(ROOT / 'data' / 'processed' / 'inflation_dataset.csv')
D['date'] = pd.PeriodIndex(D.date, freq='M')
D = D.set_index('date').sort_index()
EVENT_MONTHS = pd.period_range('2020-03', '2020-09', freq='M')
COVID_EXCLUSION = pd.period_range('2020-03', '2021-12', freq='M')
ALPHA = 0.05
BOOTSTRAP_REPS = 4999
SEED = 4552026


def _series(direction='food_to_nonfood', stl=False):
    if direction not in {'food_to_nonfood', 'nonfood_to_food', 'food_to_core', 'core_to_food'}:
        raise ValueError(f'Unknown direction: {direction}')
    if stl:
        sa = pd.read_csv(ROOT / 'outputs' / 'tables' / 'stl_seasonally_adjusted_monthly_inflation.csv')
        sa['date'] = pd.PeriodIndex(sa.date, freq='M')
        sa = sa.set_index('date')
        food = sa['Food and Beverages']
        nonfood = sa['Non-food']
    else:
        food = D['infl_food_log']
        nonfood = D['infl_nonfood_log']
    if direction == 'food_to_nonfood':
        return nonfood.rename('y'), food.rename('x')
    if direction == 'food_to_core':
        return D['infl_core_log'].rename('y'), food.rename('x')
    if direction == 'core_to_food':
        return food.rename('y'), D['infl_core_log'].rename('x')
    return food.rename('y'), nonfood.rename('x')


def design(q=3, p=0, start='2013-10', end='2025-12', mask_months=None,
           stl=False, direction='food_to_nonfood', post_interaction=False,
           include_covid_controls=True, covid_lag_horizon=None):
    """Create a design matrix after full-calendar lag construction.

    The earliest allowed month is calculated from the maximum lag, ensuring
    June 2013 cannot enter through any included regressor.
    COVID event-month controls are March-September 2020; an additional
    post-event exposure indicator covers later outcomes whose included lags
    reach one of those event months, through max(p,q).
    """
    if q < 1 or p < 0:
        raise ValueError('Require q >= 1 and p >= 0')
    maxlag = max(p, q)
    earliest_start = pd.Period('2013-06', freq='M') + maxlag + 1
    if pd.Period(start, freq='M') < earliest_start:
        raise ValueError(f'Start must be {earliest_start} or later to prevent June-2013 exposure at lag horizon {maxlag}')
    y, x = _series(direction, stl=stl)
    z = pd.DataFrame({'y': y, 'x0': x})
    for lag in range(1, maxlag + 1):
        z[f'x_l{lag}'] = x.shift(lag)
        z[f'y_l{lag}'] = y.shift(lag)
    z = z.loc[str(start):str(end)].copy()

    # Calendar month indicators; January is the reference category.
    month = pd.DataFrame(
        {f'month_{m:02d}': (z.index.month == m).astype(float) for m in range(2, 13)},
        index=z.index,
    )
    controls = [month]
    if include_covid_controls and not stl:
        # One pooled indicator covers direct event months and every subsequent
        # outcome row whose included lagged regressors can reach those months.
        affected = []
        exposure_horizon = maxlag if covid_lag_horizon is None else max(maxlag, int(covid_lag_horizon))
        for date in z.index:
            in_event = date in EVENT_MONTHS
            in_lag_exposure = any((date - lag) in EVENT_MONTHS for lag in range(1, exposure_horizon + 1))
            affected.append(float(in_event or in_lag_exposure))
        pulses = pd.DataFrame({'covid_affected_window': affected}, index=z.index)
        controls.append(pulses)

    regressors = [f'x_l{j}' for j in range(1, q + 1)] + ['x0']
    regressors += [f'y_l{i}' for i in range(1, p + 1)]
    X = pd.concat([z[regressors], *controls], axis=1)
    if post_interaction:
        post = (z.index >= pd.Period('2021-01', freq='M')).astype(float)
        for j in range(1, q + 1):
            X[f'x_l{j}_post2021'] = X[f'x_l{j}'].to_numpy() * post

    # A mask applies to outcome rows only, after all lags were constructed.
    if mask_months is not None:
        mask_months = set(pd.Period(m, freq='M') for m in mask_months)
        keep = ~z.index.isin(mask_months)
        z, X = z.loc[keep], X.loc[keep]

    joined = pd.concat([z['y'], X], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    y_out = joined['y']
    X_out = joined.drop(columns='y')
    # Remove all-zero columns (notably event pulses under an exclusion mask).
    zero_cols = [c for c in X_out.columns if np.allclose(X_out[c].to_numpy(), 0.0)]
    if zero_cols:
        X_out = X_out.drop(columns=zero_cols)
    X_out = sm.add_constant(X_out, has_constant='add')
    return y_out, X_out


def fit_model(y, X):
    if np.linalg.matrix_rank(X.to_numpy()) < X.shape[1]:
        raise ValueError('Rank-deficient design matrix; inspect redundant columns or sample size')
    return sm.OLS(y, X).fit()


def residual_tests(res, p):
    bg6 = float(acorr_breusch_godfrey(res, nlags=6)[1])
    bg12 = float(acorr_breusch_godfrey(res, nlags=12)[1])
    # Ljung-Box degrees of freedom adjusted by the AR order. It is undefined
    # when lag <= model_df, so the invalid horizon is reported as NaN.
    lbvals = {}
    for lag in (6, 12):
        if lag <= p:
            lbvals[lag] = np.nan
        else:
            lb = acorr_ljungbox(res.resid, lags=[lag], model_df=p, return_df=True)
            lbvals[lag] = float(lb.iloc[0]['lb_pvalue'])
    return {'BG_p_lag6': bg6, 'BG_p_lag12': bg12,
            'LB_p_lag6_model_df_p': lbvals[6], 'LB_p_lag12_model_df_p': lbvals[12]}


def fallback_trigger(tests):
    return any(
        np.isfinite(tests[f'LB_p_lag{lag}_model_df_p'])
        and tests[f'BG_p_lag{lag}'] < ALPHA
        and tests[f'LB_p_lag{lag}_model_df_p'] < ALPHA
        for lag in (6, 12)
    )


def candidate_clears(tests):
    valid = []
    for lag in (6, 12):
        lb = tests[f'LB_p_lag{lag}_model_df_p']
        bg = tests[f'BG_p_lag{lag}']
        if np.isfinite(lb):
            valid.extend([bg >= ALPHA, lb >= ALPHA])
    return bool(valid) and all(valid)



def choose_fallback_candidate(candidate_rows):
    """Select the smallest p that clears all valid BG/LB tests.

    If none clears, select the candidate with the fewest failed valid tests;
    ties are broken by BIC and then p. Input rows must include p, BIC,
    clears_all_valid_BG_LB_horizons and failed_valid_diagnostic_count.
    """
    clears = [r for r in candidate_rows if r['clears_all_valid_BG_LB_horizons']]
    if clears:
        return min(clears, key=lambda r: r['p']), 'smallest_p_clearing_all_valid_BG_LB_tests'
    return min(candidate_rows, key=lambda r: (r['failed_valid_diagnostic_count'], r['BIC'], r['p'])), \
        'no_clear_candidate_min_failed_tests_then_BIC_then_p'

def restriction_matrix(names, terms):
    missing = [term for term in terms if term not in names]
    if missing:
        raise ValueError(f'Missing restriction terms: {missing}')
    R = np.zeros((len(terms), len(names)))
    for i, term in enumerate(terms):
        R[i, names.index(term)] = 1.0
    return R


def contrast_wald(res, cov, R):
    beta = np.asarray(res.params)
    delta = R @ beta
    V = R @ np.asarray(cov.cov_params()) @ R.T
    stat = float(delta.T @ np.linalg.pinv(V) @ delta)
    df = int(np.linalg.matrix_rank(V))
    p_chi = float(chi2.sf(stat, df))
    fstat = stat / df
    p_f = float(f_dist.sf(fstat, df, res.df_resid))
    return {'chi2': stat, 'chi2_p': p_chi, 'F': fstat, 'F_p': p_f, 'df': df}


def robust_tests(res, terms, hac_lags=6):
    names = list(res.model.exog_names)
    R = restriction_matrix(names, terms)
    hac = res.get_robustcov_results(cov_type='HAC', maxlags=hac_lags,
                                    use_correction=True, use_t=False)
    hac12 = res.get_robustcov_results(cov_type='HAC', maxlags=12,
                                      use_correction=True, use_t=False)
    hc3 = res.get_robustcov_results(cov_type='HC3', use_t=False)
    a = contrast_wald(res, hac, R)
    b = contrast_wald(res, hc3, R)
    return hac, hac12, hc3, R, {
        'HAC6_joint_chi2': a['chi2'], 'HAC6_joint_chi2_p': a['chi2_p'],
        'HAC6_joint_F': a['F'], 'HAC6_joint_F_p': a['F_p'],
        'HC3_joint_chi2': b['chi2'], 'HC3_joint_chi2_p': b['chi2_p'],
    }


def delayed_sum(res, hac, q):
    # For q=1 this is beta1; for q=3 beta1+beta2+beta3; for q=6
    # the primary-comparable sum is still beta1-beta3, while full q-sum is
    # reported separately as an extended distributed-lag effect.
    names = list(res.model.exog_names)
    lo_terms = [f'x_l{i}' for i in range(1, min(q, 3) + 1)]
    lo_w = np.zeros(len(names))
    for term in lo_terms:
        lo_w[names.index(term)] = 1.0
    theta = float(lo_w @ np.asarray(res.params))
    se = float(np.sqrt(lo_w @ hac.cov_params() @ lo_w))
    crit = float(t_dist.ppf(0.975, res.df_resid))
    result = {
        'primary_comparable_delayed_sum_definition': f'beta1_to_beta{min(q,3)}',
        'primary_comparable_delayed_sum': theta,
        'primary_comparable_delayed_sum_se_HAC6': se,
        'primary_comparable_delayed_sum_CI_low': theta - crit * se,
        'primary_comparable_delayed_sum_CI_high': theta + crit * se,
    }
    all_terms = [f'x_l{i}' for i in range(1, q + 1)]
    if q > 3:
        w = np.zeros(len(names))
        for term in all_terms:
            w[names.index(term)] = 1.0
        full_theta = float(w @ np.asarray(res.params))
        full_se = float(np.sqrt(w @ hac.cov_params() @ w))
        result.update({'full_distributed_lag_sum_definition': f'beta1_to_beta{q}',
                       'full_distributed_lag_sum': full_theta,
                       'full_distributed_lag_sum_se_HAC6': full_se,
                       'full_distributed_lag_sum_CI_low': full_theta - crit * full_se,
                       'full_distributed_lag_sum_CI_high': full_theta + crit * full_se})
    return result


def hac_wald_statistic(y_values, X_values, R, nlags=6):
    """Fast Bartlett-kernel HAC quadratic form, matching statsmodels cov_hac."""
    xa = np.asarray(X_values, dtype=float)
    ya = np.asarray(y_values, dtype=float)
    n, k = xa.shape
    bread = np.linalg.inv(xa.T @ xa)
    beta = bread @ (xa.T @ ya)
    resid = ya - xa @ beta
    xu = xa * resid[:, None]
    meat = xu.T @ xu
    for lag in range(1, nlags + 1):
        weight = 1.0 - lag / (nlags + 1.0)
        cross = xu[lag:].T @ xu[:-lag]
        meat += weight * (cross + cross.T)
    cov = bread @ meat @ bread
    cov *= n / (n - k)  # statsmodels use_correction=True
    delta = R @ beta
    restricted_cov = R @ cov @ R.T
    return float(delta.T @ np.linalg.pinv(restricted_cov) @ delta)


def _block_signs(n, block_length, rng):
    signs = np.ones(n)
    offset = int(rng.integers(0, block_length))
    for start in range(-offset, n, block_length):
        signs[max(0, start):min(n, start + block_length)] = rng.choice([-1.0, 1.0])
    return signs


def wild_block_bootstrap_wald(y, X, terms, observed_stat, reps=BOOTSTRAP_REPS,
                              block_length=6, seed=SEED):
    """Restricted-null fixed-regressor block-wild bootstrap for a joint test.

    Six-month Rademacher multipliers are constant within consecutive blocks.
    Regressors, including lagged dependent variables, are held fixed. This is
    a finite-sample conditional inference procedure, not a causal bootstrap.
    """
    names = list(X.columns)
    R = restriction_matrix(names, terms)
    restricted_X = X.drop(columns=terms).to_numpy(dtype=float)
    full_X = X.to_numpy(dtype=float)
    yv = np.asarray(y, dtype=float)
    bread0 = np.linalg.inv(restricted_X.T @ restricted_X)
    beta0 = bread0 @ (restricted_X.T @ yv)
    fitted0 = restricted_X @ beta0
    resid0 = yv - fitted0
    rng = np.random.default_rng(seed)
    exceed = successful = 0
    for _ in range(reps):
        ystar = fitted0 + resid0 * _block_signs(len(yv), block_length, rng)
        try:
            stat = hac_wald_statistic(ystar, full_X, R, nlags=block_length)
            if np.isfinite(stat):
                successful += 1
                exceed += int(stat >= observed_stat)
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            continue
    return {
        'wild_block_bootstrap_type': 'restricted-null fixed-regressor block-wild',
        'wild_block_bootstrap_reps_requested': reps,
        'wild_block_bootstrap_reps_successful': successful,
        'wild_block_bootstrap_block_length': block_length,
        'wild_block_bootstrap_wald_tail_probability': (1 + exceed) / (1 + successful) if successful else np.nan,
        'wild_block_bootstrap_wald_mcse': float(np.sqrt(((1 + exceed) / (1 + successful)) * (1 - (1 + exceed) / (1 + successful)) / (successful + 1))) if successful else np.nan,
    }


def wild_block_bootstrap_t_interval(y, X, terms, weights, reps=BOOTSTRAP_REPS,
                                    block_length=6, seed=SEED + 31, prefix='delayed_sum'):
    """Studentised fixed-regressor block-wild bootstrap-t interval for a contrast."""
    xa = np.asarray(X, dtype=float); yv = np.asarray(y, dtype=float)
    names = list(X.columns); idx = [names.index(t) for t in terms]
    w = np.zeros(len(names)); w[idx] = np.asarray(weights, dtype=float)
    n, k = xa.shape
    bread = np.linalg.inv(xa.T @ xa)
    beta = bread @ (xa.T @ yv)
    resid = yv - xa @ beta
    theta = float(w @ beta)
    observed_se = float(np.sqrt(w @ (sm.OLS(y, X).fit().get_robustcov_results(
        cov_type='HAC', maxlags=block_length, use_correction=True, use_t=False).cov_params()) @ w))
    rng = np.random.default_rng(seed)
    tstats = []
    for _ in range(reps):
        ystar = xa @ beta + resid * _block_signs(n, block_length, rng)
        bstar = bread @ (xa.T @ ystar)
        estar = ystar - xa @ bstar
        xu = xa * estar[:, None]
        meat = xu.T @ xu
        for lag in range(1, block_length + 1):
            weight = 1.0 - lag / (block_length + 1.0)
            cross = xu[lag:].T @ xu[:-lag]
            meat += weight * (cross + cross.T)
        cov = bread @ meat @ bread * (n / (n - k))
        se = float(np.sqrt(w @ cov @ w))
        if np.isfinite(se) and se > 0:
            tstats.append((float(w @ bstar) - theta) / se)
    qlo, qhi = np.quantile(tstats, [0.025, 0.975])
    return {
        f'{prefix}_bootstrap_t_reps': len(tstats),
        f'{prefix}_bootstrap_t_CI_low': theta - qhi * observed_se,
        f'{prefix}_bootstrap_t_CI_high': theta - qlo * observed_se,
    }


def supf_statistic(y, X, trim=0.15):
    """Quandt-Andrews-style sup-F for a single unknown full-parameter break.

    Uses rank-aware split regressions because event pulse columns can be all
    zero in one side of a candidate split. Bootstrap calibration is supplied
    separately; no pointwise F p-value is misreported as a sup-F p-value.
    """
    x0 = X.to_numpy(dtype=float); y0 = np.asarray(y, dtype=float)
    beta0 = np.linalg.lstsq(x0, y0, rcond=None)[0]
    resid0 = y0 - x0 @ beta0
    ssr0 = float(resid0 @ resid0)
    rank0 = int(np.linalg.matrix_rank(x0))
    n = len(y0)
    lo = max(rank0 + 2, int(np.ceil(n * trim)))
    hi = min(n - rank0 - 2, int(np.floor(n * (1 - trim))))
    best = (-np.inf, None)
    for cut in range(lo, hi + 1):
        x1, x2 = x0[:cut], x0[cut:]
        y1, y2 = y0[:cut], y0[cut:]
        b1 = np.linalg.lstsq(x1, y1, rcond=None)[0]
        b2 = np.linalg.lstsq(x2, y2, rcond=None)[0]
        e1, e2 = y1 - x1 @ b1, y2 - x2 @ b2
        ssr1, ssr2 = float(e1 @ e1), float(e2 @ e2)
        r1, r2 = int(np.linalg.matrix_rank(x1)), int(np.linalg.matrix_rank(x2))
        num_df = max(1, r1 + r2 - rank0)
        den_df = n - r1 - r2
        denom = (ssr1 + ssr2) / den_df if den_df > 0 else np.nan
        stat = ((ssr0 - ssr1 - ssr2) / num_df) / denom if denom > 0 else np.nan
        if np.isfinite(stat) and stat > best[0]:
            best = (stat, y.index[cut])
    return {'supF_15pct_trim_statistic': float(best[0]),
            'supF_15pct_trim_break_date': str(best[1]) if best[1] is not None else ''}


def wild_block_bootstrap_supf(y, X, observed_supf, reps=BOOTSTRAP_REPS,
                               block_length=6, seed=SEED + 1):
    stable = fit_model(y, X)
    fitted = np.asarray(stable.fittedvalues)
    resid = np.asarray(stable.resid)
    rng = np.random.default_rng(seed)
    exceed = success = 0
    n = len(y)
    for _ in range(reps):
        signs = np.ones(n)
        offset = int(rng.integers(0, block_length))
        for start in range(-offset, n, block_length):
            signs[max(0, start):min(n, start + block_length)] = rng.choice([-1.0, 1.0])
        ystar = pd.Series(fitted + resid * signs, index=y.index)
        try:
            stat = supf_statistic(ystar, X)['supF_15pct_trim_statistic']
            if np.isfinite(stat):
                success += 1
                exceed += int(stat >= observed_supf)
        except (ValueError, np.linalg.LinAlgError):
            continue
    return {'supF_block_bootstrap_reps_requested': reps,
            'supF_block_bootstrap_reps_successful': success,
            'supF_block_bootstrap_block_length': block_length,
            'supF_block_bootstrap_tail_probability': (1 + exceed) / (1 + success) if success else np.nan}


def supf_partial_statistic(y, X, cols, trim=0.15):
    """Sup-F test for a break restricted to selected coefficient(s) only.

    All nuisance coefficients remain common across regimes. The returned
    statistic is a date-search statistic; its bootstrap calibration, not a
    pointwise F reference, is used for inference.
    """
    xa = X.to_numpy(dtype=float); ya = np.asarray(y, dtype=float)
    names = list(X.columns); select = [names.index(c) for c in cols]
    n, k = xa.shape
    bread = np.linalg.inv(xa.T @ xa)
    beta = bread @ (xa.T @ ya)
    e0 = ya - xa @ beta
    ssr0 = float(e0 @ e0)
    rank0 = np.linalg.matrix_rank(xa)
    lo = max(rank0 + 2, int(np.ceil(n * trim)))
    hi = min(n - rank0 - 2, int(np.floor(n * (1-trim))))
    best = -np.inf
    for cut in range(lo, hi + 1):
        post = np.zeros(n); post[cut:] = 1.0
        Q = xa[:, select] * post[:, None]
        Qm = Q - xa @ (bread @ (xa.T @ Q))
        gram = Qm.T @ Qm
        r_add = int(np.linalg.matrix_rank(gram))
        if r_add == 0:
            continue
        c = Qm.T @ e0
        reduction = float(c.T @ np.linalg.pinv(gram) @ c)
        ssr1 = max(ssr0 - reduction, 0.0)
        den_df = n - rank0 - r_add
        if den_df <= 0:
            continue
        stat = (reduction / r_add) / (ssr1 / den_df) if ssr1 > 0 else np.inf
        if np.isfinite(stat) and stat > best:
            best = stat
    return float(best)


def wild_block_bootstrap_partial_supf(y, X, observed, cols, reps=BOOTSTRAP_REPS,
                                      block_length=6, seed=SEED + 81):
    """Vectorised restricted-null bootstrap for the food-lag partial sup-F."""
    xa = X.to_numpy(dtype=float); yv = np.asarray(y, dtype=float)
    n, k = xa.shape; names = list(X.columns); select = [names.index(c) for c in cols]
    bread = np.linalg.inv(xa.T @ xa)
    beta = bread @ (xa.T @ yv)
    fitted = xa @ beta; resid = yv - fitted
    rng = np.random.default_rng(seed)
    # Generate the fixed-regressor null bootstrap sample matrix.
    signs = np.ones((n, reps), dtype=float)
    for b in range(reps):
        offset = int(rng.integers(0, block_length))
        for start in range(-offset, n, block_length):
            signs[max(0, start):min(n, start + block_length), b] = rng.choice([-1.0, 1.0])
    Ystar = fitted[:, None] + resid[:, None] * signs
    Bstar = bread @ (xa.T @ Ystar)
    E0 = Ystar - xa @ Bstar
    ssr0 = np.sum(E0 * E0, axis=0)
    rank0 = np.linalg.matrix_rank(xa)
    lo = max(rank0 + 2, int(np.ceil(n * 0.15)))
    hi = min(n - rank0 - 2, int(np.floor(n * 0.85)))
    max_stats = np.full(reps, -np.inf)
    for cut in range(lo, hi + 1):
        post = np.zeros(n); post[cut:] = 1.0
        Q = xa[:, select] * post[:, None]
        Qm = Q - xa @ (bread @ (xa.T @ Q))
        gram = Qm.T @ Qm
        r_add = int(np.linalg.matrix_rank(gram))
        if r_add == 0:
            continue
        inv_gram = np.linalg.pinv(gram)
        projected = Qm.T @ Ystar
        reduction = np.einsum('ir,ij,jr->r', projected, inv_gram, projected)
        ssr1 = np.maximum(ssr0 - reduction, np.finfo(float).eps)
        den_df = n - rank0 - r_add
        if den_df <= 0:
            continue
        stats = (reduction / r_add) / (ssr1 / den_df)
        max_stats = np.maximum(max_stats, stats)
    valid = np.isfinite(max_stats)
    exceed = int(np.sum(max_stats[valid] >= observed)); success = int(valid.sum())
    p = (1 + exceed) / (1 + success) if success else np.nan
    return {'partial_supF_bootstrap_reps_requested': reps,
            'partial_supF_bootstrap_reps_successful': success,
            'partial_supF_bootstrap_block_length': block_length,
            'partial_supF_bootstrap_tail_probability': p,
            'partial_supF_bootstrap_mcse': float(np.sqrt(p*(1-p)/(success+1))) if success else np.nan}


def stable_summary_text(res):
    """Remove the nondeterministic wall-clock Time line from statsmodels text."""
    return '\n'.join(line for line in res.summary().as_text().splitlines()
                     if not line.strip().startswith('Time:')) + '\n'


def diagnostics(y, X, res, p, label, q, run_bootstrap=True, bootstrap_interval=False,
                bootstrap_contemporaneous=False, run_stability_bootstrap=False,
                full_diagnostics=False):
    tests = residual_tests(res, p)
    arch6 = het_arch(res.resid, nlags=6)
    arch12 = het_arch(res.resid, nlags=12)
    bp = het_breuschpagan(res.resid, X)
    reset = linear_reset(res, power=2, use_f=True)
    hac, hac12, hc3, R, robust = robust_tests(res, [f'x_l{i}' for i in range(1, q + 1)])
    diag = {
        **tests, **robust,
        'ARCH_LM_p_lag6': float(arch6[1]), 'ARCH_LM_p_lag12': float(arch12[1]),
        'Breusch_Pagan_Koenker_p': float(bp[1]),
        'White_cross_product_test_status': 'omitted: near-saturated auxiliary regression',
        'RESET_p': float(reset.pvalue),
        'n': int(res.nobs), 'p': p, 'q': q, 'BIC': float(res.bic), 'R2': float(res.rsquared),
        'design_rank': int(np.linalg.matrix_rank(X.to_numpy())), 'design_columns': int(X.shape[1]),
    }
    diag.update(delayed_sum(res, hac, q))
    # HAC12 Wald and HC3 coefficient standard errors are retained as sensitivities.
    w12 = contrast_wald(res, hac12, R)
    diag['HAC12_joint_chi2'] = w12['chi2']
    diag['HAC12_joint_chi2_p'] = w12['chi2_p']
    # HAC6 coefficient p-values and conventional/robust SEs.
    names = list(X.columns)
    coef = pd.DataFrame({'term': names, 'coefficient': np.asarray(res.params),
                         'se_OLS': np.asarray(res.bse), 'se_HAC6': np.asarray(hac.bse),
                         'p_HAC6_t': 2 * t_dist.sf(np.abs(np.asarray(hac.params) / np.asarray(hac.bse)), res.df_resid), 'se_HAC12': np.asarray(hac12.bse),
                         'p_HAC12_t': 2 * t_dist.sf(np.abs(np.asarray(hac12.params) / np.asarray(hac12.bse)), res.df_resid), 'se_HC3': np.asarray(hc3.bse),
                         'p_HC3_t': 2 * t_dist.sf(np.abs(np.asarray(hc3.params) / np.asarray(hc3.bse)), res.df_resid)})
    coef.to_csv(OUT / f'{label}_coefficients.csv', index=False)
    # Food-lag VIFs computed after zero-column removal.
    vif = []
    for term in [f'x_l{i}' for i in range(1, q + 1)]:
        vif.append({'term': term, 'VIF': float(variance_inflation_factor(X.to_numpy(), names.index(term)))})
    pd.DataFrame(vif).to_csv(OUT / f'{label}_food_lag_vif.csv', index=False)
    food_lag_terms = [f'x_l{i}' for i in range(1, q+1)]
    if full_diagnostics:
        # Influence diagnostics; unit-leverage event indicators may yield undefined Cook's D.
        influence = res.get_influence()
        cook = np.asarray(influence.cooks_distance[0])
        leverage = np.asarray(influence.hat_matrix_diag)
        finite = np.isfinite(cook)
        if finite.any():
            max_i = int(np.nanargmax(np.where(finite, cook, np.nan)))
            diag['max_finite_Cooks_D'] = float(cook[max_i])
            diag['max_finite_Cooks_date'] = str(y.index[max_i])
        else:
            diag['max_finite_Cooks_D'] = np.nan
            diag['max_finite_Cooks_date'] = ''
        diag['undefined_Cooks_count'] = int((~finite).sum())
        diag['unit_leverage_count'] = int((leverage >= 1 - 1e-10).sum())
        inf = pd.DataFrame({'date': y.index.astype(str), 'leverage': leverage, 'cooks_distance': cook})
        inf.sort_values('cooks_distance', ascending=False).to_csv(OUT / f'{label}_influence.csv', index=False)
        # Residual ACF/PACF and Q-Q plots.
        fig, ax = plt.subplots(figsize=(8, 4)); plot_acf(res.resid, lags=min(24, len(res.resid)//3), ax=ax)
        ax.set_title(f'Residual ACF — {label}'); fig.tight_layout(); fig.savefig(FIG / f'{label}_residual_acf.png', dpi=150); plt.close(fig)
        fig, ax = plt.subplots(figsize=(8, 4)); plot_pacf(res.resid, lags=min(24, len(res.resid)//3), method='ywm', ax=ax)
        ax.set_title(f'Residual PACF — {label}'); fig.tight_layout(); fig.savefig(FIG / f'{label}_residual_pacf.png', dpi=150); plt.close(fig)
        fig, ax = plt.subplots(figsize=(6, 6)); probplot(res.resid, dist='norm', plot=ax); ax.set_title(f'Residual Q-Q — {label}')
        fig.tight_layout(); fig.savefig(FIG / f'{label}_residual_qq.png', dpi=150); plt.close(fig)
        # CUSUM of OLS residuals, with the package's reported critical values.
        cusum_stat, cusum_p, cusum_crit = breaks_cusumolsresid(res.resid, ddof=X.shape[1])
        diag['CUSUM_statistic'] = float(cusum_stat)
        diag['CUSUM_p'] = float(cusum_p)
        diag['CUSUM_5pct_critical'] = float(next((critical for level, critical in cusum_crit if abs(level - 5) < 1e-9), np.nan))
        # Expanding-window recursive coefficients for food lags.
        rec_rows = []
        min_obs = max(X.shape[1] + 5, int(0.30 * len(y)))
        for end in range(min_obs, len(y) + 1):
            rr = sm.OLS(y.iloc[:end], X.iloc[:end]).fit()
            rec_rows.append({'end_date': str(y.index[end-1]), **{f'coef_{v}': float(rr.params[v]) for v in [f'x_l{i}' for i in range(1, q+1)]}})
        pd.DataFrame(rec_rows).to_csv(OUT / f'{label}_recursive_coefficients.csv', index=False)
        # Full-parameter sup-F retained as descriptive diagnostic only; its date is
        # not interpreted because seasonal/COVID terms can produce a plateau.
        sf = supf_statistic(y, X, trim=0.15)
        diag['full_parameter_supF_15pct_trim_statistic_diagnostic_only'] = sf['supF_15pct_trim_statistic']
        partial_sf = supf_partial_statistic(y, X, food_lag_terms, trim=0.15)
        diag['food_lag_partial_supF_15pct_trim_statistic'] = partial_sf
    if run_bootstrap:
        diag.update(wild_block_bootstrap_wald(y, X, food_lag_terms,
                                                robust['HAC6_joint_chi2']))
        if bootstrap_contemporaneous and 'x0' in names:
            x0_stat = float(hac.wald_test(restriction_matrix(names, ['x0']), use_f=False, scalar=True).statistic)
            diag.update({f'contemporaneous_{k}': v for k, v in wild_block_bootstrap_wald(
                y, X, ['x0'], x0_stat, seed=SEED + 11).items()})
        if bootstrap_interval:
            weights = np.ones(len(food_lag_terms))
            diag.update(wild_block_bootstrap_t_interval(y, X, food_lag_terms, weights))
        if run_stability_bootstrap:
            if not full_diagnostics:
                raise ValueError('run_stability_bootstrap requires full_diagnostics=True')
            diag.update(wild_block_bootstrap_partial_supf(y, X, partial_sf, food_lag_terms))
    return diag, coef



def select_bic_candidate(candidate_rows):
    """Deterministic BIC selection; ties go to the lower own-lag order."""
    return min(candidate_rows, key=lambda row: (row['BIC'], row['p']))

def _candidate_row(p, q, y, X, res):
    return {'p': p, 'q': q, 'n': int(res.nobs), 'BIC': float(res.bic), 'AIC': float(res.aic),
            **residual_tests(res, p)}


def estimate(label, q, start, mask_months=None, stl=False, direction='food_to_nonfood',
             max_initial_p=3, allow_fallback=True, do_diagnostics=True, run_bootstrap=True,
             include_covid_controls=True, bootstrap_interval=False,
             bootstrap_contemporaneous=False, run_stability_bootstrap=False,
             full_diagnostics=False):
    initial_rows = []
    initial_fits = {}
    for p in range(max_initial_p + 1):
        y, X = design(q, p, start, mask_months=mask_months, stl=stl, direction=direction,
                      include_covid_controls=include_covid_controls, covid_lag_horizon=max(q, max_initial_p))
        r = fit_model(y, X)
        row = _candidate_row(p, q, y, X, r)
        initial_rows.append(row); initial_fits[p] = (y, X, r)
    selected_p = select_bic_candidate(initial_rows)['p']
    original_y, original_X, original_r = initial_fits[selected_p]
    original_tests = residual_tests(original_r, selected_p)
    fallback_used = bool(allow_fallback and fallback_trigger(original_tests))
    if fallback_used:
        # Preserve the complete original BIC-selected model before any fallback
        # re-estimation, not merely its BIC and residual diagnostic row.
        diagnostics(original_y, original_X, original_r, selected_p,
                    f'{label}_original_bic_selected', q, run_bootstrap=False)
        (OUT/f'{label}_original_bic_selected_ols_summary.txt').write_text(
            stable_summary_text(original_r) +
            '\n\nOriginal BIC-selected model before fallback re-estimation.\n'
        )
    final_y, final_X, final_r = original_y, original_X, original_r
    final_p, final_start = selected_p, start
    fallback_rows = []
    if fallback_used:
        # For p up to 6, use Jan-2014 onwards so June-2013 cannot enter through lags.
        fallback_start = max(str(start), '2014-01')
        candidates = []
        for p in range(7):
            yy, XX = design(q, p, fallback_start, mask_months=mask_months, stl=stl,
                            direction=direction, include_covid_controls=include_covid_controls,
                            covid_lag_horizon=max(q, 6))
            rr = fit_model(yy, XX)
            tt = residual_tests(rr, p)
            row = _candidate_row(p, q, yy, XX, rr)
            row['clears_all_valid_BG_LB_horizons'] = candidate_clears(tt)
            row['failed_valid_diagnostic_count'] = sum(
                int(v < ALPHA) for key, v in tt.items() if key.startswith(('BG_p_', 'LB_p_')) and np.isfinite(v)
            )
            fallback_rows.append(row); candidates.append((p, yy, XX, rr, tt, row))
        selected_row, fallback_selection_rule = choose_fallback_candidate([c[5] for c in candidates])
        chosen = next(c for c in candidates if c[0] == selected_row['p'])
        final_p, final_y, final_X, final_r = chosen[0], chosen[1], chosen[2], chosen[3]
        final_start = fallback_start
    pd.DataFrame(initial_rows).to_csv(OUT / f'{label}_initial_bic_candidates.csv', index=False)
    pd.DataFrame(fallback_rows).to_csv(OUT / f'{label}_fallback_candidates.csv', index=False)
    diag = {'label': label, 'direction': direction, 'original_start': start,
            'final_start': final_start, 'original_BIC_selected_p': selected_p,
            'final_selected_p': final_p, 'q': q, 'fallback_used': fallback_used,
            'fallback_selection_rule': fallback_selection_rule if fallback_used else 'not_triggered',
            'original_model_BG_LB': str(original_tests), 'n': int(final_r.nobs),
            'BIC': float(final_r.bic), 'R2': float(final_r.rsquared)}
    if do_diagnostics:
        dd, coef = diagnostics(final_y, final_X, final_r, final_p, label, q,
                               run_bootstrap=run_bootstrap, bootstrap_interval=bootstrap_interval,
                               bootstrap_contemporaneous=bootstrap_contemporaneous,
                               run_stability_bootstrap=run_stability_bootstrap,
                               full_diagnostics=full_diagnostics)
        diag.update(dd)
        # Include row-level estimation-period metadata.
        diag['sample_first_date'] = str(final_y.index.min())
        diag['sample_last_date'] = str(final_y.index.max())
        pd.DataFrame([diag]).to_csv(OUT / f'{label}_model_summary.csv', index=False)
        (OUT / f'{label}_ols_summary.txt').write_text(
            stable_summary_text(final_r) +
            '\n\nInterpretation: conditional predictive association, not causal identification.\n'
        )
    return diag, (final_y, final_X, final_r)


def leave_out_checks(label, base_y, base_X, base_res, q):
    periods = {
        'march_september_2020': pd.period_range('2020-03','2020-09',freq='M'),
        'july_2023': [pd.Period('2023-07',freq='M')],
        'september_2023_high_cook': [pd.Period('2023-09',freq='M')],
        'may_2021_high_cook': [pd.Period('2021-05',freq='M')],
        'april_2022_high_cook': [pd.Period('2022-04',freq='M')],
        'nov_dec_2013': pd.period_range('2013-11','2013-12',freq='M'),
        'april_may_2020_collection_gap': pd.period_range('2020-04','2020-05',freq='M'),
        'june_2013': [pd.Period('2013-06',freq='M')],
    }
    terms = [f'x_l{i}' for i in range(1,q+1)]
    rows=[]
    for name, remove in periods.items():
        keep = ~base_y.index.isin(remove)
        if keep.sum() == len(base_y):
            rows.append({'leave_out':name,'status':'target month not in estimation outcomes','n':len(base_y)})
            continue
        y, X = base_y.loc[keep], base_X.loc[keep]
        X = X.loc[:, [c for c in X.columns if c == 'const' or not np.allclose(X[c].to_numpy(), 0.0)]]
        if np.linalg.matrix_rank(X.to_numpy()) < X.shape[1]:
            rows.append({'leave_out':name,'status':'rank deficient after exclusion','n':len(y)})
            continue
        r=fit_model(y,X)
        hac, _, _, R, tests=robust_tests(r,terms)
        s=delayed_sum(r,hac,q)
        rows.append({'leave_out':name,'status':'estimated','n':int(r.nobs),
                     'HAC6_joint_chi2_p':tests['HAC6_joint_chi2_p'],**s})
    pd.DataFrame(rows).to_csv(OUT/f'{label}_leave_out_checks.csv',index=False)


def post2021_interaction(q=3, start='2013-10'):
    """Exploratory, ex-post 2021 interaction; bootstrap is primary inference."""
    rows=[]
    for p in range(4):
        y,X=design(q,p,start,covid_lag_horizon=max(q,3))
        r=fit_model(y,X); rows.append({'p':p,'BIC':r.bic})
    p=select_bic_candidate(rows)['p']
    y,X=design(q,p,start,post_interaction=True,covid_lag_horizon=max(q,3))
    r=fit_model(y,X)
    terms=[f'x_l{i}_post2021' for i in range(1,q+1)]
    hac,_,_,R,tests=robust_tests(r,terms)
    boot=wild_block_bootstrap_wald(y,X,terms,tests['HAC6_joint_chi2'],seed=SEED+515)
    out={'p_selected':p,'q':q,'n':int(r.nobs),
         'post2021_lag_interaction_HAC6_chi2_p':tests['HAC6_joint_chi2_p'],
         'post2021_lag_interaction_HAC6_F_p':tests['HAC6_joint_F_p'],
         'post2021_lag_interaction_bootstrap_tail_probability':boot['wild_block_bootstrap_wald_tail_probability'],
         'bootstrap_reps':boot['wild_block_bootstrap_reps_successful'],
         'break_date_status':'January 2021 is an ex-post interaction split, not an identified break date',
         'BIC':float(r.bic)}
    pd.DataFrame([out]).to_csv(OUT/'post2021_food_lag_interaction.csv',index=False)
    return out

def export_bidirectional_summary():
    forward = pd.read_csv(OUT/'postreview_q3_jan2014_model_summary.csv').iloc[0]
    reverse = pd.read_csv(OUT/'postreview_reverse_nonfood_to_food_q3_model_summary.csv').iloc[0]
    rows=[]
    for direction, row, predictor in [
        ('food_to_nonfood', forward, 'Food and Beverages'),
        ('nonfood_to_food', reverse, 'Non-food'),
    ]:
        rows.append({
            'direction': direction, 'lagged_predictor': predictor,
            'start': row['sample_first_date'], 'end': row['sample_last_date'],
            'n': int(row['n']), 'own_lag_order_p': int(row['final_selected_p']),
            'predictor_lag_horizon_q': int(row['q']),
            'HAC6_joint_chi2_p': row['HAC6_joint_chi2_p'],
            'HAC6_joint_F_p': row['HAC6_joint_F_p'],
            'HAC12_joint_chi2_p': row['HAC12_joint_chi2_p'],
            'HC3_joint_chi2_p': row['HC3_joint_chi2_p'],
            'conditional_delayed_sum': row['primary_comparable_delayed_sum'],
            'delayed_sum_CI_low': row['primary_comparable_delayed_sum_CI_low'],
            'delayed_sum_CI_high': row['primary_comparable_delayed_sum_CI_high'],
            'interpretation': 'Granger-style conditional predictive association; not causal identification.'
        })
    pd.DataFrame(rows).to_csv(OUT/'bidirectional_granger_style_summary.csv',index=False)


def short_run_sum_benchmark():
    """Reproduce beta0+beta1+beta2+beta3 effect-size calibration for both outcomes."""
    rows=[]
    for direction, label in [('food_to_nonfood','food_to_nonfood_primary'),
                             ('food_to_core','food_to_core_primary')]:
        y, X = design(q=3, p=1, start='2013-10', direction=direction)
        res = fit_model(y, X)
        terms = ['x0','x_l1','x_l2','x_l3']
        weights = np.ones(len(terms))
        names = list(X.columns)
        w = np.zeros(len(names))
        for term, weight in zip(terms, weights):
            w[names.index(term)] = weight
        hac = res.get_robustcov_results(cov_type='HAC', maxlags=6,
                                        use_correction=True, use_t=False)
        theta = float(w @ np.asarray(res.params))
        se = float(np.sqrt(w @ hac.cov_params() @ w))
        crit = float(t_dist.ppf(0.975, res.df_resid))
        boot = wild_block_bootstrap_t_interval(y, X, terms, weights,
            prefix='short_run_sum', seed=SEED + (101 if direction == 'food_to_nonfood' else 202))
        rows.append({'outcome':label,'n':int(res.nobs),
            'short_run_sum_beta0_to_beta3':theta,'HAC6_SE':se,
            'HAC6_95CI_low':theta-crit*se,'HAC6_95CI_high':theta+crit*se,
            **boot,
            'interpretation':'Includes contemporaneous and three delayed food coefficients. RBI ARDL comparator is not identical.'})
    pd.DataFrame(rows).to_csv(OUT/'food_to_inflation_short_run_sum_benchmark.csv',index=False)
    return pd.DataFrame(rows)


def main():
    results=[]
    # Baseline non-food outcome: report pooled COVID adjustment and a genuinely
    # different exclusion of the imputed April-May 2020 rows.
    base_diag, base_parts=estimate('postreview_primary_q3_oct2013',3,'2013-10',run_bootstrap=True,bootstrap_interval=True,bootstrap_contemporaneous=True,run_stability_bootstrap=True,full_diagnostics=True)
    results.append(base_diag)
    leave_out_checks('postreview_primary_q3_oct2013',*base_parts,3)
    for label,q in [('postreview_q3_jan2014',3),('postreview_q1_jan2014',1),('postreview_q6_jan2014',6)]:
        dd,_=estimate(label,q,'2014-01',run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_fit2016_q3',3,'2016-04',run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_covid_exclusion_mar2020_dec2021_q3',3,'2013-10',
                  mask_months=COVID_EXCLUSION,allow_fallback=False,include_covid_controls=False,
                  run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_covid_exclusion_mar2020_dec2020_q3',3,'2013-10',
                  mask_months=pd.period_range('2020-03','2020-12',freq='M'),allow_fallback=False,
                  include_covid_controls=False,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_imputed_aprmay2020_exclusion_nonfood_q3',3,'2013-10',
                  mask_months=pd.period_range('2020-04','2020-05',freq='M'),allow_fallback=False,
                  include_covid_controls=True,run_bootstrap=True); results.append(dd)

    # Pre-declared operational core outcome: food and fuel groups excluded.
    for label,q,start in [
        ('postreview_core_q3_oct2013',3,'2013-10'),
        ('postreview_core_q3_jan2014',3,'2014-01'),
        ('postreview_core_q1_jan2014',1,'2014-01'),
        ('postreview_core_q6_jan2014',6,'2014-01'),
    ]:
        dd,_=estimate(label,q,start,direction='food_to_core',run_bootstrap=True,
                      bootstrap_interval=(label=='postreview_core_q3_oct2013'),
                      bootstrap_contemporaneous=(label=='postreview_core_q3_oct2013'),
                      run_stability_bootstrap=(label=='postreview_core_q3_oct2013'),
                      full_diagnostics=(label=='postreview_core_q3_oct2013')); results.append(dd)
    dd,_=estimate('postreview_core_imputed_aprmay2020_exclusion_q3',3,'2013-10',
                  direction='food_to_core',mask_months=pd.period_range('2020-04','2020-05',freq='M'),
                  allow_fallback=False,include_covid_controls=True,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_core_covid_exclusion_mar2020_dec2021_q3',3,'2013-10',
                  direction='food_to_core',mask_months=COVID_EXCLUSION,allow_fallback=False,
                  include_covid_controls=False,run_bootstrap=True); results.append(dd)

    # Reverse direction remains exploratory; all variants receive the same
    # bootstrap inference and explicit COVID/imputation sensitivities.
    dd,_=estimate('postreview_reverse_nonfood_to_food_q3',3,'2014-01',
                  direction='nonfood_to_food',allow_fallback=False,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_reverse_covid_exclusion_mar2020_dec2020_q3',3,'2014-01',
                  direction='nonfood_to_food',mask_months=pd.period_range('2020-03','2020-12',freq='M'),
                  allow_fallback=False,include_covid_controls=False,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_reverse_covid_exclusion_mar2020_dec2021_q3',3,'2014-01',
                  direction='nonfood_to_food',mask_months=COVID_EXCLUSION,
                  allow_fallback=False,include_covid_controls=False,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_reverse_imputed_aprmay2020_exclusion_q3',3,'2014-01',
                  direction='nonfood_to_food',mask_months=pd.period_range('2020-04','2020-05',freq='M'),
                  allow_fallback=False,include_covid_controls=True,run_bootstrap=True); results.append(dd)
    dd,_=estimate('postreview_reverse_stl_q3',3,'2014-01',direction='nonfood_to_food',
                  stl=True,allow_fallback=False,include_covid_controls=False,run_bootstrap=True); results.append(dd)

    # STL-adjusted forward sensitivity is deliberately estimated without the
    # pooled COVID control; the design note and results table state this.
    dd,_=estimate('postreview_stl_adjusted_q3',3,'2013-10',stl=True,
                  allow_fallback=False,include_covid_controls=False,
                  run_bootstrap=True,bootstrap_interval=True); results.append(dd)

    interaction=post2021_interaction()
    short_run_sum_benchmark()
    pd.DataFrame(results).to_csv(OUT/'postreview_model_comparison_summary.csv',index=False)
    export_bidirectional_summary()
    print(pd.DataFrame(results)[['label','direction','final_start','final_selected_p','q','n',
        'HAC6_joint_chi2_p','wild_block_bootstrap_wald_tail_probability',
        'primary_comparable_delayed_sum','fallback_used']].to_string(index=False))
    print('Post-2021 interaction:',interaction)

if __name__ == '__main__':
    main()
