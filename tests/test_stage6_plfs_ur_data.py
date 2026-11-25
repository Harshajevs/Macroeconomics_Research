"""Structural and transcription checks for Stage 6 PLFS urban UR input.

This test does not download source PDFs, recreate PLFS microdata, construct CPI
inflation, or estimate a Phillips Curve. It checks the source-transcribed input
and the separately recorded overlaps against the project's frozen transcription.
"""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "plfs_urban_quarterly_ur_2018_2024.csv"
RECON = ROOT / "data" / "raw" / "plfs_urban_quarterly_ur_source_reconciliation_stage6.csv"

EXPECTED_VALUES = {
    "2018Q2": 9.7, "2018Q3": 9.6, "2018Q4": 9.7,
    "2019Q1": 9.2, "2019Q2": 8.8, "2019Q3": 8.3,
    "2019Q4": 7.8, "2020Q1": 9.1, "2020Q2": 20.8,
    "2020Q3": 13.2, "2020Q4": 10.3, "2021Q1": 9.3,
    "2021Q2": 12.6, "2021Q3": 9.8, "2021Q4": 8.7,
    "2022Q1": 8.2, "2022Q2": 7.6, "2022Q3": 7.2,
    "2022Q4": 7.2, "2023Q1": 6.8, "2023Q2": 6.6,
    "2023Q3": 6.6, "2023Q4": 6.5, "2024Q1": 6.7,
    "2024Q2": 6.6, "2024Q3": 6.4, "2024Q4": 6.4,
}


class TestStage6PLFSUrbanUR(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with DATA.open(newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))
        with RECON.open(newline="", encoding="utf-8") as f:
            cls.reconciliation = list(csv.DictReader(f))

    def test_complete_ordered_quarter_calendar(self) -> None:
        expected = [f"{year}Q{quarter}" for year in range(2018, 2025)
                    for quarter in range(1, 5)
                    if year > 2018 or quarter >= 2]
        actual = [row["quarter_id"] for row in self.rows]
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 27)
        self.assertEqual(len(set(actual)), 27)

    def test_values_match_source_transcription_record(self) -> None:
        actual = {row["quarter_id"]: float(row["ur_cws_15plus_person_pct"])
                  for row in self.rows}
        self.assertEqual(actual, EXPECTED_VALUES)

    def test_series_dimensions_and_primary_provenance(self) -> None:
        for row in self.rows:
            self.assertIn("All India; Urban; CWS; age 15 years and above; Person",
                          row["series_definition"])
            self.assertEqual(row["primary_statement_table"], "Statement 5")
            self.assertTrue(row["primary_page"])
            self.assertTrue(row["primary_source_url"].startswith("https://"))
            self.assertEqual(row["retrieval_date"], "2026-11-17")

    def test_overlapping_bulletins_agree(self) -> None:
        self.assertEqual(len(self.reconciliation), 17)
        for row in self.reconciliation:
            self.assertEqual(row["match"], "yes")
            self.assertEqual(float(row["primary_value_pct"]),
                             float(row["crosscheck_value_pct"]))
            self.assertTrue(row["crosscheck_url"].startswith("https://"))

    def test_pandemic_observations_are_retained_and_flagged(self) -> None:
        by_quarter = {row["quarter_id"]: row for row in self.rows}
        self.assertEqual(float(by_quarter["2020Q2"]["ur_cws_15plus_person_pct"]), 20.8)
        self.assertIn("Pandemic quarter", by_quarter["2020Q2"]["notes"])
        self.assertIn("2020Q3", by_quarter)

    def test_no_claim_of_model_estimation(self) -> None:
        report = ROOT / "outputs" / "tables" / "stage6_plfs_ur_validation.txt"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertIn("No CPI data construction", text)
        self.assertIn("regression", text.lower())
        self.assertIn("17 of 17 match", text)


if __name__ == "__main__":
    unittest.main()
