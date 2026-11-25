"""Corrected descriptive outputs and post-results v3.3 specification checks."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DOCS = ROOT / "documentation"
DATA = ROOT / "data" / "processed" / "inflation_dataset.csv"
sys.path.insert(0, str(ROOT / "src"))
from corrected_descriptive_analysis import stationary_bootstrap_index_matrix


def main():
    assert DATA.exists(), "Run src/build_dataset.py first"
    data = pd.read_csv(DATA)
    assert len(data) == 156
    assert data.date.iloc[0] == "2013-01" and data.date.iloc[-1] == "2025-12"
    assert data.date.is_unique
    assert data.loc[data.date >= "2013-02", "infl_food_log"].notna().all()
    assert data.loc[data.date < "2014-01", "infl_food_yoy"].isna().all()
    assert int(data.flag_covid_pulse.sum()) == 7
    assert int(data.flag_june_2013_housing_step.sum()) == 1
    assert int(data.flag_collection_gap.sum()) == 2
    assert int(data.flag_covid_imputed_series_month.sum()) == 2
    assert list(data.loc[data.flag_covid_imputed_series_month.eq(1), "date"].astype(str)) == ["2020-04", "2020-05"]

    required = [
        "yoy_descriptive_moments_no_iid_inference.csv",
        "raw_mom_descriptive_moments.csv",
        "stl_mom_descriptive_moments.csv",
        "stl_seasonally_adjusted_monthly_inflation.csv",
        "stl_seasonally_adjusted_log_indices.csv",
        "stl_mom_paired_stationary_bootstrap.csv",
        "stl_mom_politis_white_block_length.csv",
        "food_subgroup_stylised_facts.csv",
        "nonfood_group_volatility_comparison.csv",
        "food_subgroup_indices_and_food_ex_vegetables_proxy.csv",
        "food_subgroup_aggregation_validation.txt",
        "covariance_aware_group_variance_decomposition.csv",
        "corrected_descriptive_summary.txt",
        "stl_seasonal_window_sensitivity.csv",
    ]
    missing = [x for x in required if not (TABLES / x).exists()]
    assert not missing, f"Missing corrected output files: {missing}"

    yoy = pd.read_csv(TABLES / "yoy_descriptive_moments_no_iid_inference.csv")
    assert yoy["inference_note"].str.contains("descriptive only", case=False).all()
    assert not any("pvalue" in c.lower() for c in yoy.columns), "No iid YoY p-values should be included"

    sa = pd.read_csv(TABLES / "stl_seasonally_adjusted_monthly_inflation.csv")
    assert len(sa) == 156
    assert sa.loc[sa.date >= "2013-02", "Food and Beverages"].notna().sum() == 155

    boot = pd.read_csv(TABLES / "stl_mom_paired_stationary_bootstrap.csv")
    assert set(boot["block_selection"]) == {"Politis-White automatic", "fixed sensitivity"}
    assert set(boot.loc[boot.block_selection == "fixed sensitivity", "expected_block_length"]) == {1, 3, 6, 12, 24}
    assert boot["replications"].eq(4999).all()
    assert boot["monte_carlo_resolution"].gt(0).all()
    assert boot["bootstrap_tail_probability_le_zero"].gt(0).all()

    # Vectorised stationary bootstrap indices are reproducible, in range and shared by paired series.
    idx_a = stationary_bootstrap_index_matrix(155, 6, 50, np.random.default_rng(1234))
    idx_b = stationary_bootstrap_index_matrix(155, 6, 50, np.random.default_rng(1234))
    assert idx_a.shape == (50, 155) and np.array_equal(idx_a, idx_b)
    assert idx_a.min() >= 0 and idx_a.max() < 155

    block = pd.read_csv(TABLES / "stl_mom_politis_white_block_length.csv")
    assert set(block.series) == {"Food", "Non-food"}
    assert block.block_length.between(2, 50).all()
    assert block.method.str.contains("Politis-White").all()
    assert block.block_length.between(2, 50).all(), "Block length must obey documented local finite-sample bounds"
    assert not block.method.str.contains("cube-root", case=False).any()

    weights = pd.read_csv(ROOT / "data" / "raw" / "food_subgroup_combined_weights_2012.csv")
    assert len(weights) == 12
    assert abs(weights.combined_weight_percent.sum() - 45.86) < 1e-8
    assert abs(weights.loc[weights.subgroup == "Vegetables", "combined_weight_percent"].iloc[0] - 6.04) < 1e-8
    food_note = (TABLES / "food_subgroup_aggregation_validation.txt").read_text()
    assert "not an independently published MoSPI series" in food_note

    sub = pd.read_csv(TABLES / "food_subgroup_stylised_facts.csv")
    assert len(sub) == 12
    groups = pd.read_csv(TABLES / "nonfood_group_volatility_comparison.csv")
    assert len(groups) == 7

    vd = pd.read_csv(TABLES / "covariance_aware_group_variance_decomposition.csv")
    assert {"raw", "STL-adjusted", "raw-overlapping-12m-descriptive"}.issubset(set(vd.basis))
    for _, grp in vd.groupby(["frequency", "basis", "decomposition"]):
        assert abs(grp.share_of_aggregate_variance_percent.sum() - 100) < 1e-6
    assert vd.interpretation.str.contains("not causal").all()

    hyp = (DOCS / "hypotheses.md").read_text()
    spec = (DOCS / "econometric_model_specification.md").read_text()
    core = (DOCS / "core_measure_composition.md").read_text()
    assert "H2 (retired as confirmatory)" in hyp
    assert "group-built non-food CPI" in spec
    assert "Team-authored reasoning and partner approval remain pending" in hyp
    assert "q=3" in spec and "{0,1,2,3}" in spec
    assert "October 2013" in spec and "March–September 2020" in spec
    assert "smallest p" in spec
    assert "beta_1=\\cdots=\\beta_q=0" in spec
    assert "March" in spec and "June" in spec
    assert "3.58866" in core

    # Ensure stale inferential artifacts are not left in active tables.
    for stale in ["food_lead_nonfood_lag_correlations.csv", "food_nonfood_volatility_difference_block_bootstrap.csv"]:
        assert not (TABLES / stale).exists(), f"Legacy output should be archived, found active: {stale}"
        assert list((ROOT / "outputs" / "archive").rglob(stale)), f"Legacy output was not preserved: {stale}"

    # Every active figure must be named in a source generator; legacy figures are archived.
    import re
    source_text = "\n".join(p.read_text(errors="ignore") for p in (ROOT / "src").rglob("*.py") if "archive" not in p.parts)
    active_figs = list((ROOT / "outputs" / "figures").glob("*.png"))
    unreferenced = [p.name for p in active_figs if p.name not in source_text]
    assert not unreferenced, f"Active figures without a source-code generator reference: {unreferenced}"

    print("ALL POST-REVIEW DESCRIPTIVE/SPECIFICATION STRUCTURE TESTS PASSED")
    print("Validated authentic CPI pipeline, corrected YoY labels, STL-MoM series, bootstrap sensitivities, subgroup weights, covariance decomposition and post-results v3.3 specification.")
    print("Regression behaviour and outputs are validated separately by postreview tests.")


if __name__ == "__main__":
    main()
