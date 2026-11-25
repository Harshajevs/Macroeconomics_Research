"""Pre-estimation diagnostics and specification review for food/non-food CPI.

This script does NOT produce the final spillover regression. It evaluates the
properties needed to choose a defensible model using the authentic CPI dataset.
Run from the project root:
    python src/econometric_design_diagnostics.py
"""
from __future__ import annotations

from pathlib import Path
import itertools
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss, coint, zivot_andrews
from statsmodels.tsa.ardl import ARDL, UECM
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_arch, het_breuschpagan

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg

DATA = cfg.OUT_FILE
TABLES = cfg.ROOT / "outputs" / "tables"
DOCS = cfg.ROOT / "documentation"
SEED = 20261114


def load_data() -> pd.DataFrame:
    if not DATA.exists():
        raise FileNotFoundError(f"Run python src/build_dataset.py first: {DATA}")
    df = pd.read_csv(DATA)
    df["date"] = pd.PeriodIndex(df["date"], freq="M")
    df = df.set_index("date").sort_index()
    required = ["food", "nonfood", "nonfood_from_headline", "core", "cfpi",
                "infl_food_log", "infl_nonfood_log", "infl_core_log",
                "infl_food_yoy", "infl_nonfood_yoy", "flag_collection_gap"]
    missing = [c for c in required if c not in df]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    # This pre-estimation diagnostic is retained as a historical Stage-2 check and
    # intentionally works on the common YoY comparison window. The corrected
    # descriptive and later regression scripts use the expanded MoM window.
    df = df.loc[cfg.YOY_ANALYSIS_START:cfg.YOY_ANALYSIS_END]
    if len(df) != 144 or str(df.index.min()) != "2014-01" or str(df.index.max()) != "2025-12":
        raise ValueError("Expected 144 monthly observations from 2014-01 to 2025-12")
    return df


def stationarity_table(df: pd.DataFrame) -> pd.DataFrame:
    specs = {
        "log_food_index": (np.log(df.food), "ct"),
        "log_nonfood_index": (np.log(df.nonfood), "ct"),
        "log_core_index": (np.log(df.core), "ct"),
        "monthly_log_food_inflation": (df.infl_food_log, "c"),
        "monthly_log_nonfood_inflation": (df.infl_nonfood_log, "c"),
        "monthly_log_core_inflation": (df.infl_core_log, "c"),
        "yoy_food_inflation": (df.infl_food_yoy, "c"),
        "yoy_nonfood_inflation": (df.infl_nonfood_yoy, "c"),
    }
    rows = []
    for name, (series, regression) in specs.items():
        s = pd.Series(series).dropna().astype(float)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            adf = adfuller(s, regression=regression, autolag="AIC", maxlag=12)
            try:
                kp = kpss(s, regression=regression, nlags="auto")
                kp_stat, kp_p = float(kp[0]), float(kp[1])
            except Exception:
                kp_stat, kp_p = np.nan, np.nan
        rows.append({
            "series": name, "n": len(s), "ADF_regression": regression,
            "ADF_statistic": float(adf[0]), "ADF_pvalue": float(adf[1]),
            "ADF_lags": int(adf[2]), "KPSS_regression": regression,
            "KPSS_statistic": kp_stat, "KPSS_pvalue": kp_p,
            "interpretation_note": "ADF H0: unit root; KPSS H0: level/trend stationarity. Read jointly; neither test is decisive alone."
        })
    return pd.DataFrame(rows)


def month_dummies(index: pd.PeriodIndex) -> pd.DataFrame:
    months = pd.Series(index.month, index=index, name="month")
    return pd.get_dummies(months.astype(str), prefix="month", drop_first=True, dtype=float)


