"""Corrected descriptive and stylised-facts analysis.

Key design choices:
- YoY moments are reported descriptively only (overlapping windows invalidate iid p-values).
- Formal volatility/moment comparisons use monthly log changes from STL-adjusted log CPI levels.
- Paired stationary bootstrap preserves contemporaneous dependence; expected block length is
  selected using the corrected Politis-White plug-in procedure (with transparent sensitivity).
- Food subgroup and non-food group comparisons use official Combined CPI subgroup indices.
- Covariance variance decomposition is accounting/statistical, not causal.

Run after `python src/build_dataset.py`:
    python src/corrected_descriptive_analysis.py
"""
from __future__ import annotations

import sys
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.seasonal import STL

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg

TABLES = cfg.ROOT / "outputs" / "tables"
FIGS = cfg.ROOT / "outputs" / "figures"
DOCS = cfg.ROOT / "documentation"
SEED = 20261114
BOOT_REPS = 4999

FOOD_SUBGROUP_LABELS = list(cfg.FOOD_SUBGROUP_WEIGHTS)
SOURCE_GROUP_TO_COL = {
    "Food and Beverages": "food_bev",
    "Pan, Tobacco and Intoxicants": "pan_tobacco",
    "Clothing and Footwear": "clothing",
    "Housing": "housing",
    "Fuel and Light": "fuel_light",
    "Miscellaneous": "misc",
}
NONFOOD_GROUP_LABELS = {
    "pan_tobacco": "Pan, Tobacco and Intoxicants",
    "clothing": "Clothing and Footwear",
    "housing": "Housing",
    "fuel_light": "Fuel and Light",
    "misc": "Miscellaneous",
}


def load_processed() -> pd.DataFrame:
    path = cfg.OUT_FILE
    if not path.exists():
        raise FileNotFoundError("Run python src/build_dataset.py first")
    df = pd.read_csv(path, parse_dates=False)
    df["date"] = pd.PeriodIndex(df["date"], freq="M")
    return df.set_index("date").sort_index()


def load_source_export() -> pd.DataFrame:
    path = cfg.SOURCE_EXPORT
    if not path.exists():
        raise FileNotFoundError(f"Missing row-level source export: {path}")
    src = pd.read_csv(path)
    src = src[(src["baseyear"] == 2012) & (src["state"] == "All India") & (src["sector"] == "Combined")].copy()
    src["date"] = pd.PeriodIndex(src["year"].astype(int).astype(str) + "-" + src["month_code"].astype(int).astype(str).str.zfill(2), freq="M")
    src["index"] = pd.to_numeric(src["index"], errors="coerce")
    return src


def load_food_subgroups(src: pd.DataFrame) -> pd.DataFrame:
    f = src[(src["group"] == "Food and Beverages") & src["subgroup"].isin(FOOD_SUBGROUP_LABELS)].copy()
    if f.duplicated(["date", "subgroup"]).any():
        raise ValueError("Duplicate food subgroup/date records in source export")
    wide = f.pivot(index="date", columns="subgroup", values="index").sort_index()
    expected = pd.period_range(cfg.RAW_START, cfg.RAW_END, freq="M")
    wide = wide.reindex(expected)
    missing = wide.isna().sum()
    if missing.any():
        raise ValueError(f"Missing food subgroup observations: {missing[missing > 0].to_dict()}")
    return wide[FOOD_SUBGROUP_LABELS]


def stl_adjust_log_index(index: pd.Series, period: int = 12) -> tuple[pd.Series, pd.Series, pd.Series]:
    """STL-adjust log CPI level, then difference adjusted log level."""
    x = pd.to_numeric(index, errors="coerce").astype(float)
    if x.isna().any() or (x <= 0).any():
        raise ValueError("STL input index must be complete and strictly positive")
    logx = np.log(x)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = STL(logx, period=period, robust=True).fit()
    log_sa = logx - fit.seasonal
    mom_sa = 100.0 * log_sa.diff()
    return log_sa, mom_sa, fit.seasonal


