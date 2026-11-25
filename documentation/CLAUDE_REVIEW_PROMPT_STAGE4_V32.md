# Independent review prompt — Stage 4 post-results v3.2

You are reviewing the attached `food-inflation-project-stage4-v3.2-postresults.zip` for an Indian CPI food/non-food inflation project (HS455). This is an adversarial technical audit. Please do not assume the implementation is correct because the previous review's recommendations were adopted.

## Critical context

- Stage 4 v3.1 regression outputs were already produced before your previous audit. They are preserved unchanged in `outputs/archive/stage4_v3.1_pre_review/` and are not to be overwritten.
- The active v3.2 specification and `postreview_*` results are explicitly a **post-results revision**, not a claim of a pre-estimation freeze.
- Your previous review did not estimate or evaluate the food-to-non-food coefficients. This review should inspect and independently reproduce both code and outputs.
- Do not ask students for personal notes or approvals as a prerequisite to the technical audit. Their review remains pending and is not represented as complete.

## Review tasks

1. **Reproducibility:** Extract the ZIP into a clean directory and Python environment. Confirm the stated Python/dependency requirements. Run the data pipeline, all tests, `src/stl_window_sensitivity.py` and `src/estimate_baseline.py`. Report exact commands and any warnings/errors.
2. **June 2013 protection:** Inspect `design()`. Confirm all lagged variables are made on the uninterrupted monthly calendar. Confirm October 2013 is allowed only for `max(p,q)<=3`; January 2014 protects six-lag designs and any p=0…6 fallback candidate. Test January 2014's sixth lag manually against July 2013 raw data.
3. **COVID design and index vintage:** Check the pooled `covid_affected_window` construction for q/p maxima 1, 3 and 6. Verify the new `flag_covid_imputed_series_month` in the processed dataset and inspect the April–May 2020 provenance record. The original April release is partial; the later NSO imputation note describes a continuous business-continuity reconstruction. Check that project index values match the official reconstructed All-India Combined table and that the month-level flag does not falsely imply every component was imputed. Does it cover March–September 2020 direct event rows and every subsequent outcome row whose included lags reach those months? Is pooling defensible relative to seven one-row dummies? Is the separate March-2020–December-2021 row-exclusion sensitivity genuinely distinct and correctly applied after lag construction? Check zero-column removal and matrix rank.
4. **Fallback:** Verify BIC candidates share an identical sample. Check the BG/Ljung–Box trigger, `model_df=p`, invalid LB horizons, smallest-p clearing rule and the no-candidate-clears tie-break. Test the synthetic trigger and selection functions. Assess whether the p=0…6 fallback re-estimation on Jan-2014 is internally coherent and clearly reported. Check that all candidates and the original model are saved.
5. **Inference:** Recompute the HAC(6) delayed-lag restriction for the primary model from the coefficient vector and covariance matrix. Check chi-square and F reference calculations, HAC(12), HC3 and the t-based interval for the delayed sum. Confirm q-dependent estimand labels are correct. Check whether the block-wild bootstrap design is statistically defensible and accurately named.
6. **Diagnostics/influence:** Inspect ARCH(6/12), White/BP, RESET, BG/LB, residual ACF/PACF/Q-Q, CUSUM, recursive coefficients, sup-F with 15% trimming, block-wild sup-F calibration, Cook's distance and leave-out tests. In particular, scrutinize whether the rank-aware Quandt–Andrews-style sup-F statistic and its bootstrap calibration are implemented correctly and whether the June-2021 maximum is robust or artefactual. Check the high Cook's observations (especially Sep-2023, May-2021 and Apr-2022).
7. **Economic interpretation:** Independently evaluate the primary food→non-food result, the reverse non-food→food result, the post-2021 interaction and the covariance-estimator sensitivity. Distinguish failure to reject from evidence of no effect. Do not treat reverse Granger-style predictability as causality. Assess whether the CPI basket construction/common drivers could explain the reverse-direction signal.
8. **STL sensitivity:** Check the s=7/13/25 robust windows, the s=99 near-periodic finite-window approximation and non-robust s=7. Confirm that s=99 is not described as an exact periodic STL setting and that the table stays descriptive.
9. **Documentation/freeze integrity:** Check the v3.1 archived hash against the archived original specification. Check that active v3.2 files are labelled post-results, that the README/run summary/tracker agree, and that input/output SHA-256 manifests match their files.
10. **Final verdict:** Classify findings as blocking, material, minor or optional. State which results (if any) should not be relied on and what must be corrected before the report. Do not restrict the review to document text-presence checks: inspect calculations, rerun code and test the statistical procedures.

## Baseline numbers for independent reproduction (not assumptions)

The current output reports q=3, p=1, n=147 on October 2013–December 2025; HAC(6) joint chi-square p=0.2966; F-reference p=0.3012; delayed sum beta1+beta2+beta3=-0.00349 with a 95% HAC(6) interval [-0.04653, 0.03955]. The block-wild delayed-lag tail probability is 0.425 (999 draws). CUSUM p=0.257. The 15%-trimmed sup-F statistic is 2.013 with maximum at June 2021 and block-wild bootstrap tail probability 0.050 (999 draws). These are to be independently recomputed, not accepted on trust.

The January-2014 common-sample reverse non-food→food equation selects p=2; HAC(6) joint p=0.0149, HAC(12) p=0.0237, HC3 joint chi-square p=0.1234. Post-2021 interaction HAC(6) F p=0.0595. Review all of these critically.

Return a structured memo with exact file paths, function names, numerical evidence, proposed code corrections and any alternative specification you recommend. Do not silently patch files; propose corrections first.