def seasonal_analysis(df: pd.DataFrame):
    D = month_dummies(df.index)
    rows, adjusted = [], pd.DataFrame(index=df.index)
    columns = {
        "Food and Beverages": "infl_food_log",
        "Non-food": "infl_nonfood_log",
        "Core": "infl_core_log",
    }
    for label, col in columns.items():
        y = df[col].astype(float)
        tmp = pd.concat([y.rename("y"), D], axis=1).dropna()
        X = sm.add_constant(tmp[D.columns], has_constant="add")
        fit = sm.OLS(tmp.y, X).fit()
        hac = fit.get_robustcov_results(cov_type="HAC", maxlags=6)
        # Joint Wald test that all calendar-month effects are zero.
        names = list(fit.params.index)
        ix = [names.index(c) for c in D.columns]
        R = np.zeros((len(ix), len(names)))
        for r, j in enumerate(ix):
            R[r, j] = 1.0
        wald = hac.f_test(R)
        # Subtract fitted calendar component and add back the unconditional mean.
        fitted = fit.predict(X)
        adj = (tmp.y - (fitted - fit.params["const"]))
        adj = adj + y.mean() - adj.mean()
        adjusted.loc[adj.index, label] = adj
        rows.append({
            "series": label, "n": int(fit.nobs), "raw_mean_pct": float(y.mean()),
            "raw_sd_pp": float(y.std(ddof=1)), "seasonal_adjusted_mean_pct": float(adj.mean()),
            "seasonal_adjusted_sd_pp": float(adj.std(ddof=1)),
            "month_effects_joint_F": float(wald.fvalue),
            "month_effects_joint_pvalue_HAC6": float(wald.pvalue),
            "month_dummy_R2": float(fit.rsquared),
            "adjustment": "OLS calendar-month fixed effects on monthly log inflation; residualized series recentered to the original mean. Not an official X-13 adjustment."
        })
    # Report the average seasonal pattern for the three monthly rates.
    month_rows = []
    for label, col in columns.items():
        tmp = pd.DataFrame({"month": df.index.month, "rate": df[col].values})
        for m, grp in tmp.groupby("month"):
            month_rows.append({"series": label, "calendar_month": int(m),
                               "mean_monthly_log_inflation_pct": float(grp.rate.mean()),
                               "sd_monthly_log_inflation_pp": float(grp.rate.std(ddof=1))})
    return pd.DataFrame(rows), pd.DataFrame(month_rows), adjusted


def moving_block_bootstrap_sd_diff(x, y, block_len, reps=4999, seed=SEED):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < block_len:
        raise ValueError("Bootstrap series must be paired and at least one block long")
    rng = np.random.default_rng(seed + block_len)
    n = len(x)
    nblocks = int(np.ceil(n / block_len))
    starts_max = n - block_len
    effects = np.empty(reps)
    for b in range(reps):
        starts = rng.integers(0, starts_max + 1, size=nblocks)
        ix = np.concatenate([np.arange(s, s + block_len) for s in starts])[:n]
        effects[b] = np.std(x[ix], ddof=1) - np.std(y[ix], ddof=1)
    estimate = np.std(x, ddof=1) - np.std(y, ddof=1)
    lo, hi = np.quantile(effects, [0.025, 0.975])
    return {
        "statistic": "SD(seasonally adjusted food MoM log inflation) - SD(seasonally adjusted non-food MoM log inflation)",
        "estimate_pp": estimate, "ci_2_5_pp": lo, "ci_97_5_pp": hi,
        "block_length_months": block_len, "replications": reps,
        "seed": seed + block_len,
        "bootstrap_probability_difference_le_zero": float(np.mean(effects <= 0)),
        "method": "paired non-circular moving-block bootstrap"
    }



