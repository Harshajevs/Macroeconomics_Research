# Independent project tracker — ChatGPT lead copy (Stage 3)

**Project:** Food Inflation in India: Volatility, Persistence and Spillover Effects on Non-Food Prices  
**Last updated:** 14 November 2026  
**Canonical package:** Stage-3 corrected pre-estimation package  
**Data base:** All-India Combined CPI, 2012=100  
**Raw coverage:** Jan-2013 to Dec-2025 (156 months)  
**YoY descriptive window:** Jan-2014 to Dec-2025 (144 months)  
**MoM analytical window:** Feb-2013 to Dec-2025 (155 monthly changes)  

## Current overall status

<progress>52%</progress>

**Credited completion: 52 / 100 weighted points.** This is a project-management estimate, not an instructor grade. Credit is based on files and tests regenerated in the current package. Formal spillover regression, final robustness, student-authored literature synthesis and report writing are not credited.

| Phase | Weight | Credited | Status | Evidence and remaining work |
|---|---:|---:|---|---|
| 1. Setup, scoping and verification | 10 | 8 | In progress | Topic, sample windows, outcome and current model rules documented. Record instructor and teammate confirmation; student approval of frozen design remains pending. |
| 2. Literature reading and matrix | 12 | 5 | In progress | Research matrix, citation bank and literature digest exist. Read the original papers closely, verify exact RBI 2024a/2024b variable definitions and write an original literature synthesis. |
| 3. Data acquisition and cleaning | 15 | 15 | Complete | Authentic 156-month data, six groups, CFPI, subgroup source export, recovered Housing observations, discrepancy log, official spot-check and 156-row pipeline validation pass. |
| 4. Descriptive statistics and stylised facts | 12 | 10 | Corrected and substantially complete | YoY moments explicitly descriptive-only; STL-adjusted MoM moments, paired stationary bootstrap with automatic and 6/12/24 sensitivities, group/subgroup volatility comparisons generated. H2 retired as confirmatory; final economic interpretation remains. |
| 5. Decomposition and correlations | 8 | 6 | Substantially complete | Food contribution retained as accounting decomposition; covariance-aware variance decomposition generated at group and aggregate level. Do not interpret as causal. Dynamic spillover inference awaits regression. |
| 6. Econometric model and diagnostics | 15 | 8 | Pre-estimation design frozen; estimation pending | Dated v3 specification: q=3, p by BIC in 0–3, common sample, month effects, COVID pulses, delayed-lag estimand and diagnostic plan. Formal coefficient estimates and residual diagnostics remain. |
| 7. Robustness and extensions | 8 | 0 | Pending | Formal model sensitivities, reverse-direction/Granger tests, core outcome, food-ex-vegetables, sample and seasonality robustness. |
| 8. Report writing | 15 | 0 | Pending | Final five-section report must be based on verified regression results and original student synthesis. |
| 9. Final QA and submission | 5 | 0 | Pending | References, reproducibility, word count, appendix and submission package. |
| **TOTAL** | **100** | **52** |  |  |

## Claude memo gap audit — current status

