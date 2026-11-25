"""Compares our official headline series with stylized facts reported in the RBI Bulletin
article by Mohan, Hasan, Sarkar and John (Feb 2026), which covers April 2016 to August 2025.
Run from the project root after headline_analysis.py:  python src/replicate_rbi_stylised_facts.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg

df = pd.read_csv(cfg.ROOT / "data" / "processed" / "headline_dataset.csv", index_col="date")
df.index = pd.PeriodIndex(df.index, freq="M")
w = df.loc["2016-04":"2025-08"]

# RBI's figures as reported in the paper's text (the paper states them to 1 decimal / whole %)
reported = {"mean": 4.9, "sd": 1.5, "share_above_6_pct": 26, "months_below_2": 3}

L = ["REPLICATION CHECK: RBI Bulletin Feb 2026 (Mohan, Hasan, Sarkar, John), stylized facts, Apr 2016 to Aug 2025",
     f"Months in window: {len(w)}", ""]
for label, s in [("Published YoY (Apr-May 2020 not compiled)", w["headline_yoy_published"]),
                 ("YoY computed from index (fills Apr-May 2020)", w["yoy_computed"])]:
    s = s.dropna()
    L.append(f"{label}: n={len(s)}")
    L.append(f"  mean {s.mean():.2f} (RBI {reported['mean']}), SD {s.std(ddof=1):.2f} (RBI {reported['sd']})")
    L.append(f"  months above 6%: {(s > 6).sum()} = {100 * (s > 6).sum() / len(s):.1f}% (RBI about {reported['share_above_6_pct']}%)")
    L.append(f"  months below 2%: {(s < 2).sum()} (RBI {reported['months_below_2']}): {[str(p) for p in s.index[s < 2]]}")
    L.append("")
L.append("READING: using index-computed YoY from the later MoSPI/NSO reconstructed series for Apr-May 2020")
L.append("reproduces the RBI's approximately 26% above-band share; using only published YoY gives 24.3%.")
L.append("This is consistent with those two months being included in the RBI tally, but does not establish")
L.append("the exact source vintage or handling used by the RBI authors; treat this as a replication clue, not proof.")
out = cfg.ROOT / "outputs" / "tables" / "replication_rbi_feb2026.txt"
out.write_text("\n".join(L) + "\n")
print("\n".join(L))