def break_aware_unit_root_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Zivot-Andrews one-break unit-root tests on log price-index levels."""
    rows = []
    for label, col in [("Food and Beverages", "food"), ("Non-food", "nonfood"),
                       ("Core", "core"), ("Non-food (headline-derived)", "nonfood_from_headline")]:
        series = np.log(df[col].astype(float))
        for regression in ["c", "ct"]:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = zivot_andrews(series, trim=0.15, maxlag=12,
                                       regression=regression, autolag="AIC")
            break_idx = int(result[4])
            rows.append({
                "series": label, "ZA_regression": regression,
                "ZA_statistic": float(result[0]), "ZA_pvalue": float(result[1]),
                "critical_1pct": float(result[2]["1%"]),
                "critical_5pct": float(result[2]["5%"]),
                "critical_10pct": float(result[2]["10%"]),
                "selected_lags": int(result[3]),
                "estimated_break_month": str(df.index[break_idx]),
                "interpretation": "Do not reject unit root with one break" if result[1] >= 0.05 else "Reject unit root with one break"
            })
    return pd.DataFrame(rows)


def adjusted_series_stationarity(adjusted: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label in adjusted.columns:
        series = adjusted[label].dropna().astype(float)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            adf = adfuller(series, regression="c", autolag="AIC", maxlag=12)
            kp = kpss(series, regression="c", nlags="auto")
        rows.append({
            "series": f"{label} (calendar-month adjusted monthly log inflation)",
            "n": int(len(series)), "ADF_regression": "c", "ADF_statistic": float(adf[0]),
            "ADF_pvalue": float(adf[1]), "ADF_lags": int(adf[2]),
            "KPSS_regression": "c", "KPSS_statistic": float(kp[0]),
            "KPSS_pvalue": float(kp[1]),
            "interpretation_note": "Calendar-month fixed effects removed; ADF H0 unit root, KPSS H0 stationarity."
        })
    return pd.DataFrame(rows)


def short_run_lag_selection(df: pd.DataFrame) -> pd.DataFrame:
    """Select own-lag order by BIC with a fixed food lag horizon 0..6."""
    rows = []
    samples = {
        "Full 2014-2025": df.index,
        "FIT from 2016-04": df.index[df.index >= pd.Period("2016-04", freq="M")],
    }
    for sample_name, idx in samples.items():
        sub = df.loc[idx]
        D = month_dummies(sub.index)
        for outcome, ycol, xcol in [("Non-food", "infl_nonfood_log", "infl_food_log"),
                                    ("Core", "infl_core_log", "infl_food_log")]:
            y, x = sub[ycol].astype(float), sub[xcol].astype(float)
            candidates = []
            for p in range(1, 7):
                X = pd.DataFrame({"const": 1.0}, index=sub.index)
                for i in range(1, p + 1):
                    X[f"y_lag{i}"] = y.shift(i)
                for j in range(0, 7):
                    X[f"food_lag{j}"] = x.shift(j)
                X = pd.concat([X, D], axis=1)
                z = pd.concat([y.rename("y"), X], axis=1).dropna()
                fit = sm.OLS(z.y, z.drop(columns="y")).fit()
                candidates.append((float(fit.bic), p, float(fit.aic), float(fit.rsquared), int(fit.nobs)))
            best = min(candidates, key=lambda value: value[0])
            for bic, p, aic, r2, n in candidates:
                rows.append({
                    "sample": sample_name, "dependent_variable": outcome,
                    "AR_lags_p": p, "food_lag_horizon": "0-6 fixed", "n": n,
                    "AIC": aic, "BIC": bic, "R2": r2,
                    "BIC_selected": bool(p == best[1]),
                    "selected_p_for_sample_outcome": int(best[1])
                })
    return pd.DataFrame(rows)

def cointegration_diagnostics(df: pd.DataFrame):
    pairs = [
        ("Non-food", "nonfood", "Food and Beverages", "food"),
        ("Core", "core", "Food and Beverages", "food"),
        ("Food and Beverages", "food", "Non-food", "nonfood"),
        ("Non-food (headline-derived)", "nonfood_from_headline", "Food and Beverages", "food"),
    ]
    eg_rows, ardl_rows, grid_rows = [], [], []
    for y_label, y_col, x_label, x_col in pairs:
        ylev = np.log(df[y_col].astype(float))
        xlev = np.log(df[x_col].astype(float))
        for trend in ["c", "ct"]:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                stat, pvalue, crit = coint(ylev, xlev, trend=trend, autolag="aic")
            eg_rows.append({"dependent_level": y_label, "explanatory_level": x_label,
                            "trend_specification": trend, "EG_statistic": float(stat),
                            "EG_pvalue": float(pvalue), "critical_1pct": float(crit[0]),
                            "critical_5pct": float(crit[1]), "critical_10pct": float(crit[2]),
                            "interpretation": "Do not reject no cointegration at 5%" if pvalue >= 0.05 else "Reject no cointegration at 5%"})
        # Compare AIC/BIC lag selection for ARDL levels with seasonal month dummies.
        best = {"aic": None, "bic": None}
        for p in range(1, 7):
            for q in range(1, 7):
                model = ARDL(ylev, lags=p, exog=pd.DataFrame({x_col: xlev}), order=q,
                             trend="c", seasonal=True, period=12).fit()
                item = {"p": p, "q": q, "aic": float(model.aic), "bic": float(model.bic), "model": model}
                grid_rows.append({"dependent_level": y_label, "explanatory_level": x_label,
                                  "AR_lags_p": p, "distributed_lags_q": q,
                                  "AIC": float(model.aic), "BIC": float(model.bic)})
                for criterion in ["aic", "bic"]:
                    if best[criterion] is None or item[criterion] < best[criterion][criterion]:
                        best[criterion] = item
        for criterion in ["aic", "bic"]:
            item = best[criterion]
            uecm = UECM.from_ardl(item["model"].model).fit()
            bt = uecm.bounds_test(case=3)
            ardl_rows.append({
                "dependent_level": y_label, "explanatory_level": x_label,
                "selection_criterion": criterion.upper(), "selected_p": item["p"], "selected_q": item["q"],
                "AIC": item["aic"], "BIC": item["bic"], "bounds_F": float(bt.stat),
                "bounds_p_I0": float(bt.p_values["lower"]), "bounds_p_I1": float(bt.p_values["upper"]),
                "interpretation_at_5pct": (
                    "Evidence against no cointegration (F above upper bound)" if bt.p_values["upper"] < 0.05
                    else "No evidence of cointegration (F below lower bound)" if bt.p_values["lower"] > 0.05
                    else "Inconclusive bounds test"
                ),
                "caution": "Exploratory lag-selection sensitivity; not a final ECM estimate."
            })
    return pd.DataFrame(eg_rows), pd.DataFrame(ardl_rows), pd.DataFrame(grid_rows)



def seasonal_level_cointegration_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    """Engle-Granger tests on log levels after deterministic month-of-year adjustment.

    This is a sensitivity calculation, not a substitute for an official X-13 SA series.
    """
    D = month_dummies(df.index)
    adjusted = {}
    for label, col in [("Food", "food"), ("Non-food", "nonfood"), ("Core", "core")]:
        y = np.log(df[col].astype(float))
        tmp = pd.concat([y.rename("y"), D], axis=1).dropna()
        X = sm.add_constant(tmp[D.columns], has_constant="add")
        fit = sm.OLS(tmp.y, X).fit()
        # Remove fitted month effects only; preserve the intercept and long-run trend.
        adjusted[label] = tmp.y - (fit.predict(X) - fit.params["const"])
    rows = []
    for y_label, x_label in [("Non-food", "Food"), ("Core", "Food")]:
        for trend in ["c", "ct"]:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                stat, pvalue, crit = coint(adjusted[y_label], adjusted[x_label], trend=trend, autolag="aic")
            rows.append({"dependent_level": y_label, "explanatory_level": x_label,
                         "seasonal_adjustment": "calendar-month fixed effects on log levels",
                         "trend_specification": trend, "EG_statistic": float(stat),
                         "EG_pvalue": float(pvalue), "critical_5pct": float(crit[1]),
                         "interpretation": "Do not reject no cointegration at 5%" if pvalue >= 0.05 else "Reject no cointegration at 5%",
                         "caution": "Deterministic monthly adjustment sensitivity; not official X-13 adjustment."})
    return pd.DataFrame(rows)

def short_run_screen(df: pd.DataFrame):
    """Exploratory short-run distributed-lag screens; not final estimates."""
    out_rows = []
    month_all = month_dummies(df.index)
    samples = {
        "Full 2014-2025": df.index,
        "FIT from 2016-04": df.index[df.index >= pd.Period("2016-04", freq="M")],
        "Exclude Apr-May 2020": df.index[~df.index.astype(str).isin(cfg.COLLECTION_GAP_MONTHS)],
    }
    for sample_name, idx in samples.items():
        sub = df.loc[idx]
        D = month_dummies(sub.index)
        for outcome, ycol, xcol in [("Non-food", "infl_nonfood_log", "infl_food_log"),
                                    ("Core", "infl_core_log", "infl_food_log"),
                                    ("Food reverse direction", "infl_food_log", "infl_nonfood_log")]:
            y = sub[ycol].astype(float)
            x = sub[xcol].astype(float)
            # A fixed six-month lag window is a transparent screening horizon; current month is
            # estimated separately from lagged months 1-6.
            X = pd.DataFrame({"const": 1.0, "y_lag1": y.shift(1)}, index=sub.index)
            for j in range(0, 7):
                X[f"x_lag{j}"] = x.shift(j)
            X = pd.concat([X, D], axis=1)
            z = pd.concat([y.rename("y"), X], axis=1).dropna()
            ols = sm.OLS(z.y, z.drop(columns="y")).fit()
            hac = ols.get_robustcov_results(cov_type="HAC", maxlags=6)
            names = list(ols.params.index)
            lag_names = [f"x_lag{j}" for j in range(1, 7)]
            ixlag = [names.index(v) for v in lag_names]
            R = np.zeros((len(ixlag), len(names)))
            for r, c in enumerate(ixlag):
                R[r, c] = 1.0
            lag_test = hac.f_test(R)
            i0 = names.index("x_lag0")
            bg = acorr_breusch_godfrey(ols, nlags=6)
            arch = het_arch(ols.resid, nlags=6)
            bp = het_breuschpagan(ols.resid, ols.model.exog)
            out_rows.append({
                "sample": sample_name, "dependent_variable": outcome,
                "n": int(ols.nobs), "AR_lag_p": 1, "food_lags_included": "0-6",
                "R2": float(ols.rsquared), "AIC": float(ols.aic), "BIC": float(ols.bic),
                "same_month_food_coef": float(hac.params[i0]), "same_month_food_p_HAC6": float(hac.pvalues[i0]),
                "food_lags_1_to_6_joint_F_HAC6": float(lag_test.fvalue),
                "food_lags_1_to_6_joint_p_HAC6": float(lag_test.pvalue),
                "BG_LM_p_6lags": float(bg[1]), "ARCH_LM_p_6lags": float(arch[1]),
                "Breusch_Pagan_p": float(bp[1]),
                "warning": "Exploratory fixed-lag screen, not the final selected model; do not cite as final evidence."
            })
    return pd.DataFrame(out_rows)


def write_memo(stationarity, seasonality, eg, bounds, screen, boot, za, lag_selection, sa_coint):
    nf = bounds[(bounds.dependent_level == "Non-food") & (bounds.explanatory_level == "Food and Beverages")]
    nf_eg = eg[(eg.dependent_level == "Non-food") & (eg.explanatory_level == "Food and Beverages")]
    nf_screen = screen[(screen.dependent_variable == "Non-food") & (screen["sample"] == "Full 2014-2025")].iloc[0]
    lines = [
        "# Econometric design review — pre-estimation milestone",
        "",
        "**Status:** diagnostic and specification-design stage only. No final spillover model is frozen or reported.",
        "**Data:** authentic MoSPI CPI (2012=100), All-India Combined, January 2014–December 2025; 144 monthly observations.",
        "",
        "## 1. Main recommendation",
        "Use a short-run dynamic distributed-lag regression in monthly log changes as the primary spillover test, with calendar-month effects and HAC inference. Keep year-on-year inflation primarily for stylised facts and visual communication. Do not estimate or interpret a long-run error-correction multiplier unless a cointegrating relationship is supported by the data and survives reasonable lag specifications.",
        "",
        "## 2. Why monthly log changes are preferred for the primary regression",
        "Year-on-year rates compare each month with the same month one year earlier. Adjacent YoY observations share 11 of 12 monthly price changes, which induces overlapping-window dependence and obscures the timing of a monthly transmission mechanism. Monthly log changes are non-overlapping one-month price changes and are therefore the more natural outcome for short-run dynamic spillover analysis. YoY rates remain useful for descriptive summaries and comparison with RBI stylised facts.",
        "",
        "## 3. Stationarity and cointegration evidence",
        "The log CPI level series are not rejected as unit-root processes by the ADF tests in this sample. First differences in logs are substantially more stationary; the non-food ADF result is relatively borderline, while KPSS does not reject stationarity of the monthly non-food log-change series at conventional levels. After removing calendar-month fixed effects, the monthly log-change series are strongly stationary by ADF and do not reject stationarity by KPSS. This supports the month-effects dynamic model, while preserving a transparent note on the borderline unadjusted non-food result.",
        f"One-break Zivot-Andrews checks: {za[['series','ZA_regression','ZA_statistic','ZA_pvalue','estimated_break_month']].to_dict(orient='records')}. The tests do not reject a unit root allowing a single break at conventional levels; estimated break dates are search outcomes, not established economic break dates.",
        f"Engle–Granger food/non-food results: {nf_eg[['trend_specification','EG_statistic','EG_pvalue']].to_dict(orient='records')}.",
        f"ARDL bounds results for non-food dependent on food: {nf[['selection_criterion','selected_p','selected_q','bounds_F','bounds_p_I0','bounds_p_I1','interpretation_at_5pct']].to_dict(orient='records')}.",
        "Across AIC/BIC-selected short-lag ARDL models, the food-to-non-food level relationship does not pass the upper critical bound. The reverse-direction bounds result is sensitive to AIC versus BIC selection, so it is not a robust basis for a long-run relation. Calendar-month-adjusted log-level Engle-Granger sensitivities also do not reject no cointegration at 5% (see the seasonal cointegration table). This differs from the RBI 2024 paper's reported bounds-test evidence, but the sample window, data construction and seasonal adjustment differ. Do not force an ECM just to imitate the published specification.",
        "",
        "## 4. Seasonality",
        f"Calendar-month indicators are jointly relevant for monthly log inflation. Results: {seasonality[['series','month_effects_joint_F','month_effects_joint_pvalue_HAC6','raw_sd_pp','seasonal_adjusted_sd_pp']].to_dict(orient='records')}.",
        "For transparent descriptive comparisons, report both unadjusted monthly log inflation and a deterministic calendar-month-adjusted series obtained by removing estimated month-of-year effects. This is an OLS fixed-seasonality adjustment, not an official X-13 seasonal adjustment. In the regression, include 11 month-of-year indicators directly rather than relying only on a pre-adjusted series.",
        "",
        "## 5. Primary specification to take forward for formal estimation",
        r"\[m_t^{NF}=\alpha+\sum_{i=1}^{p}\rho_i m_{t-i}^{NF}+\sum_{j=0}^{6}\beta_j m_{t-j}^{F}+\sum_{k=2}^{12}\gamma_k D_{k,t}+\varepsilon_t\]",
        "where m is 100 times the monthly log change in the CPI index. Include the current-month food change to capture same-month co-movement, but make the primary spillover test the joint null H0: beta_1 = ... = beta_6 = 0. The beta_0 coefficient alone is contemporaneous association, not evidence that food prices lead non-food prices. Use HAC/Newey-West standard errors with a pre-specified lag length (six months in the first pass; report a 12-month HAC sensitivity). Select p parsimoniously using BIC over a limited range (1-6), while keeping the food lag horizon fixed at six months for the main joint test. The BIC lag-selection table is saved separately; in the full sample it selects one own-lag for the non-food equation. A 12-month food-lag horizon can be a robustness check, not an opportunity for specification shopping.",
        "",
        "## 6. Outcome definitions and robustness",
        "Primary outcome: group-built non-food CPI inflation, using all five non-food groups and retaining Fuel and Light. Robustness outcome: core inflation, excluding both Food and Beverages and Fuel and Light. Compare with the headline-derived non-food index as a construction sensitivity. Alternative food measure: CFPI. Do not use domestic Fuel and Light CPI as an ordinary control in the primary non-food regression because it is already part of the dependent basket.",
        "",
        "## 7. Sample and event treatment",
        "Primary sample: Jan 2014–Dec 2025. Robustness: FIT period from Apr 2016, and exclusion of Apr–May 2020. The two 2020 group indices are retained because index values are published; the collection-gap flag records the interruption in published headline YoY compilation. Do not interpolate or silently delete source data.",
        "",
        "## 8. Diagnostic requirements for the formal model",
        "Report BG serial-correlation tests, ARCH-LM, heteroskedasticity tests, residual ACF/PACF, parameter stability/CUSUM where appropriate, influence checks, and HAC standard errors. HAC inference does not cure omitted variables or misspecification. Consider GARCH only if residual ARCH is detected and if the research question benefits from conditional-volatility modelling; it is not automatically required.",
        "",
        "## 9. Exploratory screen (not final results)",
        f"For the full sample, the fixed AR(1)+food lags 0–6+month-effects screening model gives same-month food coefficient {nf_screen.same_month_food_coef:.4f} (HAC p={nf_screen.same_month_food_p_HAC6:.4f}) and joint p-value for lagged food terms 1–6 of {nf_screen.food_lags_1_to_6_joint_p_HAC6:.4f}. This is not the final model and should not be presented as a confirmed research finding. It suggests distinguishing contemporaneous co-movement from delayed spillover is essential.",
        "",
        "## 10. Decisions still required before the formal regression",
        "1. Confirm that the group-built non-food series remains the primary outcome after comparing its difference from headline-derived non-food CPI.",
        "2. Decide whether to add international crude oil and INR/USD changes as a separate extended model; do not add repo rate to the baseline because policy rates respond endogenously to inflation.",
        "3. Keep the first formal model parsimonious, then add external controls only if their source, frequency and transformations are verified.",
        "4. Do not claim causality; the design estimates dynamic conditional associations / predictive spillovers.",
        "",
        "## BIC own-lag selection (food lags fixed at 0-6)",
        lag_selection[lag_selection.BIC_selected][["sample","dependent_variable","AR_lags_p","food_lag_horizon","BIC","n"]].to_string(index=False),
        "",
        "## Calendar-adjusted level cointegration sensitivity",
        sa_coint.to_string(index=False),
        "",
        "## Bootstrap sensitivity",
        pd.DataFrame(boot).round(4).to_string(index=False),
        "",
        "## Reproducibility",
        "All tables are generated by `src/econometric_design_diagnostics.py`. Review `outputs/tables/` before using values in the report."
    ]
    (DOCS / "econometric_design_review.md").write_text("\n".join(lines) + "\n")


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    df = load_data()
    st = stationarity_table(df)
    sea, months, adj = seasonal_analysis(df)
    st = pd.concat([st, adjusted_series_stationarity(adj)], ignore_index=True)
    st.to_csv(TABLES / "econometric_stationarity_tests.csv", index=False, float_format="%.8f")
    za = break_aware_unit_root_tests(df)
    za.to_csv(TABLES / "econometric_zivot_andrews_tests.csv", index=False, float_format="%.8f")
    sea.to_csv(TABLES / "econometric_seasonality_tests.csv", index=False, float_format="%.8f")
    months.to_csv(TABLES / "econometric_monthly_seasonal_pattern.csv", index=False, float_format="%.8f")
    adj.to_csv(TABLES / "seasonally_adjusted_monthly_inflation.csv", index_label="date", float_format="%.8f")
    boot = []
    paired = adj[["Food and Beverages", "Non-food"]].dropna()
    for block in [6, 12, 18]:
        boot.append(moving_block_bootstrap_sd_diff(paired.iloc[:, 0], paired.iloc[:, 1], block))
    pd.DataFrame(boot).to_csv(TABLES / "seasonal_adjusted_volatility_bootstrap_sensitivity.csv", index=False, float_format="%.8f")
    eg, bounds, grid = cointegration_diagnostics(df)
    eg.to_csv(TABLES / "econometric_engle_granger_tests.csv", index=False, float_format="%.8f")
    bounds.to_csv(TABLES / "econometric_ardl_bounds_sensitivity.csv", index=False, float_format="%.8f")
    sa_coint = seasonal_level_cointegration_sensitivity(df)
    sa_coint.to_csv(TABLES / "econometric_cointegration_seasonal_sensitivity.csv", index=False, float_format="%.8f")
    grid.to_csv(TABLES / "econometric_ardl_lag_grid.csv", index=False, float_format="%.8f")
    screen = short_run_screen(df)
    screen.to_csv(TABLES / "econometric_short_run_screen_exploratory.csv", index=False, float_format="%.8f")
    lag_selection = short_run_lag_selection(df)
    lag_selection.to_csv(TABLES / "econometric_short_run_BIC_lag_selection.csv", index=False, float_format="%.8f")
    write_memo(st, sea, eg, bounds, screen, boot, za, lag_selection, sa_coint)
    print("ECONOMETRIC DESIGN DIAGNOSTICS COMPLETE")
    print(f"Sample: {df.index.min()} to {df.index.max()} ({len(df)} observations)")
    print("Stationarity, seasonality, cointegration and exploratory short-run screening tables written.")
    print(f"Memo: {DOCS / 'econometric_design_review.md'}")
    print("No final spillover regression was estimated.")


if __name__ == "__main__":
    main()