def moment_row(label: str, s: pd.Series, frequency: str, note: str) -> dict:
    x = pd.Series(s).dropna().astype(float)
    return {
        "series": label,
        "frequency": frequency,
        "n": int(len(x)),
        "mean": float(x.mean()),
        "median": float(x.median()),
        "variance": float(x.var(ddof=1)),
        "sd": float(x.std(ddof=1)),
        "min": float(x.min()),
        "max": float(x.max()),
        "skewness": float(stats.skew(x, bias=False)) if len(x) > 2 else np.nan,
        "excess_kurtosis": float(stats.kurtosis(x, fisher=True, bias=False)) if len(x) > 3 else np.nan,
        "acf1": float(x.autocorr(1)) if len(x) > 2 else np.nan,
        "inference_note": note,
    }


def _autocovariance(x: np.ndarray, lag: int) -> float:
    z = x - np.mean(x)
    return float(np.dot(z[lag:], z[: len(z) - lag]) / len(z)) if lag else float(np.dot(z, z) / len(z))


def politis_white_stationary_block_length(series: pd.Series | np.ndarray) -> dict:
    """Politis-White/Patton-Politis-White stationary-bootstrap block length.

    This follows the published/arch implementation structure: lag-dependent
    autocorrelation normalization for selecting the truncation point, flat-top
    lag window, and the corrected stationary-bootstrap variance constant
    d_SB = 2 * (long_run_variance_estimate ** 2). The raw estimate is rounded and bounded below at 2 and above by
    ceil(min(3*sqrt(n), n/3)); these are documented local finite-sample modifications.

    Reference implementation details: arch.bootstrap.optimal_block_length
    documentation/source; references Politis & White (2004) and Patton,
    Politis & White (2009).
    """
    x = np.asarray(pd.Series(series).dropna(), dtype=float)
    n = len(x)
    if n < 30:
        return {"n": n, "m": np.nan, "M": np.nan, "threshold": np.nan,
                "block_length_raw": np.nan, "block_length": max(2, min(n // 3, 2)),
                "method": "short-sample fallback (n<30)"}

    eps = x - x.mean()
    b_max = int(np.ceil(min(3.0 * np.sqrt(n), n / 3.0)))
    kn = max(5, int(np.log10(n)))
    m_max = int(np.ceil(np.sqrt(n))) + kn
    threshold = 2.0 * np.sqrt(np.log10(n) / n)
    acov = np.zeros(m_max + 1, dtype=float)
    abs_acorr = np.zeros(m_max + 1, dtype=float)
    opt_m = None

    # Match the maximum-sample-length autocovariance/autocorrelation estimator.
    for lag in range(m_max + 1):
        v1 = float(eps[lag + 1:] @ eps[lag + 1:])
        v2 = float(eps[: -(lag + 1)] @ eps[: -(lag + 1)])
        cross = float(eps[lag:] @ eps[: n - lag])
        acov[lag] = cross / n
        denom = np.sqrt(v1 * v2)
        abs_acorr[lag] = abs(cross) / denom if denom > 0 else 0.0
        if lag >= kn and opt_m is None:
            if np.all(abs_acorr[lag - kn:lag] < threshold):
                opt_m = lag - kn

    m = 2 * max(int(opt_m), 1) if opt_m is not None else m_max
    m = min(m, m_max)
    g = 0.0
    long_run_variance = float(acov[0])
    for lag in range(1, m + 1):
        lam = 1.0 if lag / m <= 0.5 else 2.0 * (1.0 - lag / m)
        g += 2.0 * lam * lag * acov[lag]
        long_run_variance += 2.0 * lam * acov[lag]

    d_sb = 2.0 * long_run_variance ** 2
    if not np.isfinite(d_sb) or d_sb <= 0 or not np.isfinite(g):
        raw = float(n ** (1.0 / 3.0))
        method = "non-finite safeguard (non-positive long-run variance estimate)"
    else:
        raw = float(((2.0 * g ** 2 / d_sb) ** (1.0 / 3.0)) * n ** (1.0 / 3.0))
        method = "Politis-White flat-top; PPW-corrected stationary constant"
        if not np.isfinite(raw):
            raw = 1.0
            method += "; non-finite safeguard to 1 before documented floor"
    block = int(np.clip(round(raw), 2, max(2, b_max)))
    return {"n": n, "kn": kn, "m_max": m_max, "opt_m": opt_m,
            "m": m, "threshold": threshold, "sigma2_long_run": long_run_variance,
            "g_flat_top": g, "block_length_raw": raw, "block_length_max": b_max,
            "block_length": block, "method": method}


def stationary_bootstrap_index_matrix(n: int, expected_block: float, reps: int,
                                      rng: np.random.Generator) -> np.ndarray:
    """Vectorised Politis-Romano stationary-bootstrap indices.

    Each replication has geometric block lengths. When a block continues past the
    final observation, the standard stationary bootstrap wraps the time index.
    Food and non-food use the same index matrix to preserve paired dependence.
    """
    if n < 2 or reps < 1:
        raise ValueError("Need n >= 2 and reps >= 1")
    mean_block = max(1.0, float(expected_block))
    restart_prob = min(1.0, 1.0 / mean_block)
    idx = np.empty((reps, n), dtype=np.int32)
    idx[:, 0] = rng.integers(0, n, size=reps)
    restart = rng.random((reps, n - 1)) < restart_prob
    fresh_start = rng.integers(0, n, size=(reps, n - 1), dtype=np.int32)
    for t in range(1, n):
        idx[:, t] = np.where(restart[:, t - 1], fresh_start[:, t - 1], (idx[:, t - 1] + 1) % n)
    return idx


def bootstrap_paired_moments(x: pd.Series, y: pd.Series, reps: int = BOOT_REPS, seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    pair = pd.concat([x.rename("food"), y.rename("nonfood")], axis=1).dropna()
    xa, ya = pair["food"].to_numpy(float), pair["nonfood"].to_numpy(float)
    b_food = politis_white_stationary_block_length(xa)
    b_nonfood = politis_white_stationary_block_length(ya)
    auto_b = max(b_food["block_length"], b_nonfood["block_length"])

    def stats_vec(a, b_):
        sd_a, sd_b = np.std(a, ddof=1, axis=-1), np.std(b_, ddof=1, axis=-1)
        return np.column_stack([
            sd_a - sd_b,
            np.log(sd_a / sd_b),
            stats.skew(a, axis=-1, bias=False) - stats.skew(b_, axis=-1, bias=False),
            stats.kurtosis(a, axis=-1, fisher=True, bias=False) - stats.kurtosis(b_, axis=-1, fisher=True, bias=False),
        ])

    point = stats_vec(xa[None, :], ya[None, :])[0]
    labels = [
        ("sd_difference_food_minus_nonfood", point[0], "pp"),
        ("log_sd_ratio_food_to_nonfood", point[1], "log ratio"),
        ("skewness_difference_food_minus_nonfood", point[2], "unitless"),
        ("excess_kurtosis_difference_food_minus_nonfood", point[3], "unitless"),
    ]
    all_rows = []
    # The automatic selection is primary; fixed block lengths are pre-declared sensitivity checks.
    block_scenarios = [("Politis-White automatic", auto_b), ("fixed sensitivity", 1),
                       ("fixed sensitivity", 3), ("fixed sensitivity", 6),
                       ("fixed sensitivity", 12), ("fixed sensitivity", 24)]
    for scenario_i, (scenario_name, b) in enumerate(block_scenarios):
        rng = np.random.default_rng(seed + scenario_i)
        index_matrix = stationary_bootstrap_index_matrix(len(xa), b, reps, rng)
        draws = stats_vec(xa[index_matrix], ya[index_matrix])
        for i, (name, estimate, unit) in enumerate(labels):
            finite = draws[:, i][np.isfinite(draws[:, i])]
            lo, hi = np.quantile(finite, [0.025, 0.975])
            count = int(np.sum(finite <= 0))
            p_upper = (count + 1) / (len(finite) + 1)
            all_rows.append({
                "block_selection": scenario_name,
                "statistic": name, "estimate": estimate, "unit": unit,
                "ci_2_5": lo, "ci_97_5": hi,
                "bootstrap_tail_probability_le_zero": p_upper,
                "monte_carlo_resolution": 1 / (len(finite) + 1),
                "replications": len(finite), "seed": seed + scenario_i,
                "expected_block_length": b,
                "block_length_food_auto": b_food["block_length"],
                "block_length_nonfood_auto": b_nonfood["block_length"],
                "resampling": "paired stationary bootstrap; geometric block lengths; common indices",
                "note": "Automatic PPW length is primary; fixed 6/12/24 lengths are sensitivity checks. Standard stationary bootstrap has circular time indexing."
            })
    block_rows = []
    for label, info in [("Food", b_food), ("Non-food", b_nonfood)]:
        block_rows.append({"series": label, **info})
    return pd.DataFrame(all_rows), pd.DataFrame(block_rows)


def build_food_subgroup_indices(src: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    food_sub = load_food_subgroups(src)
    weights = pd.Series(cfg.FOOD_SUBGROUP_WEIGHTS, dtype=float)
    weighted_all = (food_sub * weights).sum(axis=1) / weights.sum()
    exveg_weights = weights.drop(index="Vegetables")
    food_ex_veg = (food_sub[exveg_weights.index] * exveg_weights).sum(axis=1) / exveg_weights.sum()
    idx = pd.DataFrame({
        "food_subgroup_rebuilt": weighted_all,
        "food_beverages_official": food_sub.sum(axis=1) * np.nan,  # filled from processed series later
        "food_ex_vegetables_proxy": food_ex_veg,
        "vegetables": food_sub["Vegetables"],
    }, index=food_sub.index)
    for col in food_sub.columns:
        idx[f"subgroup::{col}"] = food_sub[col]
    weight_table = pd.DataFrame([
        {"subgroup": k, "combined_weight_percent": v,
         "source": cfg.FOOD_SUBGROUP_WEIGHT_SOURCE}
        for k, v in cfg.FOOD_SUBGROUP_WEIGHTS.items()
    ])
    return idx, weight_table


def covariance_variance_decomposition(index_data: pd.DataFrame, groups: list[str], aggregate_map: dict[str, list[str]], freq: str, basis: str = "raw") -> pd.DataFrame:
    """Variance attribution using Cov(component contribution, aggregate change)/Var(total)."""
    w = pd.Series(cfg.WEIGHTS, dtype=float) / 100.0
    rebuilt = sum(index_data[g] * w[g] for g in groups)
    contrib = pd.DataFrame(index=index_data.index)
    if freq == "MoM":
        denominator = rebuilt.shift(1)
        for g in groups:
            contrib[g] = 100 * w[g] * (index_data[g] - index_data[g].shift(1)) / denominator
    elif freq == "YoY":
        denominator = rebuilt.shift(12)
        for g in groups:
            contrib[g] = 100 * w[g] * (index_data[g] - index_data[g].shift(12)) / denominator
    else:
        raise ValueError(freq)
    out_rows = []
    for scheme, mapping in [("six CPI groups", {g: [g] for g in groups}), ("food-fuel-other", aggregate_map)]:
        c = pd.DataFrame(index=contrib.index)
        for name, members in mapping.items():
            c[name] = contrib[members].sum(axis=1, min_count=1)
        c = c.dropna()
        total = c.sum(axis=1)
        vtotal = float(total.var(ddof=1))
        if vtotal <= 0:
            continue
        for name in c.columns:
            cov = float(np.cov(c[name], total, ddof=1)[0, 1])
            out_rows.append({
                "frequency": freq, "basis": basis, "decomposition": scheme, "component": name,
                "component_mean_contribution_pp": float(c[name].mean()),
                "component_variance_pp2": float(c[name].var(ddof=1)),
                "covariance_with_aggregate_pp2": cov,
                "share_of_aggregate_variance_percent": 100 * cov / vtotal,
                "aggregate_variance_pp2": vtotal,
                "n": int(len(c)),
                "interpretation": "Cov(component contribution, aggregate change)/Var(aggregate change); includes cross-covariance; accounting/statistical attribution, not causal."
            })
    return pd.DataFrame(out_rows)


def make_figures(stl_mom: pd.DataFrame, group_stats: pd.DataFrame, subgroup_stats: pd.DataFrame,
                 food_indices: pd.DataFrame, variance_decomp: pd.DataFrame):
    FIGS.mkdir(parents=True, exist_ok=True)
    # Seasonally adjusted MoM series.
    fig, ax = plt.subplots(figsize=(11, 5))
    for label in ["Food and Beverages", "Non-food", "Core"]:
        if label in stl_mom.columns:
            ax.plot(stl_mom.index.to_timestamp(), stl_mom[label], label=label, lw=1.3)
    ax.axhline(0, color="black", lw=.7)
    ax.set(title="Seasonally adjusted monthly log inflation", ylabel="Monthly log change (%)", xlabel="Month")
    ax.grid(alpha=.25); ax.legend(frameon=False); fig.tight_layout()
    fig.savefig(FIGS / "fig_stl_adjusted_mom_food_nonfood.png", dpi=200); plt.close(fig)

    # Non-food groups vs food volatility.
    g = group_stats.sort_values("sd", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.3))
    ax.barh(g["series"], g["sd"])
    ax.set(title="Seasonally adjusted monthly volatility by CPI group", xlabel="Standard deviation (pp)")
    ax.grid(axis="x", alpha=.25); fig.tight_layout()
    fig.savefig(FIGS / "fig_nonfood_groups_volatility.png", dpi=200); plt.close(fig)

    s = subgroup_stats.sort_values("sd", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(s["subgroup"], s["sd"])
    ax.set(title="Seasonally adjusted monthly volatility across food subgroups", xlabel="Standard deviation (pp)")
    ax.grid(axis="x", alpha=.25); fig.tight_layout()
    fig.savefig(FIGS / "fig_food_subgroup_volatility.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    for col, label in [("food_beverages_official", "Official Food and Beverages"),
                       ("food_ex_vegetables_proxy", "Derived food-ex-vegetables proxy"),
                       ("vegetables", "Vegetables subgroup")]:
        ax.plot(food_indices.index.to_timestamp(), food_indices[col], label=label, lw=1.4)
    ax.set(title="Food CPI and food-ex-vegetables proxy (index, 2012=100)", ylabel="Index", xlabel="Month")
    ax.grid(alpha=.25); ax.legend(frameon=False); fig.tight_layout()
    fig.savefig(FIGS / "fig_food_ex_vegetables_proxy.png", dpi=200); plt.close(fig)

    vd = variance_decomp[(variance_decomp["frequency"] == "MoM") & (variance_decomp["basis"] == "STL-adjusted") & (variance_decomp["decomposition"] == "food-fuel-other")]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(vd["component"], vd["share_of_aggregate_variance_percent"])
    ax.axhline(0, color="black", lw=.7)
    ax.set(title="Covariance-aware contribution to reconstructed CPI-change variance",
           ylabel="Share of variance (%)", xlabel="Component")
    ax.grid(axis="y", alpha=.25); fig.tight_layout()
    fig.savefig(FIGS / "fig_covariance_variance_decomposition.png", dpi=200); plt.close(fig)


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    data = load_processed()
    src = load_source_export()
    raw_index = data[["headline", "food", "nonfood", "core", "cfpi", *cfg.WEIGHTS.keys()]].copy()
    # Add source subgroup indices and construct a documented weighted food-ex-vegetables proxy.
    food_index, weight_table = build_food_subgroup_indices(src)
    food_index["food_beverages_official"] = data["food"]
    food_index.to_csv(TABLES / "food_subgroup_indices_and_food_ex_vegetables_proxy.csv", index_label="date", float_format="%.8f")
    weight_table.to_csv(cfg.ROOT / "data" / "raw" / "food_subgroup_combined_weights_2012.csv", index=False)

    # Reconstruct a weighted food index from subgroup indices and compare with the official aggregate.
    food_rebuild_gap = food_index["food_subgroup_rebuilt"] - food_index["food_beverages_official"]
    rebuild_report = [
        "FOOD SUBGROUP AGGREGATION CHECK",
        f"Food subgroup weights sum: {sum(cfg.FOOD_SUBGROUP_WEIGHTS.values()):.2f}% (official Food & Beverages weight {cfg.WEIGHTS['food_bev']:.2f}%)",
        f"Weighted subgroup food index vs official Food & Beverages: mean abs gap {food_rebuild_gap.abs().mean():.4f}; max abs gap {food_rebuild_gap.abs().max():.4f} index points.",
        "The food-ex-vegetables index is a derived fixed-weight proxy from published subgroup indices and official rounded subgroup weights; it is not an independently published MoSPI series."
    ]
    (TABLES / "food_subgroup_aggregation_validation.txt").write_text("\n".join(rebuild_report) + "\n")

    # Extend processed data with derived proxy, using the complete raw source window.
    food_ex_veg = food_index["food_ex_vegetables_proxy"].rename("food_ex_vegetables")
    all_indices = raw_index.join(food_ex_veg)
    group_series = {
        "Food and Beverages": all_indices["food"],
        "Non-food": all_indices["nonfood"],
        "Core": all_indices["core"],
        "Headline": all_indices["headline"],
        "CFPI": all_indices["cfpi"],
        "Pan, Tobacco and Intoxicants": all_indices["pan_tobacco"],
        "Clothing and Footwear": all_indices["clothing"],
        "Housing": all_indices["housing"],
        "Fuel and Light": all_indices["fuel_light"],
        "Miscellaneous": all_indices["misc"],
        "Food ex Vegetables (proxy)": all_indices["food_ex_vegetables"],
    }
    # Add all 12 food subgroups from original source export.
    for subgroup in FOOD_SUBGROUP_LABELS:
        group_series[subgroup] = food_index[f"subgroup::{subgroup}"]

    stl_log_levels = pd.DataFrame(index=data.index)
    stl_mom = pd.DataFrame(index=data.index)
    seasonal_components = pd.DataFrame(index=data.index)
    for label, series in group_series.items():
        log_sa, mom_sa, seasonal = stl_adjust_log_index(series)
        stl_log_levels[label] = log_sa
        stl_mom[label] = mom_sa
        seasonal_components[label] = seasonal
    stl_mom.to_csv(TABLES / "stl_seasonally_adjusted_monthly_inflation.csv", index_label="date", float_format="%.8f")
    stl_log_levels.to_csv(TABLES / "stl_seasonally_adjusted_log_indices.csv", index_label="date", float_format="%.10f")
    seasonal_components.to_csv(TABLES / "stl_seasonal_components_log_index.csv", index_label="date", float_format="%.10f")

    yoy_cols = {
        "Food and Beverages": data["infl_food_yoy"],
        "Non-food": data["infl_nonfood_yoy"],
        "Headline": data["infl_headline_yoy"],
        "Core": data["infl_core_yoy"],
        "CFPI": data["infl_cfpi_yoy"],
    }
    yoy_rows = [moment_row(label, series, "YoY (%)", "Descriptive only: overlapping 12-month windows; do not use iid Jarque-Bera p-values or conventional iid confidence intervals.")
                for label, series in yoy_cols.items()]
    pd.DataFrame(yoy_rows).to_csv(TABLES / "yoy_descriptive_moments_no_iid_inference.csv", index=False, float_format="%.8f")

    mom_rows = [moment_row(label, stl_mom[label], "STL-adjusted MoM log change (%)",
                           "Seasonal adjustment applied to log CPI level using robust STL, period=12, then first-differenced.")
                for label in ["Food and Beverages", "Non-food", "Headline", "Core", "CFPI", "Food ex Vegetables (proxy)"]]
    pd.DataFrame(mom_rows).to_csv(TABLES / "stl_mom_descriptive_moments.csv", index=False, float_format="%.8f")

    # Raw MoM descriptive moments are retained to show the effect of seasonal adjustment.
    raw_mom_rows = []
    for label, col in [("Food and Beverages", "infl_food_log"), ("Non-food", "infl_nonfood_log"),
                       ("Headline", "infl_headline_log"), ("Core", "infl_core_log")]:
        raw_mom_rows.append(moment_row(label, data[col], "Raw MoM log change (%)", "Descriptive only; seasonal calendar pattern remains.") )
    pd.DataFrame(raw_mom_rows).to_csv(TABLES / "raw_mom_descriptive_moments.csv", index=False, float_format="%.8f")

    # Bootstrap inference on the pre-declared H1 statistic and explicitly exploratory H2 retest.
    x = stl_mom["Food and Beverages"].loc[cfg.MOM_ANALYSIS_START:]
    y = stl_mom["Non-food"].loc[cfg.MOM_ANALYSIS_START:]
    boot, block_info = bootstrap_paired_moments(x, y)
    boot.to_csv(TABLES / "stl_mom_paired_stationary_bootstrap.csv", index=False, float_format="%.8f")
    block_info.to_csv(TABLES / "stl_mom_politis_white_block_length.csv", index=False, float_format="%.8f")

    # Food subgroup stylised facts, and non-food group diversification comparison.
    subgroup_rows = []
    for subgroup in FOOD_SUBGROUP_LABELS:
        subgroup_rows.append({"subgroup": subgroup, **moment_row(subgroup, stl_mom[subgroup], "STL-adjusted MoM log change (%)", "Subgroup descriptive result; fixed-weight group aggregation not implied.")})
    subgroup_stats = pd.DataFrame(subgroup_rows)
    subgroup_stats.to_csv(TABLES / "food_subgroup_stylised_facts.csv", index=False, float_format="%.8f")

    group_rows = [{"series": "Food and Beverages", **moment_row("Food and Beverages", stl_mom["Food and Beverages"], "STL-adjusted MoM log change (%)", "Single major CPI group compared with composite non-food basket.") }]
    for g, label in NONFOOD_GROUP_LABELS.items():
        group_rows.append({"series": label, **moment_row(label, stl_mom[label], "STL-adjusted MoM log change (%)", "Individual non-food CPI group; volatility comparison is not a causal comparison.")})
    group_rows.append({"series": "Non-food (weighted composite)", **moment_row("Non-food", stl_mom["Non-food"], "STL-adjusted MoM log change (%)", "Weighted composite of five non-food groups; diversification may reduce aggregate volatility.")})
    group_stats = pd.DataFrame(group_rows)
    group_stats.to_csv(TABLES / "nonfood_group_volatility_comparison.csv", index=False, float_format="%.8f")

    # Correlation matrix on STL-adjusted monthly log inflation only; descriptive association, not causality.
    corr_cols = ["Food and Beverages", "Non-food", "Core", "Headline", "CFPI"]
    stl_mom[corr_cols].loc[cfg.MOM_ANALYSIS_START:].corr().to_csv(TABLES / "stl_mom_correlation_matrix_descriptive_only.csv", float_format="%.8f")

    # Covariance-aware variance decomposition: contribution components covary with aggregate movement.
    main_indices = data[list(cfg.WEIGHTS)].copy()
    aggregate_map = {
        "Food": ["food_bev"],
        "Fuel and Light": ["fuel_light"],
        "Other non-food": [g for g in cfg.WEIGHTS if g not in ("food_bev", "fuel_light")],
    }
    vd_mom_raw = covariance_variance_decomposition(main_indices, list(cfg.WEIGHTS), aggregate_map, "MoM", "raw")
    # For STL basis, reconstruct contributions from seasonally adjusted log-index levels.
    stl_label_map = {
        "food_bev": "Food and Beverages", "pan_tobacco": "Pan, Tobacco and Intoxicants",
        "clothing": "Clothing and Footwear", "housing": "Housing",
        "fuel_light": "Fuel and Light", "misc": "Miscellaneous",
    }
    stl_main = np.exp(stl_log_levels[[stl_label_map[g] for g in cfg.WEIGHTS]].copy())
    stl_main.columns = list(cfg.WEIGHTS)
    vd_mom_stl = covariance_variance_decomposition(stl_main, list(cfg.WEIGHTS), aggregate_map, "MoM", "STL-adjusted")
    vd_yoy = covariance_variance_decomposition(main_indices, list(cfg.WEIGHTS), aggregate_map, "YoY", "raw-overlapping-12m-descriptive")
    variance_decomp = pd.concat([vd_mom_raw, vd_mom_stl, vd_yoy], ignore_index=True)
    variance_decomp.to_csv(TABLES / "covariance_aware_group_variance_decomposition.csv", index=False, float_format="%.8f")

    # A report-friendly concise summary and caveats.
    food_stats = pd.DataFrame([moment_row("Food", x, "STL-adjusted MoM log change (%)", "")]).iloc[0]
    nf_stats = pd.DataFrame([moment_row("Non-food", y, "STL-adjusted MoM log change (%)", "")]).iloc[0]
    h1 = boot.loc[boot["statistic"] == "sd_difference_food_minus_nonfood"].iloc[0]
    h2_skew = boot.loc[boot["statistic"] == "skewness_difference_food_minus_nonfood"].iloc[0]
    h2_kurt = boot.loc[boot["statistic"] == "excess_kurtosis_difference_food_minus_nonfood"].iloc[0]
    summary = [
        "CORRECTED DESCRIPTIVE ANALYSIS — DESCRIPTIVE OUTPUTS ONLY",
        f"MoM sample: {cfg.MOM_ANALYSIS_START} to {cfg.MOM_ANALYSIS_END}; n={len(x.dropna())}.",
        f"YoY descriptive sample: {cfg.YOY_ANALYSIS_START} to {cfg.YOY_ANALYSIS_END}; overlapping windows; moments are descriptive only.",
        f"STL-adjusted MoM SD: Food={food_stats['sd']:.4f} pp; Non-food={nf_stats['sd']:.4f} pp.",
        f"H1 SD difference food-minus-nonfood={h1['estimate']:.4f} pp; 95% stationary-bootstrap CI [{h1['ci_2_5']:.4f}, {h1['ci_97_5']:.4f}], block length={int(h1['expected_block_length'])}.",
        f"H1 log SD ratio={boot.loc[boot.statistic=='log_sd_ratio_food_to_nonfood','estimate'].iloc[0]:.4f} with 95% CI [{boot.loc[boot.statistic=='log_sd_ratio_food_to_nonfood','ci_2_5'].iloc[0]:.4f}, {boot.loc[boot.statistic=='log_sd_ratio_food_to_nonfood','ci_97_5'].iloc[0]:.4f}].",
        f"Exploratory H2 MoM skewness difference={h2_skew['estimate']:.4f}, CI [{h2_skew['ci_2_5']:.4f}, {h2_skew['ci_97_5']:.4f}]; excess-kurtosis difference={h2_kurt['estimate']:.4f}, CI [{h2_kurt['ci_2_5']:.4f}, {h2_kurt['ci_97_5']:.4f}]. H2 remains retired as confirmatory.",
        f"Weighted subgroup food index max absolute gap from official Food & Beverages: {food_rebuild_gap.abs().max():.4f} index points.",
        "The food-ex-vegetables measure is a derived weighted subgroup proxy, not an official MoSPI series; compare cautiously against the official group index.",
        "YoY Jarque-Bera p-values, iid YoY correlation inference and circular YoY bootstrap outputs are deprecated and must not be cited as inferential evidence.",
        "The covariance decomposition assigns aggregate variance using Cov(component contribution, total contribution)/Var(total contribution); this includes cross-covariances and is not causal.",
    ]
    (TABLES / "corrected_descriptive_summary.txt").write_text("\n".join(summary) + "\n")

    make_figures(stl_mom, group_stats, subgroup_stats, food_index, variance_decomp)
    print("CORRECTED DESCRIPTIVE ANALYSIS COMPLETE")
    print(f"MoM sample: {cfg.MOM_ANALYSIS_START} to {cfg.MOM_ANALYSIS_END}; n={len(x.dropna())}")
    print(f"STL-adjusted SD food={food_stats['sd']:.4f}; non-food={nf_stats['sd']:.4f}; H1 diff={h1['estimate']:.4f}")
    print("Created: STL monthly stats, paired stationary-bootstrap CIs, subgroup comparisons, food-ex-vegetables proxy, covariance decomposition.")
    print("This script produces descriptive outputs only; run src/run_v33_estimations.py in forward, core and reverse batches for the current v3.3 econometric models.")


if __name__ == "__main__":
    main()
