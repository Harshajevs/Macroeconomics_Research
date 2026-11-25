"""Compare the complete analytical input against official three-month CPI spot checks.
Run from the project root: python src/spotcheck_groups.py
"""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as cfg

raw_path = cfg.ROOT / "data" / "raw" / "cpi_2012_combined_groups.csv"
check_path = cfg.ROOT / "data" / "raw" / "group_spotcheck_from_dec2025_release.csv"
if not raw_path.exists():
    print(f"FAIL: analytic raw group file not found: {raw_path}")
    sys.exit(1)
raw = pd.read_csv(raw_path).set_index("date")
ref = pd.read_csv(check_path).set_index("date")
cols = ["headline", *cfg.WEIGHTS.keys(), "cfpi"]
missing = [c for c in cols if c not in raw.columns or c not in ref.columns]
if missing:
    print(f"FAIL: missing comparison columns: {missing}")
    sys.exit(1)
lines = ["FULL-INPUT SPOT-CHECK AGAINST OFFICIAL MoSPI DECEMBER 2025 RELEASE",
         f"Analytic input rows: {len(raw)}; spot-check dates: {len(ref)}",
         f"Group weights sum: {sum(cfg.WEIGHTS.values()):.2f}"]
all_diffs=[]
for date, expected in ref.iterrows():
    if date not in raw.index:
        lines.append(f"FAIL {date}: missing from analytic input")
        all_diffs.append(float("inf"))
        continue
    gaps=[]
    for col in cols:
        gap=abs(float(raw.loc[date,col])-float(expected[col]))
        gaps.append(gap); all_diffs.append(gap)
    lines.append(f"{date}: max abs series difference {max(gaps):.3f} index points")
# Check weighted index aggregation for these official check months.
w = pd.Series(cfg.WEIGHTS, dtype=float) / 100
ref_calc=(ref[list(cfg.WEIGHTS)]*w).sum(axis=1)
ref_gap=ref_calc-ref["headline"]
lines.append(f"Official spot-check weighted-index residual max: {ref_gap.abs().max():.3f}")
maxdiff=max(all_diffs) if all_diffs else float('inf')
ok=(maxdiff <= 0.051) and (ref_gap.abs().max() < 0.1)
lines.append(f"RESULT: {'PASS' if ok else 'FAIL'}")
out=cfg.ROOT/"outputs"/"tables"/"group_weight_spotcheck.txt"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text("\n".join(lines)+"\n")
print("\n".join(lines))
sys.exit(0 if ok else 1)
