"""Build the complete monthly analytical dataset from authentic MoSPI CPI indices.

Run from project root:
    python src/build_dataset.py

The processed file preserves all raw months (Jan-2013 to Dec-2025). YoY rates
therefore begin in Jan-2014; one-month rates begin in Feb-2013.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg


def load_raw(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    need = ["date", "headline"] + list(cfg.WEIGHTS)
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise ValueError(f"Raw file is missing columns: {missing}")
    parsed = pd.to_datetime(df["date"], errors="coerce")
    if parsed.isna().any():
        bad = df.loc[parsed.isna(), "date"].tolist()[:10]
        raise ValueError(f"Invalid date values: {bad}")
    df["date"] = parsed.dt.to_period("M")
    for col in ["headline"] + list(cfg.WEIGHTS) + (["cfpi"] if "cfpi" in df.columns else []):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "headline_yoy_published" in df.columns:
        df["headline_yoy_published"] = pd.to_numeric(df["headline_yoy_published"], errors="coerce")
    return df.sort_values("date").set_index("date")


def check_raw(df, start, end):
    problems, notes = [], []
    if df.index.duplicated().any():
        dups = [str(p) for p in df.index[df.index.duplicated()]]
        problems.append(f"Duplicate months: {dups}")
    expected = pd.period_range(start, end, freq="M")
    absent = expected.difference(df.index)
    if len(absent):
        problems.append(f"Missing months: {[str(p) for p in absent]}")
    extra = df.index.difference(expected)
    if len(extra):
        notes.append(f"{len(extra)} months outside {start}..{end} will be dropped.")
    cols = ["headline"] + list(cfg.WEIGHTS) + (["cfpi"] if "cfpi" in df.columns else [])
    nulls = df[cols].isna().sum()
    if nulls.any():
        problems.append(f"Missing values: {nulls[nulls > 0].to_dict()}")
    if (df[cols] <= 0).any().any():
        problems.append("Non-positive index values found.")
    if abs(sum(cfg.WEIGHTS.values()) - 100) > 0.01:
        problems.append("Group weights in config do not sum to 100.")
    if abs(sum(cfg.FOOD_SUBGROUP_WEIGHTS.values()) - cfg.WEIGHTS["food_bev"]) > 0.01:
        problems.append("Food subgroup weights do not sum to the published Food & Beverages weight.")
    if "headline_yoy_published" in df.columns:
        missing_pub = int(df["headline_yoy_published"].isna().sum())
        if missing_pub:
            notes.append(f"{missing_pub} published headline YoY values are blank; expected Jan-Dec 2013 warm-up plus documented Apr-May 2020 collection gaps.")
    return problems, notes


def build(df, weights=None, food=None, fuel=None):
    """Construct weighted indices, inflation rates, contributions and event flags."""
    weights = weights or cfg.WEIGHTS
    food = food or cfg.FOOD
    fuel = fuel or cfg.FUEL
    groups = list(weights)
    w = pd.Series(weights, dtype=float) / 100.0
    keep = ["headline"] + groups
    for optional in ["cfpi", "headline_yoy_published"]:
        if optional in df.columns:
            keep.append(optional)
    out = df[keep].copy()

    out["headline_rebuilt"] = (out[groups] * w).sum(axis=1)
    out["rebuild_error"] = out["headline_rebuilt"] - out["headline"]
    nonfood_g = [g for g in groups if g != food]
    core_g = [g for g in groups if g not in (food, fuel)]
    out["food"] = out[food]
    out["nonfood"] = (out[nonfood_g] * w[nonfood_g]).sum(axis=1) / w[nonfood_g].sum()
    out["nonfood_from_headline"] = (out["headline"] - w[food] * out[food]) / (1 - w[food])
    out["core"] = (out[core_g] * w[core_g]).sum(axis=1) / w[core_g].sum()

    inflation_series = ["headline", "food", "nonfood", "core", "nonfood_from_headline"]
    if "cfpi" in out.columns:
        inflation_series.append("cfpi")
    for name in inflation_series:
        s = out[name]
        out[f"infl_{name}_yoy"] = (s / s.shift(12) - 1) * 100
        out[f"infl_{name}_mom"] = (s / s.shift(1) - 1) * 100
        out[f"infl_{name}_log"] = 100 * np.log(s).diff()

    # Approximate fixed-weight group contribution to headline YoY inflation.
    for g in groups:
        eff_w = w[g] * out[g].shift(12) / out["headline_rebuilt"].shift(12)
        yoy_g = (out[g] / out[g].shift(12) - 1) * 100
        out[f"contrib_{g}_yoy"] = eff_w * yoy_g
    out["contrib_food_bev_yoy"] = out[f"contrib_{food}_yoy"]

    out["flag_collection_gap"] = out.index.astype(str).isin(cfg.COLLECTION_GAP_MONTHS).astype(int)
    # April–May 2020 full CPI index levels use the later MoSPI business-continuity
    # reconstruction; at least some components are explicitly imputed in both months.
    out["flag_covid_imputed_series_month"] = out.index.astype(str).isin(["2020-04", "2020-05"]).astype(int)
    out["flag_covid_pulse"] = out.index.astype(str).isin(cfg.COVID_PULSE_MONTHS).astype(int)
    out["flag_june_2013_housing_step"] = out.index.astype(str).isin(cfg.JUNE_2013_PULSE_MONTHS).astype(int)
    for month in cfg.JUNE_2013_PULSE_MONTHS:
        out[f"pulse_{month.replace('-', '_')}"] = (out.index.astype(str) == month).astype(int)
    for month in cfg.COVID_PULSE_MONTHS:
        out[f"pulse_{month.replace('-', '_')}"] = (out.index.astype(str) == month).astype(int)
    out["flag_post_covid_2021_onward"] = (out.index >= pd.Period(cfg.POST_COVID_START, freq="M")).astype(int)
    out["flag_fit_period"] = (out.index >= pd.Period(cfg.FIT_START, freq="M")).astype(int)
    return out


def validation_report(out, tol, groups):
    ok = True
    lines = ["VALIDATION REPORT — AUTHENTIC MoSPI CPI SERIES"]
    lines.append(f"Rows in processed dataset: {len(out)} ({out.index.min()} to {out.index.max()})")
    lines.append(f"YoY analysis window: {cfg.YOY_ANALYSIS_START} to {cfg.YOY_ANALYSIS_END}; MoM analysis window: {cfg.MOM_ANALYSIS_START} to {cfg.MOM_ANALYSIS_END}")
    yoy_cols = [c for c in out.columns if c.endswith("_yoy") and c.startswith("infl_")]
    yoy_window = out.loc[cfg.YOY_ANALYSIS_START:cfg.YOY_ANALYSIS_END, yoy_cols]
    mom_cols = [c for c in out.columns if c.endswith("_mom") and c.startswith("infl_")]
    mom_window = out.loc[cfg.MOM_ANALYSIS_START:cfg.MOM_ANALYSIS_END, mom_cols]
    null_yoy = int(yoy_window.isna().sum().sum())
    null_mom = int(mom_window.isna().sum().sum())
    lines.append(f"Missing derived YoY values inside YoY window: {null_yoy}")
    lines.append(f"Missing derived MoM values inside MoM window: {null_mom}")
    if null_yoy or null_mom:
        ok = False
        lines.append("  FAIL: unexpected missing derived inflation values")
    lines.append(f"Expected warm-up: 12 raw months for YoY; 1 raw month for MoM")

    err = out["rebuild_error"].abs()
    lines.append(f"Headline vs weighted group sum: max abs gap {err.max():.3f}, mean {err.mean():.3f} index points")
    bad = out.index[err > tol]
    if len(bad):
        ok = False
        lines.append(f"  FAIL: {len(bad)} months exceed tolerance {tol}: {[str(x) for x in bad][:10]}")
    else:
        lines.append(f"  OK: all months within tolerance {tol}")

    lvl_gap = (out["nonfood"] - out["nonfood_from_headline"]).abs()
    mom_gap = (out["infl_nonfood_mom"] - out["infl_nonfood_from_headline_mom"]).abs()
    lines.append(f"Non-food group-built vs headline-built: max level gap {lvl_gap.max():.3f}; max MoM inflation gap {mom_gap.loc[cfg.MOM_ANALYSIS_START:].max():.3f} pp")

    contrib_cols = [f"contrib_{g}_yoy" for g in groups]
    ident = (out[contrib_cols].sum(axis=1) - out["infl_headline_yoy"]).abs()
    lines.append(f"Approx. group contribution identity max gap: {ident.loc[cfg.YOY_ANALYSIS_START:].max():.3f} pp")

    if "headline_yoy_published" in out.columns:
        d = (out.loc[cfg.YOY_ANALYSIS_START:, "infl_headline_yoy"] - out.loc[cfg.YOY_ANALYSIS_START:, "headline_yoy_published"]).abs().dropna()
        lines.append(f"Computed vs published headline YoY: n={len(d)}, max gap {d.max():.3f} pp, mean {d.mean():.3f} pp")
        if len(d) == 0 or d.max() > 0.15:
            ok = False
            lines.append("  FAIL: gap above 0.15 pp or no published comparisons.")
        else:
            lines.append("  OK: computed values agree within rounding tolerance.")
        yoy_slice = out.loc[cfg.YOY_ANALYSIS_START:]
        missing_pub = yoy_slice["headline_yoy_published"].isna()
        lines.append(f"Published headline YoY gaps within YoY window: {list(yoy_slice.index[missing_pub])}")

    lines.append(f"CFPI included: {'yes' if 'infl_cfpi_yoy' in out.columns else 'no'}")
    lines.append(f"COVID pulse months flagged: {int(out['flag_covid_pulse'].sum())}")
    lines.append(f"Collection-gap months flagged: {int(out['flag_collection_gap'].sum())}")
    lines.append(f"Months containing MoSPI-imputed CPI components: {list(out.index[out['flag_covid_imputed_series_month'].eq(1)].astype(str))}")
    lines.append("OVERALL: " + ("PASS" if ok else "FAIL"))
    return lines, ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", default=str(cfg.RAW_FILE))
    ap.add_argument("--out", default=str(cfg.OUT_FILE))
    ap.add_argument("--report", default=str(cfg.REPORT_FILE))
    args = ap.parse_args(argv)
    if not Path(args.raw).exists():
        print(f"Raw file not found: {args.raw}")
        return 1
    df = load_raw(args.raw)
    problems, notes = check_raw(df, cfg.RAW_START, cfg.RAW_END)
    for note in notes:
        print("NOTE:", note)
    if problems:
        print("RAW DATA PROBLEMS:")
        for problem in problems:
            print(" -", problem)
        return 1
    df = df.loc[cfg.RAW_START:cfg.RAW_END]
    out = build(df)
    lines, ok = validation_report(out, cfg.TOLERANCE, list(cfg.WEIGHTS))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    save = out.copy()
    save.index = save.index.astype(str)
    save.index.name = "date"
    save.to_csv(args.out, float_format="%.8f")
    Path(args.report).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nSaved dataset to {args.out}\nSaved report to {args.report}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
