"""Self-test of the pipeline on SYNTHETIC data (random numbers, not real CPI).
Never use the synthetic file for analysis. Run:  python tests/test_pipeline.py
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import build_dataset as bd
import config as cfg


def synthetic_raw(seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.period_range(cfg.RAW_START, cfg.RAW_END, freq="M")
    w = pd.Series(cfg.WEIGHTS) / 100
    data = {g: np.round(100 + np.cumsum(rng.normal(0.4, 0.8, len(idx))), 1) for g in cfg.WEIGHTS}
    df = pd.DataFrame(data, index=idx)
    df.insert(0, "headline", np.round((df * w).sum(axis=1), 1))
    df.index.name = "date"
    return df.reset_index().assign(date=lambda d: d["date"].astype(str))


def main():
    raw = synthetic_raw()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        raw_path = tmp / "raw.csv"
        raw.to_csv(raw_path, index=False)

        # 1. Full pipeline runs and passes
        code = bd.main(["--raw", str(raw_path), "--out", str(tmp / "out.csv"), "--report", str(tmp / "rep.txt")])
        assert code == 0, "pipeline should pass on consistent synthetic data"
        out = pd.read_csv(tmp / "out.csv", index_col="date")
        assert len(out) == 156, len(out)
        assert out.index[0] == "2013-01" and out.index[-1] == "2025-12"
        assert out.loc["2014-01":].filter(like="_yoy").notna().all().all()
        assert out.loc["2013-02":].filter(like="_mom").notna().all().all()

        # 2. Contributions add up to headline inflation
        contrib = out[[f"contrib_{g}_yoy" for g in cfg.WEIGHTS]].sum(axis=1)
        assert (contrib - out["infl_headline_yoy"]).abs().max() < 0.2

        # 3. Missing month is caught
        broken = bd.load_raw(raw_path).drop(pd.Period("2018-06", "M"))
        problems, _ = bd.check_raw(broken, cfg.RAW_START, cfg.RAW_END)
        assert any("Missing months" in p for p in problems)

        # 4. A wrong weight is caught by the headline check
        bad_w = dict(cfg.WEIGHTS)
        bad_w["food_bev"] = 30.0
        df = bd.load_raw(raw_path)
        o = bd.build(df, weights=bad_w)
        _, ok = bd.validation_report(o, cfg.TOLERANCE, list(bad_w))
        assert not ok, "wrong weights should fail validation"
    print("ALL TESTS PASSED (synthetic data only)")


if __name__ == "__main__":
    main()
