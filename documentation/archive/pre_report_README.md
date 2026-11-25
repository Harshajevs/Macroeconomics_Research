# Food Inflation Spillovers into Non-Food Inflation (India) — HS455 Project

**Research direction:** Food inflation in India: volatility, persistence and spillovers into non-food inflation.  
**Primary CPI base:** 2012=100, All-India Combined.  
**Raw index coverage:** January 2013–December 2025 (156 monthly observations).  
**YoY descriptive window:** January 2014–December 2025 (144 observations).  
**MoM analytical window:** February 2013–December 2025 (155 observations).  
**Submission deadline:** 29 November 2026, 11:59 PM IST.

## Current data status

- The user-supplied MoSPI/eSankhyiki workbook is preserved unchanged at `data/raw/cpi_2012_combined_groups_source_export.xlsx`.
- `data/raw/cpi_2012_combined_groups.csv` is the one-row-per-month analytical input: headline CPI, six CPI groups, CFPI and published headline YoY.
- Ten Housing values missing in the supplied workbook export (Dec 2018–Sep 2019) were recovered from official monthly MoSPI/NSO press-release tables. The values and URLs are recorded in `data/raw/housing_index_recovery_sources.csv`.
- The Dec-2025 Pan/Tobacco discrepancy (export 215.9 vs official release/spot-check 215.8) is transparently reconciled in `data/raw/source_reconciliation.csv`; original workbook remains unchanged.
- The source row export includes all twelve Food and Beverages subgroups, 156 months each. Their official rounded Combined weights are stored in `data/raw/food_subgroup_combined_weights_2012.csv` and sum to 45.86%.
- Food subgroup weights support an explicitly derived food-ex-vegetables proxy. This is a researcher-derived sensitivity index, not an official MoSPI series.
- The official 2012-base item-weight table shows that the operational core CPI (excluding Food and Beverages and Fuel and Light) still retains selected vehicle-fuel and precious-metal item weights inside Miscellaneous. See `documentation/core_measure_composition.md`.
- `data/processed/inflation_dataset.csv` now preserves the full 156 raw months. YoY rates begin in Jan-2014; monthly log changes begin in Feb-2013.
- April–May 2020 require a provenance caveat: the project index levels match MoSPI/NSO's later business-continuity reconstruction with imputed components, while contemporaneous published headline YoY rates remain unavailable. Separate flags identify the collection-gap months and the two months containing imputed index components; see `data/raw/source_metadata.md` §13.
- December 2025 is provisional in the final 2012-base CPI release.

See `data/raw/source_metadata.md` for source construction and data reconciliation.

## Real data vs synthetic tests

`tests/test_pipeline.py` deliberately uses synthetic data for software unit tests only. It does not generate research estimates. `tests/test_real_data.py` validates the authentic MoSPI-derived inputs and pipeline output.

## Environment

Python 3.11+ required by the pinned NumPy/SciPy versions. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Reproduce the current pipeline

Run from the project root, in this order:

```bash
python tests/test_pipeline.py
python tests/test_real_data.py
python src/spotcheck_groups.py
python src/headline_analysis.py
python src/replicate_rbi_stylised_facts.py
python src/build_dataset.py
python src/corrected_descriptive_analysis.py
python src/stl_window_sensitivity.py
python tests/test_econometric_design.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch forward
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch core
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch reverse
python tests/test_postreview_econometrics.py
python tests/test_baseline_model.py
```

`python src/food_nonfood_stylised_facts.py` remains as a compatibility wrapper for the corrected descriptive script.

## Current methodological rules

