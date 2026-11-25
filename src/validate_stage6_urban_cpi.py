"""Strict intake validation for the All-India Urban CPI (2012=100) series.

This is an intake validator, not a downloader or estimator. It requires the
untouched source export and anchor-check file. It does not impute or silently
repair observations. Month-on-month jumps are reported and large jumps fail.
"""
from __future__ import annotations
import argparse, csv, hashlib, math, re
from pathlib import Path
from typing import Iterable

EXPECTED_MONTHS = [f"{y:04d}-{m:02d}" for y in range(2013, 2026) for m in range(1, 13)]
INDEX_FIELDS = [
    "urban_general_index", "food_beverages_group1_index", "pan_tobacco_group2_index",
    "clothing_footwear_group3_index", "housing_group4_index", "fuel_light_group5_index",
    "miscellaneous_group6_index",
]
GROUP_FIELDS = INDEX_FIELDS[1:]
WEIGHTS = {
    "food_beverages_group1_index": 36.29,
    "pan_tobacco_group2_index": 1.36,
    "clothing_footwear_group3_index": 5.57,
    "housing_group4_index": 21.67,
    "fuel_light_group5_index": 5.58,
    "miscellaneous_group6_index": 29.53,
}
FLAG_FIELDS = [
    "flag_general_macro_imputed", "flag_food_group1_macro_imputed",
    "flag_pan_group2_macro_imputed", "flag_clothing_group3_macro_imputed",
    "flag_housing_group4_macro_imputed", "flag_fuel_group5_macro_imputed",
    "flag_miscellaneous_group6_macro_imputed",
]
REQUIRED_FIELDS = [
    "month", *INDEX_FIELDS, "sector", "base_year", "series", "state_coverage",
    "source_document", "source_url", "retrieval_date", "export_date", "filter_settings",
    "month_status", "raw_source_sha256", *FLAG_FIELDS,
]
ANCHOR_MONTHS = ["2017-01", "2018-12", "2019-12", "2020-04", "2020-05", "2021-12", "2023-12", "2024-12"]
PLAUSIBLE_MIN, PLAUSIBLE_MAX = 90.0, 300.0
COMPOSITE_MAX_ABS_RESIDUAL = 0.50  # provisional gate only; Claude must reassess against the actual Urban export
MOM_WARNING_LOG_CHANGE = 0.10    # warning flag only
MOM_BLOCK_LOG_CHANGE = 0.35      # hard fail; catches gross spikes (e.g. 10x)

class CPIValidationError(ValueError):
    """Raised when the CPI input fails a pre-estimation acceptance check."""

def _as_bool(value: object, name: str, rowno: int) -> bool:
    s = str(value).strip().lower()
    if s in {"1", "true", "yes", "y"}: return True
    if s in {"0", "false", "no", "n"}: return False
    raise CPIValidationError(f"Row {rowno}: {name} must be an explicit true/false flag; got {value!r}.")

