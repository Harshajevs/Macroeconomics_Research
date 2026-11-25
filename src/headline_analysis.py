"""Headline-CPI checks and stylized facts from the OFFICIAL MoSPI time series.

Uses the All-India Combined headline series (General CPI, base 2012=100). For April–May
2020, the index levels in the continuous historical series reflect MoSPI/NSO's later
business-continuity reconstruction with imputed components; contemporaneous headline YoY
rates were not published. Food and group series are handled separately by build_dataset.py.

Run from the project root:  python src/headline_analysis.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg

RAW = cfg.ROOT / "data" / "raw" / "cpi_2012_combined_headline_official.csv"
PROCESSED = cfg.ROOT / "data" / "processed" / "headline_dataset.csv"
TABLES = cfg.ROOT / "outputs" / "tables"
FIGS = cfg.ROOT / "outputs" / "figures"
BAND_LOW, BAND_HIGH = 2.0, 6.0


def load():
    df = pd.read_csv(RAW)
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M")
    return df.set_index("date").sort_index()


def construct(df):
    out = df.copy()
    out["yoy_computed"] = (out["headline"] / out["headline"].shift(12) - 1) * 100
    out["mom"] = (out["headline"] / out["headline"].shift(1) - 1) * 100
    out["log_mom"] = 100 * np.log(out["headline"]).diff()
    out["gap_pp"] = out["yoy_computed"] - out["headline_yoy_published"]
    return out


def validate(out):
    w = out.loc[cfg.ANALYSIS_START:cfg.ANALYSIS_END]
    L = ["HEADLINE VALIDATION (official MoSPI series, CPI Combined, base 2012=100)"]
    L.append(f"Index months available: {len(out)} ({out.index.min()} to {out.index.max()})")
    L.append(f"Analysis window: {w.index.min()} to {w.index.max()} ({len(w)} months)")
    missing_pub = [str(p) for p in w.index[w['headline_yoy_published'].isna()]]
    L.append(f"Months with no published YoY: {missing_pub} (MoSPI: not compiled due to Covid-19)")
    g = w["gap_pp"].abs()
    L.append(f"Computed YoY (from rounded indices) vs published YoY: max gap {g.max():.3f} pp, "
             f"mean {g.mean():.3f} pp, months > 0.10 pp: {int((g > 0.10).sum())}")
    ok = bool(g.max() < 0.15)
    L.append("  " + ("OK: differences are consistent with rounding of one-decimal indices" if ok
                     else "FAIL: investigate transcription or definitions"))
    L.append("April–May 2020 index levels in this continuous series are from the later MoSPI/NSO business-continuity reconstruction and contain imputed components; the contemporaneous General CPI/YoY releases were incomplete or unavailable.")
    yc = out.loc[["2020-04", "2020-05"], "yoy_computed"]
    L.append(f"  Index-computed YoY from the reconstructed levels: {yc.iloc[0]:.2f}% and {yc.iloc[1]:.2f}% (not published official YoY rates; interpret as imputation-sensitive).")
    L.append("Dec 2025 index and inflation are marked provisional by MoSPI.")
    L.append("OVERALL: " + ("PASS" if ok else "FAIL"))
    return L, ok


def summary_stats(out):
    w = out.loc[cfg.ANALYSIS_START:cfg.ANALYSIS_END]
    rows = {}
    for label, s in [("Headline YoY, published (%)", w["headline_yoy_published"]),
                     ("Headline MoM, computed (%)", w["mom"])]:
        s = s.dropna()
        rows[label] = {
            "n": len(s), "mean": s.mean(), "median": s.median(), "std": s.std(ddof=1),
            "min": s.min(), "max": s.max(), "skewness": stats.skew(s, bias=False),
            "excess_kurtosis": stats.kurtosis(s, fisher=True, bias=False),
            "first_order_autocorr": s.autocorr(1),
        }
    return pd.DataFrame(rows).T


def band_episodes(out):
    s = out.loc[cfg.ANALYSIS_START:cfg.ANALYSIS_END, "headline_yoy_published"]
    state = pd.Series(np.where(s.isna(), "gap", np.where(s > BAND_HIGH, "above 6%",
                      np.where(s < BAND_LOW, "below 2%", "within band"))), index=s.index)
    eps, start = [], None
    for i, p in enumerate(state.index):
        cur = state.iloc[i]
        prev = state.iloc[i - 1] if i else None
        if cur != prev:
            if start is not None and state.iloc[i - 1] in ("above 6%", "below 2%"):
                eps.append(_ep(s, state, start, i - 1))
            start = i
    if state.iloc[-1] in ("above 6%", "below 2%"):
        eps.append(_ep(s, state, start, len(state) - 1))
    return state, pd.DataFrame(eps)


def _ep(s, state, a, b):
    seg = s.iloc[a:b + 1]
    return {"direction": state.iloc[a], "start": str(s.index[a]), "end": str(s.index[b]),
            "months": b - a + 1, "peak_or_trough": seg.max() if state.iloc[a] == "above 6%" else seg.min()}


def figure(out, state):
    w = out.loc[cfg.ANALYSIS_START:cfg.ANALYSIS_END]
    x = w.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.axhspan(BAND_LOW, BAND_HIGH, color="#d9ead3", alpha=0.7, label="2-6% band")
    ax.plot(x, w["headline_yoy_published"], color="#1f4e79", lw=1.8, label="Headline CPI inflation (YoY, published)")
    ax.axvspan(pd.Timestamp("2020-03-15"), pd.Timestamp("2020-05-31"), color="grey", alpha=0.25,
               label="Apr-May 2020: YoY not compiled")
    ax.set_ylabel("Per cent, year on year")
    ax.set_title("India headline CPI inflation, January 2014 to December 2025")
    ax.legend(loc="upper right", fontsize=8, frameon=False)
    ax.grid(alpha=0.3)
    fig.text(0.01, 0.005, "Source: MoSPI, CPI (Combined), base 2012=100. Dec 2025 provisional.", fontsize=7)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGS / "fig_headline_yoy_band.png", dpi=200)
    plt.close(fig)


def main():
    out = construct(load())
    lines, ok = validate(out)
    st = summary_stats(out)
    state, eps = band_episodes(out)

    cnt = state.value_counts()
    lines.append("")
    lines.append(f"2-6% BAND, {cfg.ANALYSIS_START} to {cfg.ANALYSIS_END}: " +
                 ", ".join(f"{k}: {int(v)}" for k, v in cnt.items()))
    for p in ("2014-01", "2020-04"):
        pass
    TABLES.mkdir(parents=True, exist_ok=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    save = out.copy(); save.index = save.index.astype(str); save.index.name = "date"
    save.to_csv(PROCESSED)
    st.round(3).to_csv(TABLES / "headline_summary_stats.csv")
    eps.to_csv(TABLES / "headline_band_episodes.csv", index=False)
    (TABLES / "headline_validation.txt").write_text("\n".join(lines) + "\n")
    figure(out, state)
    print("\n".join(lines)); print("\nSUMMARY STATS"); print(st.round(3).to_string())
    print("\nBAND EPISODES"); print(eps.to_string(index=False))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