- YoY inflation is retained for descriptive stylised facts, RBI comparisons and the 2–6% policy-band exercise. Because adjacent observations share 11 of 12 monthly changes, do not use iid Jarque–Bera p-values, iid correlation inference or iid confidence intervals on YoY series.
- Formal short-run spillover analysis is pre-specified in monthly log changes. STL is applied to log CPI levels before differencing for descriptive volatility/moment comparisons; the regression baseline uses month-of-year indicators directly.
- Food and Beverages is the primary food series; CFPI is near-duplicate and is not treated as independent validation. Food subgroup analysis (especially vegetables) is available.
- Non-food is the primary outcome and is constructed as the normalized fixed-weight index of the other five CPI groups. Core is the pre-declared robustness outcome, excluding Food and Beverages and Fuel and Light, with item-composition caveats.
- H2 (food has greater skewness/heavier tails) is retired as a confirmatory hypothesis because the original YoY descriptive results did not support it. STL-adjusted MoM moments are an explicitly exploratory retest.
- The primary delayed-lag test is the joint null on food lags 1–3; their sum is reported as an effect-size measure, while same-month co-movement is separate. No causal identification is claimed.
- The post-review model uses a pooled COVID-affected-window indicator covering March–September 2020 and the subsequent lag-exposure months through the maximum included lag. Separate robustness checks omit April–May 2020 (imputed-component months) and March 2020–December 2021 outcome rows after full-calendar lags are formed.
- The old Stage-2 YoY correlation, lead-lag, circular bootstrap and earlier specification outputs are archived under `outputs/archive/` and must not be treated as current inference outputs.

## Econometric specification status

The original v3.1 and v3.2 revisions were post-results audit responses. The active specification is v3.3, also a clearly labelled post-results revision. Its primary joint inference is a restricted-null, fixed-regressor six-month-block wild bootstrap with 4,999 draws; HAC(6), HAC(12) and HC3 are displayed as sensitivities. The primary outcome is non-food CPI, and operational core CPI (excluding Food and Beverages and Fuel and Light) is a pre-declared alternative outcome with a retained-item caveat. The q=3 model uses BIC-selected non-food own lags, month effects and a horizon-aware pooled COVID control.

**The v3.1 and v3.2 delivered packages remain preserved as prior runs.** The v3.2 specification is archived under `documentation/archive/stage4_v3.2_postresults/`; the v3.1 outputs remain archived under `outputs/archive/stage4_v3.1_pre_review/`. Active `postreview_*` outputs are v3.3 post-results estimates and must be interpreted as such. See `documentation/core_alternative_outcome_and_effect_size_v33.md` and `documentation/literature_reconciliation_nov2026.md` for the current empirical reading and literature comparison.

## Repository guide

- `data/raw/`: original source workbook/export, CPI analytic input, official weights, spot-checks and provenance logs.
- `data/processed/`: reproducibly generated full-period dataset.
- `src/`: pipeline and current corrected descriptive analysis.
- `src/archive/`: superseded Stage-2 diagnostic source code retained for audit only.
- `tests/`: synthetic unit test, real-data integration test and corrected milestone checks.
- `outputs/tables/`: current validation, descriptive, subgroup and decomposition results.
- `outputs/figures/`: current plots.
- `outputs/archive/`: superseded YoY inference and Stage-2 diagnostic outputs, clearly marked as legacy.
- `documentation/`: research design, hypotheses, trackers, limitations, data provenance, final smoke-test record, session handoff and reviewer prompt.

## Current project tracker

See `documentation/chatgpt_independent_tracker_stage4.md` for the latest Stage 5 post-review status and remaining work.


## Stage 4 / Stage 5 post-results revision v3.3
See `documentation/econometric_model_specification.md`, `documentation/post_results_revision_log.md`, `documentation/chatgpt_independent_tracker_stage4.md`, `documentation/CLAUDE_REVIEW_PROMPT_STAGE5_V33.md`, `documentation/package_validation_v3_3.md`, `documentation/core_alternative_outcome_and_effect_size_v33.md`, `documentation/literature_reconciliation_nov2026.md`, and `documentation/current_data_update_october_2026.md`. The January/August 2024 and February 2026 RBI papers test distinct forms of transmission/volatility. October 2026 observations are stored separately under `data/external/` as a 2024-base update and are not spliced into the historical 2012-base model.


## Stage 5 regression commands

After running the data and corrected descriptive pipelines, run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch forward
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch core
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch reverse`. This regenerates the v3.3 model comparison, 4,999-draw fixed-regressor block-wild joint tests, primary bootstrap-t intervals, partial sup-F bootstrap checks and the current-plus-three-lag effect-size calibration. Then run `python tests/test_v33_econometrics.py`, `python tests/test_postreview_econometrics.py`, and `python tests/test_baseline_model.py`. The separate `src/null_size_simulation.py` script reproduces the supplementary design-specific null-size experiment. Active v3.3 results are written to `outputs/model_results/`.
