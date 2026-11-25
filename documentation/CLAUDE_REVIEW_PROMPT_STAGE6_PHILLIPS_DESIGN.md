# Independent review request — HS455 Stage 6 Phillips-curve design

**Reviewer:** Claude (independent adversarial reviewer)  
**Prepared by:** ChatGPT project implementation lead  
**Date:** 17 November 2026  
**Package basis:** Stage 5 v3.3 post-results package plus new Stage 6 design notes.  
**Review type:** Pre-estimation design audit only. Do not estimate models or change project files.

## Context and governance

The team added the following Phillips-curve objective to the original food-inflation project:

> Does the negative relationship between inflation and the unemployment rate strengthen when food inflation is excluded (core inflation)? How much of the variation in headline inflation is due to food?

The second clause is already substantially addressed by v3.3. The first is a new workstream and must be tested separately. ChatGPT is the primary implementation/orchestration lead; you are the independent reviewer. Student approval is pending. Do not imply the students have reviewed or endorsed the design.

The main project rules still apply: no fabricated data, no interpolation of unemployment, no causal language for conditional associations, no silent specification changes, preserve previous package versions, and disclose AI-assisted work.

## Files to inspect

1. `documentation/phillips_curve_data_feasibility_stage6.md`
2. `documentation/phillips_curve_preanalysis_plan_stage6.md`
3. `documentation/chatgpt_independent_tracker_stage6.md`
4. `documentation/core_measure_composition.md`
5. `documentation/econometric_model_specification.md` (v3.3 food-spillover workstream; do not overwrite it)
6. `documentation/common_driver_data_assessment_v33.md`
7. `documentation/ai_usage_log.md`
8. `data/raw/plfs_urban_quarterly_ur_2018_2024.csv`
9. `data/raw/plfs_urban_quarterly_ur_source_reconciliation_stage6.csv`
10. `tests/test_stage6_plfs_ur_data.py` and `outputs/tables/stage6_plfs_ur_validation.txt`
11. `documentation/stage6_urban_cpi_acquisition_protocol.md`
12. `src/validate_stage6_urban_cpi.py` and `tests/test_stage6_urban_cpi_validator.py`

## Questions requiring adversarial review

### A. Data validity and match

- Is PLFS all-India Urban CWS unemployment, persons aged 15+, the best official quarterly unemployment series to pair with all-India Urban CPI? Does the design clearly constrain its inferential scope to Urban India rather than the full national rural-plus-urban labour market?
- Independently spot-check the source-transcribed 27-quarter CSV against the named original bulletin tables/pages where possible. Are quarter labels, age/gender/sector definition, values and overlap comparisons correct? Flag any unsupported or ambiguous source entry.
- Is the expected pre-redesign quarterly window Apr–Jun 2018 to Oct–Dec 2024 (27 observations) correctly derived from the documented coverage, and what release/revision issues may make the effective sample shorter?
- Is it correct to keep post-Jan-2025 redesigned PLFS data separate?
- Is the Urban 2012-base group-index availability claim supported? Review the documented manual Warehouse export route and the discrepancy between current eSankhyiki v2.0.0 (`getCPIData`, token optional) and the indexed older v1.0.11 Swagger (`getCPIIndex`, bearerAuth). Is the CPI acquisition protocol sufficiently robust? Is any claim about a successful API pull being made?
- Are the cited Urban group weights (36.29, 1.36, 5.57, 21.67, 5.58, 29.53) correct and the retained-group sum 58.13?
- Is the proposed weighted group-index composite a valid project operational core, and what validation against the official general index is required?
- Is the core naming caveat sufficient given the lack of 2012-base Urban item indices?

### B. Inflation and timing

- Is year-on-year log inflation computed from quarterly-average monthly CPI levels the best primary inflation measure for this small quarterly sample?
- Should quarterly inflation instead be the average of monthly YoY changes, seasonally adjusted q/q annualised change, or another well-motivated measure?
- Does the quarter alignment correctly match the PLFS CWS quarterly estimate and three-month CPI average?
- What exact treatment is appropriate for COVID quarters and possible CPI imputation?

### C. Estimand and tests

- Is the paired-difference regression `core inflation minus headline inflation` on unemployment an exact and appropriate estimator of `beta_core - beta_headline` under the matched-sample common-regressor OLS model?
- Does the direct test of the slope difference answer the question more reliably than separate regressions and separate significance tests?
- Are the sign hypotheses correctly stated, and what evidential standard should govern a claim of “strengthening”?

### D. Inference with n <= 27

- Are HC3, HAC (candidate bandwidth 3) and a paired time-block bootstrap defensible?
- How would you specify a finite-sample procedure that preserves the within-quarter covariance of headline/core inflation and serial dependence across quarters?
- Are proposed block lengths 2 and 4 quarters reasonable or should they be changed?
- Would a one-lag inflation sensitivity add useful information or mostly consume power?
- What are the key risks of trend/persistence and weak identification in this sample?

### E. Scope and work sequencing

- Is the workstream correctly prioritised and kept separate from the existing food-to-non-food pass-through models?
- Are the pending v3.3 audit and common-driver items still properly visible in the tracker?
- Are any extra analyses essential before the empirical freeze, given the 29 Nov 2026 deadline?

## Required response format

1. **Verdict:** safe to freeze / freeze after specified amendments / not safe to freeze.
2. **Blocking findings:** issues that must be fixed before collecting/estimating or freezing.
3. **Material findings:** issues that affect interpretation, inference or data validity.
4. **Minor findings:** documentation or presentation improvements.
5. **Recommended primary design:** exact unemployment series, CPI/core construction, inflation transformation, sample and slope-difference test.
6. **Recommended inference:** exact primary and secondary uncertainty procedure with finite-sample caveats.
7. **Do not do:** list any tempting but invalid shortcuts.
8. **Audit boundary:** confirm no estimates were produced and no files were changed during this review.

The Stage 6 PLFS CSV is a manual transcription from official bulletin PDFs, not an API extract or microdata re-estimation. The Urban CPI template remains blank: this review package documents a verifiable acquisition route but does not contain CPI index values. No Phillips-curve estimates have been produced.

Please do not draft the student report. The students will write the report in their own words after the evidence is settled.