def _sha_ok(s: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", s.strip()))

def _parse_date(s: str, name: str, rowno: int) -> None:
    try:
        from datetime import date
        date.fromisoformat(s.strip())
    except Exception as exc:
        raise CPIValidationError(f"Row {rowno}: {name} must be YYYY-MM-DD.") from exc

def _expected_imputation_flags(month: str) -> dict[str, bool]:
    # MoSPI CPI Technical Note, Table 1, Urban columns; '@' denotes macro-imputed index.
    # April: General, Food, Pan, Clothing, Miscellaneous; May: General, Food,
    # Clothing, Miscellaneous. Housing and Fuel/Light are not marked imputed.
    mapping = {name: False for name in FLAG_FIELDS}
    if month == "2020-04":
        for key in FLAG_FIELDS: mapping[key] = key in {
            "flag_general_macro_imputed", "flag_food_group1_macro_imputed",
            "flag_pan_group2_macro_imputed", "flag_clothing_group3_macro_imputed",
            "flag_miscellaneous_group6_macro_imputed"}
    elif month == "2020-05":
        for key in FLAG_FIELDS: mapping[key] = key in {
            "flag_general_macro_imputed", "flag_food_group1_macro_imputed",
            "flag_clothing_group3_macro_imputed", "flag_miscellaneous_group6_macro_imputed"}
    return mapping

def validate_rows(rows: Iterable[dict[str, str]], anchor_rows: Iterable[dict[str, str]],
                  expected_raw_sha256: str | None = None) -> dict[str, object]:
    records = list(rows)
    anchors = list(anchor_rows)
    if not records: raise CPIValidationError("No CPI data rows found.")
    missing_fields = [f for f in REQUIRED_FIELDS if f not in records[0]]
    if missing_fields: raise CPIValidationError(f"Missing required CPI columns: {', '.join(missing_fields)}")
    months = [str(r.get("month", "")).strip() for r in records]
    if len(months) != len(set(months)): raise CPIValidationError("Duplicate month keys found.")
    if months != EXPECTED_MONTHS:
        missing = sorted(set(EXPECTED_MONTHS)-set(months)); extra = sorted(set(months)-set(EXPECTED_MONTHS))
        raise CPIValidationError(f"Month sequence must be 2013-01 to 2025-12; missing={missing[:8]}, extra={extra[:8]}.")

    hashes = set()
    values = {f: [] for f in INDEX_FIELDS}
    values_by_month = {}
    statuses = set()
    for rowno, row in enumerate(records, start=2):
        for key, expected in (("sector", "Urban"), ("base_year", "2012"), ("series", "Current"), ("state_coverage", "All India")):
            if str(row.get(key, "")).strip().lower() != expected.lower():
                raise CPIValidationError(f"Row {rowno}: {key} must be {expected!r}; got {row.get(key)!r}.")
        for key in ("source_document", "source_url", "retrieval_date", "export_date", "filter_settings"):
            if not str(row.get(key, "")).strip(): raise CPIValidationError(f"Row {rowno}: provenance field {key} is blank.")
        _parse_date(str(row["retrieval_date"]), "retrieval_date", rowno)
        _parse_date(str(row["export_date"]), "export_date", rowno)
        status = str(row.get("month_status", "")).strip().lower()
        if status not in {"final", "provisional"}: raise CPIValidationError(f"Row {rowno}: month_status must be final or provisional.")
        statuses.add(status)
        digest = str(row.get("raw_source_sha256", "")).strip().lower()
        if not _sha_ok(digest): raise CPIValidationError(f"Row {rowno}: raw_source_sha256 must be a 64-character SHA-256 hex digest.")
        hashes.add(digest)

        monthvals = {}
        for field in INDEX_FIELDS:
            raw = str(row.get(field, "")).strip()
            try: val = float(raw)
            except (TypeError, ValueError) as exc: raise CPIValidationError(f"Row {rowno}: {field} is blank or non-numeric.") from exc
            if not math.isfinite(val) or not (PLAUSIBLE_MIN <= val <= PLAUSIBLE_MAX):
                raise CPIValidationError(f"Row {rowno}: {field}={val!r} outside plausible 2012-base index range [{PLAUSIBLE_MIN}, {PLAUSIBLE_MAX}].")
            values[field].append(val); monthvals[field] = val
        values_by_month[months[rowno-2]] = monthvals
        for flag in FLAG_FIELDS: _as_bool(row.get(flag, ""), flag, rowno)
        exp = _expected_imputation_flags(months[rowno-2])
        for flag, expval in exp.items():
            got = _as_bool(row.get(flag, ""), flag, rowno)
            if got != expval:
                raise CPIValidationError(f"Row {rowno}: {flag}={got} disagrees with MoSPI Table-1 annotation for {months[rowno-2]} (expected {expval}).")

    if len(hashes) != 1: raise CPIValidationError("Rows contain more than one raw-source SHA-256 value.")
    dataset_hash = next(iter(hashes))
    if expected_raw_sha256 is not None and dataset_hash != expected_raw_sha256.lower():
        raise CPIValidationError("Row raw_source_sha256 does not match the SHA-256 of the supplied untouched export.")

    # Reject group columns that are exactly identical throughout the complete history.
    identical_pairs = []
    for i, a in enumerate(GROUP_FIELDS):
        for b in GROUP_FIELDS[i+1:]:
            if np_allclose(values[a], values[b], atol=1e-12): identical_pairs.append((a, b))
    if identical_pairs:
        raise CPIValidationError(f"Two CPI group columns are identical across the full sample: {identical_pairs}.")

    # Month-on-month change flags. A 10%-plus log jump is flagged; >=35% is a blocking
    # anomaly requiring source resolution, not an automatic repair.
    jump_flags = []
    for j in range(1, len(months)):
        for field in INDEX_FIELDS:
            change = math.log(values[field][j] / values[field][j-1])
            if abs(change) >= MOM_BLOCK_LOG_CHANGE:
                raise CPIValidationError(f"Blocking month-on-month jump: {months[j]} {field} log change={change:.3f}.")
            if abs(change) >= MOM_WARNING_LOG_CHANGE:
                jump_flags.append({"month": months[j], "field": field, "log_change": round(change, 6), "pct_change": round((math.exp(change)-1)*100, 3)})

    # Covariance-aware contributions are not used here: this is only an index-level
    # arithmetic consistency check between six weighted group indices and General.
    # The 0.50-point cutoff is provisional, not empirically calibrated on Urban data;
    # it is a blocking review threshold until an actual extract establishes a justified tolerance.
    residuals = []
    for month in months:
        v = values_by_month[month]
        rebuilt = sum(v[k] * w for k, w in WEIGHTS.items()) / 100.0
        residuals.append({"month": month, "weighted_group_composite": rebuilt,
                          "general_index": v["urban_general_index"],
                          "residual_composite_minus_general": rebuilt-v["urban_general_index"]})
    residual_frame = group_residual_summary(residuals)
    max_abs_resid = max(abs(x["residual_composite_minus_general"]) for x in residuals)
    if max_abs_resid > COMPOSITE_MAX_ABS_RESIDUAL:
        raise CPIValidationError(f"Weighted six-group composite differs from General by up to {max_abs_resid:.3f} index points, beyond {COMPOSITE_MAX_ABS_RESIDUAL:.2f}; inspect method/vintage before proceeding.")

    # At least eight source-backed anchor months. Anchors compare official press-release
    # figures to the Warehouse extract, with one-decimal publication tolerance.
    anchor_month_keys = [str(r.get("month", "")).strip() for r in anchors]
    if len(anchor_month_keys) != len(set(anchor_month_keys)):
        raise CPIValidationError("Duplicate month keys found in the official anchor-check file.")
    anchor_map = {str(r.get("month", "")).strip(): r for r in anchors}
    missing_anchor_months = sorted(set(ANCHOR_MONTHS)-set(anchor_map))
    if missing_anchor_months: raise CPIValidationError(f"Anchor file is missing required months: {missing_anchor_months}.")
    anchor_comparisons = []
    for month in ANCHOR_MONTHS:
        arow = anchor_map[month]
        for k in ("source_document", "source_url"):
            if not str(arow.get(k, "")).strip(): raise CPIValidationError(f"Anchor {month}: missing {k}.")
        for field in INDEX_FIELDS:
            try: expected = float(arow.get(field, ""))
            except (TypeError, ValueError) as exc: raise CPIValidationError(f"Anchor {month}: missing/nonnumeric {field}.") from exc
            actual = values_by_month[month][field]
            diff = actual-expected
            if abs(diff) > 0.11:
                raise CPIValidationError(f"Anchor mismatch {month}/{field}: export={actual:.3f}, anchor={expected:.3f}, diff={diff:.3f}.")
            anchor_comparisons.append({"month":month,"field":field,"export":actual,"anchor":expected,"difference":diff})

    return {
        "rows": len(records), "first_month": months[0], "last_month": months[-1],
        "raw_source_sha256": dataset_hash, "month_statuses": sorted(statuses),
        "index_min": min(min(v) for v in values.values()), "index_max": max(max(v) for v in values.values()),
        "group_composite_max_abs_residual": max_abs_resid, "residual_summary_by_subperiod": residual_frame,
        "jump_warning_count": len(jump_flags), "jump_warnings": jump_flags,
        "anchor_comparisons": len(anchor_comparisons), "imputed_months": ["2020-04", "2020-05"],
    }

def np_allclose(a, b, atol=1e-12):
    return all(abs(x-y) <= atol for x,y in zip(a,b))

def group_residual_summary(residuals):
    periods = {"pre_pandemic_2013_2019": ("2013-01", "2019-12"),
               "pandemic_2020_2021": ("2020-01", "2021-12"),
               "post_2021_2022_2025": ("2022-01", "2025-12")}
    out=[]
    for label,(lo,hi) in periods.items():
        vals=[x["residual_composite_minus_general"] for x in residuals if lo <= x["month"] <= hi]
        out.append({"period":label,"n":len(vals),"mean_residual":sum(vals)/len(vals) if vals else None,
                    "max_abs_residual":max(abs(v) for v in vals) if vals else None})
    return out

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""): h.update(block)
    return h.hexdigest()

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="Cleaned Urban CPI CSV")
    p.add_argument("--raw-export", type=Path, required=True, help="Untouched source XLSX/CSV/JSON export")
    p.add_argument("--anchors", type=Path, required=True, help="Eight-month press-release anchor CSV")
    p.add_argument("--report", type=Path, default=Path("outputs/tables/stage6_urban_cpi_validation.json"))
    args=p.parse_args()
    for x in (args.input,args.raw_export,args.anchors):
        if not x.exists(): raise SystemExit(f"Required input not found: {x}")
    digest=sha256_file(args.raw_export)
    try:
        with args.input.open(newline="",encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
        with args.anchors.open(newline="",encoding="utf-8-sig") as f: anchors=list(csv.DictReader(f))
        result=validate_rows(rows,anchors,expected_raw_sha256=digest)
    except (OSError,csv.Error,CPIValidationError) as exc:
        raise SystemExit(f"CPI validation FAILED: {exc}") from exc
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(__import__('json').dumps(result,indent=2),encoding="utf-8")
    print("Stage 6 All-India Urban CPI validation: PASS")
    print(f"raw export sha256: {digest}")
    print(f"observations: {result['rows']} ({result['first_month']} to {result['last_month']})")
    print(f"max group-composite residual: {result['group_composite_max_abs_residual']:.4f}")
    print(f"month-on-month warning flags: {result['jump_warning_count']}")
    print(f"anchor comparisons: {result['anchor_comparisons']}")
    print("No inflation rates or Phillips-curve estimates were produced.")
    return 0
if __name__ == "__main__": raise SystemExit(main())