| Memo item | Status now | Evidence / qualification |
|---|---|---|
| M1: YoY inference | Fixed in active outputs | YoY moments are descriptive only; iid Jarque-Bera and iid correlation inference removed. STL-MoM bootstrap is active. Old files archived. |
| M2: one-sided raw YoY lead-lag | Fixed by retirement | Legacy table archived. Formal direction is deferred to regression and bidirectional Granger tests. |
| M3: bootstrap seam/block length | Fixed with sensitivity | Paired stationary bootstrap, automatic Politis-White/PPW expected length, fixed 6/12/24 sensitivities, reported Monte Carlo resolution. Standard stationary bootstrap uses circular time indexing by definition; not the fixed circular-block procedure previously criticised. |
| M4: H2 contradicted/unfrozen | Decision fixed; student reasoning pending | H2 retired as confirmatory. STL-MoM shape comparison is explicitly exploratory. Hypotheses freeze dated 14-Nov-2026; students must fill own reasoning cells. |
| M5: primary outcome | Fixed | Group-built non-food primary; operational core pre-declared robustness. |
| M6: COVID treatment | Design/data fixed; regression test pending | Separate March–June 2020 pulse flags created. April–May collection-gap flags retained separately. Baseline and omission sensitivity remain for formal estimation. |
| M7: seasonal adjustment | Fixed at pre-estimation stage | Robust STL on log index before differencing for descriptive MoM; month indicators in baseline regression; STL regression is sensitivity. |
| R1: sample start | Fixed | Processed data preserve Jan-2013; MoM starts Feb-2013. For q=3/p<=3 common regression sample begins May-2013. |
| R2: CFPI near duplicate | Fixed as interpretation | CFPI not represented as independent robustness. Twelve food subgroups and food-ex-vegetables proxy added; proxy is derived, not official. |
| R3: core composition | Fixed as caveat | Official item weights document 3.58866% of full CPI weight retained within Miscellaneous; item-level monthly indices unavailable, so no adjusted core is fabricated. |
| R4: non-food aggregation | Fixed descriptively | Individual non-food group volatility compared with food and aggregate non-food. |
| R5: tracker arithmetic | Fixed | Current score is reconciled to 52 points from row-level credits. |

## Current active artifacts

- `data/processed/inflation_dataset.csv` — full 156 months, with YoY, MoM/log rates and COVID flags.
- `outputs/tables/yoy_descriptive_moments_no_iid_inference.csv` — YoY descriptive facts only.
- `outputs/tables/stl_mom_descriptive_moments.csv` — STL-adjusted monthly moments.
- `outputs/tables/stl_mom_paired_stationary_bootstrap.csv` — H1 and exploratory H2 differences with automatic and fixed block lengths.
- `outputs/tables/food_subgroup_stylised_facts.csv` — 12 food subgroups.
- `outputs/tables/nonfood_group_volatility_comparison.csv` — each non-food group and composite.
- `outputs/tables/covariance_aware_group_variance_decomposition.csv` — covariance-aware accounting decomposition.
- `documentation/hypotheses.md` — v3.0 dated hypothesis freeze; student reasoning pending.
- `documentation/econometric_model_specification.md` — pre-estimation model rules.
- `documentation/core_measure_composition.md` — core CPI caveat.

## Remaining work before and during formal estimation

1. Both students to complete the “Team's own reasoning” cells and confirm the pre-declared specification.
2. Read the original RBI papers' exact model sections; verify whether their ARDL variables are price levels, inflation rates or transformations thereof.
3. Estimate baseline q=3 distributed-lag model with p selected by BIC on common sample May-2013–Dec-2025.
4. Report HAC6/HAC12 inference, lagged-food joint test and delayed cumulative effect; separate same-month coefficient.
5. Run BG, ARCH-LM, BP/White, RESET, residual ACF/PACF, CUSUM/recursive stability and influence checks.
6. Estimate core, headline-built non-food, q=1/q=6, FIT, post-COVID interaction and COVID-exclusion sensitivities.
7. Run reverse-direction predictive model and Granger tests in both directions.
8. Only then write the results and policy discussion.

## Reproducible commands

```bash
python tests/test_pipeline.py
python tests/test_real_data.py
python src/spotcheck_groups.py
python src/headline_analysis.py
python src/replicate_rbi_stylised_facts.py
python src/build_dataset.py
python src/corrected_descriptive_analysis.py
python tests/test_econometric_design.py
```

## Status vocabulary

- **Validated:** source data, pipeline, schema checks and spot checks pass.
- **Corrected descriptive:** active descriptive results use current STL-MoM/stationary-bootstrap design; interpretation remains subject to review.
- **Frozen for estimation:** the model and tests are declared before formal estimation, pending student sign-off.
- **Pending:** formal regression, robust inference, literature synthesis and report.


## Stage 4 / v3.1 update (15 November 2026)
See `documentation/chatgpt_independent_tracker_stage4.md` for the authoritative independent tracker. Stage-4 specification amendments and formal q=3 baseline estimates are now included. Primary delayed-lag joint HAC test p=0.482; the delayed coefficient sum is near zero and its confidence interval includes zero. Reverse-direction, stability, leave-out and bootstrap Wald checks remain pending.
