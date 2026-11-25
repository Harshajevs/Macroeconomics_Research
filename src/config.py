"""Project settings. Edit values here, not inside the analysis code."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "cpi_2012_combined_groups.csv"
SOURCE_EXPORT = ROOT / "data" / "raw" / "cpi_2012_combined_groups_source_export.csv"
OUT_FILE = ROOT / "data" / "processed" / "inflation_dataset.csv"
REPORT_FILE = ROOT / "outputs" / "tables" / "validation_report.txt"

RAW_START, RAW_END = "2013-01", "2025-12"
# YoY requires 12 prior months; MoM starts as soon as one prior month exists.
YOY_ANALYSIS_START, YOY_ANALYSIS_END = "2014-01", "2025-12"
MOM_ANALYSIS_START, MOM_ANALYSIS_END = "2013-02", "2025-12"
ANALYSIS_START, ANALYSIS_END = YOY_ANALYSIS_START, YOY_ANALYSIS_END  # legacy alias

# CPI (Combined), base 2012=100, group weights in percent.
WEIGHTS = {
    "food_bev": 45.86,
    "pan_tobacco": 2.38,
    "clothing": 6.53,
    "housing": 10.07,
    "fuel_light": 6.84,
    "misc": 28.32,
}
FOOD = "food_bev"
FUEL = "fuel_light"
TOLERANCE = 0.5
COLLECTION_GAP_MONTHS = ["2020-04", "2020-05"]
COVID_PULSE_MONTHS = ["2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09"]
JUNE_2013_PULSE_MONTHS = ["2013-06"]
ECON_COMMON_START = "2013-10"  # avoids June-2013 Housing step exposure through three own lags
ECON_JAN2014_SENSITIVITY_START = "2014-01"
FIT_START = "2016-04"
POST_COVID_START = "2021-01"

# All-India Combined 2012-base food subgroup weights, from MoSPI Annexure I.
# The twelve weights sum to the Food & Beverages group weight (45.86%).
FOOD_SUBGROUP_WEIGHTS = {
    "Cereals and Products": 9.67,
    "Meat and Fish": 3.61,
    "Egg": 0.43,
    "Milk and Products": 6.61,
    "Oils and Fats": 3.56,
    "Fruits": 2.89,
    "Vegetables": 6.04,
    "Pulses and Products": 2.38,
    "Sugar and Confectionery": 1.36,
    "Spices": 2.50,
    "Non-alcoholic Beverages": 1.26,
    "Prepared Meals, Snacks, Sweets etc.": 5.55,
}
FOOD_SUBGROUP_WEIGHT_SOURCE = "https://www.mospi.gov.in/sites/default/files/press_release/cpi_pr_12apr16t.pdf"
ITEM_WEIGHT_SOURCE = "https://www.cpi.mospi.gov.in/Weight_AI_Item_Combined_2012.aspx"
