# Econometric design review — corrected pre-estimation version 3.0

This document supersedes the earlier Stage-2 design memo. The original Stage-2 diagnostic tables and script are preserved under `outputs/archive/legacy_stage2_diagnostics/` and `src/archive/` for auditability only.

## Main corrections

1. YoY moments are descriptive only; iid Jarque-Bera and correlation inference on overlapping YoY series are deprecated.
2. Monthly data now start in February 2013 for MoM analysis. YoY starts in January 2014.
3. Robust STL is applied to log CPI index levels before differencing for descriptive seasonally adjusted MoM statistics.
4. H1 volatility inference uses paired stationary bootstrap with an automatic Politis–White/Patton–Politis–White expected block length and 6/12/24-block sensitivities. SD difference and log SD ratio are both reported.
5. H2 is retired as confirmatory; the STL-MoM moment comparison is explicitly exploratory.
6. The old one-direction raw YoY lead-lag table is archived, not used for inference.
7. Four March–June 2020 pulse indicators are created in the processed dataset.
8. All twelve food subgroups and official rounded Combined weights are used for subgroup stylised facts and a derived food-ex-vegetables proxy.
9. Non-food group volatility is reported individually to address aggregation/diversification effects.
10. A covariance-aware variance decomposition is generated using Cov(component contribution, aggregate contribution)/Var(aggregate contribution), and is explicitly described as accounting/statistical rather than causal.
11. The operational core definition is documented, including 3.58866% of full CPI weight retained in Miscellaneous for vehicle-fuel and precious-metal items.
12. The formal regression specification is pre-declared in `econometric_model_specification.md`; no formal spillover regression is estimated in this milestone.

## Primary specification

Use group-built non-food monthly log inflation as the dependent variable and Food and Beverages monthly log inflation as the primary regressor. Select own-lag order `p` by BIC over {0,1,2,3}; fix the baseline food horizon at `q=3`; include month indicators and separate March–June 2020 event pulses. The delayed spillover test is H0: beta1=beta2=beta3=0, with effect-size estimand beta1+beta2+beta3. Same-month beta0 is contemporaneous co-movement only.

The common q=3 candidate-model estimation sample begins in May 2013, after the MoM series' February 2013 first observation and the three required lags. Report q=1 and q=6 sensitivity, 2014-start and FIT samples, and an exclusion of March–June 2020.

## Current active outputs

- `yoy_descriptive_moments_no_iid_inference.csv`
- `raw_mom_descriptive_moments.csv`
- `stl_mom_descriptive_moments.csv`
- `stl_seasonally_adjusted_monthly_inflation.csv`
- `stl_mom_paired_stationary_bootstrap.csv`
- `stl_mom_politis_white_block_length.csv`
- `food_subgroup_stylised_facts.csv`
- `nonfood_group_volatility_comparison.csv`
- `food_subgroup_aggregation_validation.txt`
- `covariance_aware_group_variance_decomposition.csv`

## Not yet completed

- Formal baseline distributed-lag regression and HAC inference.
- Regression residual diagnostics and post-COVID coefficient-stability test.
- External-control model using separately validated crude-oil and exchange-rate data.
- Final student-authored literature synthesis and report.

All current descriptive outputs are reproducible with `python src/corrected_descriptive_analysis.py` after running `python src/build_dataset.py`.
