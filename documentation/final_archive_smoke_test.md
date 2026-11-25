# Final archive smoke-test record — Stage 3

**Date:** 14 November 2026  
**Archive:** `food-inflation-project-stage3-corrected.zip`  
**Method:** Extracted the ZIP into a new directory and ran the README pipeline from the extracted project root.

## Result

**All commands passed in the fresh extraction.**

| Command | Result | Scope |
|---|---|---|
| `python -m compileall -q src tests` | PASS | Syntax compilation |
| `python tests/test_pipeline.py` | PASS | Synthetic data only; software unit test |
| `python tests/test_real_data.py` | PASS | Authentic CPI inputs and real-data build validation |
| `python src/spotcheck_groups.py` | PASS | Dec-2024, Nov-2025 and Dec-2025 official group spot-checks |
| `python src/headline_analysis.py` | PASS | Headline YoY reconciliation and policy-band calculations |
| `python src/replicate_rbi_stylised_facts.py` | PASS | Descriptive comparison with RBI Feb-2026 headline stylised facts |
| `python src/build_dataset.py` | PASS | Rebuild 156-month analytical dataset |
| `python src/corrected_descriptive_analysis.py` | PASS | STL, bootstrap, subgroup, group-volatility and decomposition outputs |
| `python tests/test_econometric_design.py` | PASS | Stage-3 design, output, weights, bootstrap and archive-state checks |

## Real-data validation highlights

- 156 raw and processed monthly index observations, Jan-2013 to Dec-2025.
- 144 YoY observations in the Jan-2014 to Dec-2025 descriptive window (April and May 2020 remain missing only in the published headline YoY field; derived group rates are separately identified).
- 155 MoM changes in the Feb-2013 to Dec-2025 window.
- The three official spot-check months match the selected headline, six-group and CFPI indices exactly.
- Computed headline YoY differs from the published series by at most 0.005 percentage points on published observations.
- Four March–June 2020 pulse indicators and two April–May 2020 collection-gap flags are present.
- Corrected descriptive analysis completes and writes all declared tables and figures.
- The Stage-3 econometric/design test confirms the frozen specification and does not claim that a spillover regression has been estimated.

## Important interpretation

The synthetic unit test is a code-path test only; it is not an empirical finding. The real-data integration test and official spot-check validate the authentic CPI data pipeline. All current Stage-3 descriptive and design tests pass. The formal distributed-lag spillover regression and its residual diagnostics remain the next milestone.

A full console transcript was retained separately as `STAGE3_FRESH_EXTRACTION_SMOKE_TEST.log` in the working output directory.
