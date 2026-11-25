# ChatGPT lead-session change log — Stage 2

**Date:** 14 November 2026

## Added

- `src/econometric_design_diagnostics.py`: reproducible pre-estimation diagnostics.
- `tests/test_econometric_design.py`: output schema and smoke checks.
- `documentation/econometric_design_review.md`: methodology recommendation and evidence.
- `documentation/chatgpt_independent_tracker.md`: independent project tracker and weighted completion calculation.
- `documentation/CLAUDE_REVIEW_PROMPT_STAGE2.md`: updated adversarial review prompt.

## Diagnostic work completed

- ADF and KPSS tests on CPI log levels, monthly log inflation, YoY inflation and month-effect-adjusted monthly log inflation.
- Zivot-Andrews one-break unit-root checks.
- Joint calendar-month effect tests.
- Paired non-circular moving-block bootstrap sensitivity for calendar-month-adjusted food versus non-food volatility (6, 12 and 18 month blocks; 4,999 repetitions each).
- Engle-Granger tests, ARDL bounds sensitivities under AIC/BIC lag selection, and seasonally adjusted log-level cointegration sensitivity.
- BIC selection of the non-food autoregressive lag order with a fixed food lag horizon.
- Exploratory short-run screening across full, FIT-only and April-May 2020 exclusion samples.

## Main design conclusion

Use monthly log changes with calendar-month controls for the primary short-run dynamic spillover analysis; retain YoY inflation for stylised facts. The current food-to-non-food level tests do not provide robust cointegration evidence. Do not report an ECM or long-run multiplier unless new, justified tests support cointegration. The main predictive spillover test should be the joint effect of lagged food inflation (months 1-6), separated from same-month co-movement.

## Validation

All existing project smoke tests, the new econometric design script and the new econometric design test pass in the working project folder. A second clean-extraction run is required before releasing the updated ZIP.

## Not changed

- Raw source workbook and official data files.
- The original Claude tracker.
- The core data cleaning and CPI construction logic.
- No final spillover regression has been estimated.
