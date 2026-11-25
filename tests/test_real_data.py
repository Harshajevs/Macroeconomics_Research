"""Integration/smoke test against the project's real, sourced CPI input.

Unlike test_pipeline.py (which uses synthetic data for unit testing), this test
validates the preserved MoSPI-derived input and executes the real-data pipeline.
Run from project root: python tests/test_real_data.py
"""
import sys
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import build_dataset as bd
import config as cfg


def main():
    raw_path = ROOT / "data" / "raw" / "cpi_2012_combined_groups.csv"
    check_path = ROOT / "data" / "raw" / "group_spotcheck_from_dec2025_release.csv"
    raw = pd.read_csv(raw_path)

    assert len(raw) == 156, f"Expected 156 monthly rows, got {len(raw)}"
    assert raw["date"].iloc[0] == "2013-01" and raw["date"].iloc[-1] == "2025-12"
    assert raw["date"].is_unique
    expected = pd.period_range("2013-01", "2025-12", freq="M").astype(str)
    assert raw["date"].tolist() == expected.tolist(), "Raw date range is not complete and ordered"

    # Check that the headline index in the analytic input matches the preserved workbook export.
    source_path = ROOT / "data" / "raw" / "cpi_2012_combined_groups_source_export.csv"
    source = pd.read_csv(source_path)
    general = source[(source["state"] == "All India") & (source["sector"] == "Combined") &
                     (source["subgroup"] == "General-Overall")].copy()
    general["date"] = general.apply(lambda r: f"{int(r['year']):04d}-{int(r['month_code']):02d}", axis=1)
    merged = raw[["date", "headline"]].merge(general[["date", "index"]], on="date", how="left", validate="one_to_one")
    assert merged["index"].notna().all()
    assert np.max(np.abs(merged["headline"].astype(float) - merged["index"].astype(float))) == 0.0

    groups = ["food_bev", "pan_tobacco", "clothing", "housing", "fuel_light", "misc"]
    for col in ["headline"] + groups + ["cfpi"]:
        assert raw[col].notna().all(), f"Missing values in required real-data field: {col}"
        assert (raw[col] > 0).all(), f"Non-positive values in {col}"
    missing_yoy = raw.loc[raw["headline_yoy_published"].isna(), "date"].tolist()
    expected_missing = [f"2013-{m:02d}" for m in range(1, 13)] + ["2020-04", "2020-05"]
    assert missing_yoy == expected_missing, f"Unexpected published headline YoY gaps: {missing_yoy}"

    # Compare all available series against official Dec-2024, Nov-2025 and Dec-2025 checks.
    spot = pd.read_csv(check_path).set_index("date")
    check_cols = ["headline", *groups, "cfpi"]
    indexed = raw.set_index("date")
    for date, row in spot.iterrows():
        for col in check_cols:
            gap = abs(float(indexed.loc[date, col]) - float(row[col]))
            assert gap <= 0.051, f"Spot-check mismatch {date} {col}: gap={gap}"

    # Explicitly assert the documented source-reconciliation entries.
    assert float(indexed.loc["2025-12", "pan_tobacco"]) == 215.8
    recovered = {"2018-12":146.5,"2019-01":147.7,"2019-02":148.5,"2019-03":149.0,
                 "2019-04":149.7,"2019-05":150.1,"2019-06":149.4,"2019-07":150.6,
                 "2019-08":151.6,"2019-09":152.2}
    for date, value in recovered.items():
        assert float(indexed.loc[date, "housing"]) == value, f"Housing recovery mismatch at {date}"
    recovery_log = pd.read_csv(ROOT / "data" / "raw" / "housing_index_recovery_sources.csv")
    assert len(recovery_log) == 10 and set(recovery_log["date"]) == set(recovered)

    # Execute the full real-data build to temporary output paths.
    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "inflation_dataset.csv"
        report_path = Path(tmp) / "validation_report.txt"
        code = bd.main(["--raw", str(raw_path), "--out", str(out_path), "--report", str(report_path)])
        assert code == 0, "Real data build failed"
        out = pd.read_csv(out_path, index_col="date")
        assert len(out) == 156
        assert out.index[0] == "2013-01" and out.index[-1] == "2025-12"
        assert "infl_cfpi_yoy" in out.columns
        assert "headline_yoy_published" in out.columns
        # YoY warm-up is the first twelve raw months; subsequent computed values are complete.
        for col in ["infl_food_yoy", "infl_nonfood_yoy", "infl_core_yoy", "infl_cfpi_yoy"]:
            assert out.loc["2014-01":, col].notna().all(), f"Unexpected missing YoY values in {col}"
            assert out.loc["2013-01":"2013-12", col].isna().all(), f"Unexpected pre-YoY warm-up values in {col}"
        for col in ["infl_food_log", "infl_nonfood_log", "infl_core_log"]:
            assert out.loc["2013-02":, col].notna().all(), f"Unexpected missing MoM values in {col}"
            assert pd.isna(out.loc["2013-01", col]), f"Expected Jan-2013 MoM warm-up in {col}"
        assert int(out["flag_collection_gap"].sum()) == 2
        assert int(out["flag_covid_imputed_series_month"].sum()) == 2
        assert list(out.index[out["flag_covid_imputed_series_month"].eq(1)].astype(str)) == ["2020-04", "2020-05"]
        assert int(out["flag_covid_pulse"].sum()) == 7
        assert int(out["flag_june_2013_housing_step"].sum()) == 1
        compare = (out.loc["2014-01":, "infl_headline_yoy"] - out.loc["2014-01":, "headline_yoy_published"]).abs().dropna()
        assert compare.max() < 0.02, f"Headline inflation cross-check failed: {compare.max()}"
        report = report_path.read_text()
        assert "OVERALL: PASS" in report
        assert "CFPI included: yes" in report
    print("ALL REAL-DATA INTEGRATION TESTS PASSED")
    print("Validated: 156 raw months; six groups + headline + CFPI; official spot checks; housing recovery; Pan/Tobacco reconciliation; 156-row processed dataset (144 YoY observations; 155 MoM changes).")


if __name__ == "__main__":
    main()
