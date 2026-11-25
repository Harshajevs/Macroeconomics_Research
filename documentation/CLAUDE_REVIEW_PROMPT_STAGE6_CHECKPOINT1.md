# CLAUDE ADVERSARIAL REVIEW — HS455 Stage 6 Checkpoint 1

**Date:** 18 November 2026  
**Package:** `food-inflation-project-stage6-checkpoint1.zip`  
**Role:** Independent reviewer. Do not modify project files, do not estimate any Phillips-curve regression, and do not imply student approval.

## Review objective

Adversarially review the Stage 6 amendments made after your 17 November 2026 report, and decide whether the project is safe to proceed to official data acquisition and whether the proposed state-level panel is defensible. We are not asking you to agree with ChatGPT's changes. Identify any missed defect, unsupported claim, inadequate test, invalid threshold, selection issue, or new specification risk.

## Inputs to inspect

1. Your prior audit, supplied separately by the user.
2. `documentation/claude_stage6_audit_reconciliation_checkpoint1.md`.
3. `documentation/phillips_curve_preanalysis_plan_stage6_v2.md`.
4. `documentation/state_panel_feasibility_stage6.md`.
5. `src/validate_stage6_urban_cpi.py` and `tests/test_stage6_urban_cpi_validator.py`.
6. `src/stage6_aggregate_null_size_simulation.py` and its generated CSV.
7. PLFS all-India input/reconciliation and aggregate leverage diagnostics.
8. The three state-panel templates and All-India CPI/anchor templates.
9. README/checkpoint notes, AI-use log and tracker.
10. `documentation/stage6_urban_cpi_acquisition_protocol.md` and `documentation/stage6_api_version_assessment.md` (new API-version distinction).

## Part A — B1 through B6 remediation

For each blocking issue B1–B6, grade it `closed`, `partly closed`, `open`, or `incorrectly handled`. Recompute B1 directly from the 27 UR values. Check both the compressed-rank and original calendar-time correlation after dropping the three pandemic quarters; distinguish the 17.39% within-subsample re-centred SS share from the 24.57% retained SS around the original full-sample mean and the 19.66% sample-variance ratio. Check that Q2 2021 and the Apr/May 2020 CPI gap are treated differently for YoY and q/q measures.

### B3 null-size simulation

Reproduce the Monte Carlo script from scratch. Verify the outcome processes (iid q/q-like; four-quarter overlapping MA; AR(0.5) innovations plus overlap; random walk), the use of the fixed observed UR regressor, the HAC calendar-lag kernel and df, HC3 implementation, sample masks, seed, and Monte Carlo standard errors. Identify any weakness in the DGP, estimator or interpretation. Do not regard low rejection rate as proof of validity. Recommend whether any procedure can support inferential claims for the aggregate sample.

### B5 validator

Inspect all tests and mutation-test the validator with at least these failures: rates in place of levels, General three times larger than group aggregate, tenfold Housing spike, Fuel copied from Food, missing anchor, anchor value mismatch, bad raw SHA, false April/May flags, invalid date, mixed raw hashes, wrong sample period, and wrong sector/base/vintage. Check whether the 0.50 index-point composite tolerance is justified or should be loosened/changed to a diagnostic-only gate pending the actual Urban export. Does the current validator correctly separate warning flags from blocking errors? Are eight anchors adequate, and are all anchor months practically source-verifiable?

## Part B — State-level panel feasibility

This is a new candidate, not a frozen specification. Evaluate critically:

1. Is the candidate intersection of 21 state/UT units correctly drawn from PLFS Table 7 and MoSPI major-state CPI availability? What about J&K/Ladakh, Andhra Pradesh/Telangana, Delhi and other UT boundaries?
2. Does PLFS Table 7 have the same 15+ person CWS definition and all quarters in all bulletin vintages? Is the matching UR RSE table identifiable and extractable in every bulletin? Should state-quarter weights/reliability thresholds be used?
3. Is state-wise 2012-base Urban CPI group/general coverage available for all 21 state/UT units and the full monthly period? Confirm the state CPI not-compiled months and all resulting quarter-level consequences. Also scrutinise the distinction between current eSankhyiki v2.0.0 `getCPIData` (catalogued as open/guest access) and the older token-based `getCPIIndex` user manual / Swagger. Are the parameter schemas actually interchangeable? What exact low-risk test should be run before bulk acquisition?
4. Are state-specific weights from Annexure II valid for constructing a fixed-weight operational core? Should the group-weighted aggregate be validated against state General within a tolerance?
5. Does a state-FE/time-FE panel identify a useful within-state, within-quarter relationship? How should cross-sectional dependence and time dependence be handled with approximately 21 state clusters and 27 quarters? Is CR2/Satterthwaite or a wild cluster bootstrap credible? What design-specific null simulation should be run?
6. Could PLFS state UR RSE be so high in some state-quarter cells that the panel is unreliable? The Oct–Dec 2024 bulletin's Delhi Person RSE is 27.3% in Oct–Dec 2023 and 26.5% in Jul–Sep 2024; assess the full RSE distribution and recommend a predeclared sensitivity without cherry-picked deletion. Recommend transparent inclusion/weighting sensitivity, avoiding cherry-picked state deletion.
7. Should Candidate B be primary, secondary or rejected? Explain what it actually estimates and whether it answers the wording of the assignment better than the aggregate 27Q design.

## Part C — v3.3 integrity and historical work

Confirm the original v3.3 input/output manifests and archives have not been changed by Stage 6 updates. Confirm all v3.3 numerical outputs remain untouched. If you find manifest failures, list exact path and expected/actual hash; do not repair the archive.

## Part D — precise deliverable

Return a structured report with:

1. Overall verdict and whether Checkpoint 1 is safe for data collection.
2. A B1–B6 and M1–M7 disposition table.
3. Independent reproduction of the unemployment leverage statistics and null-size simulation (include seed, replications, code differences, Monte Carlo error).
4. Validator mutation-test matrix (pass/fail and defects not caught).
5. State panel recommendation with a specific data/inference gate list.
6. Any new material concerns.
7. Exact changes required before Checkpoint 2; distinguish mandatory from optional.

Do not produce or guess any inflation or Phillips-curve estimates: no actual Urban CPI dataset is included. The CPI files in this package are templates only. Do not rewrite code. Students' review/approval remains pending.
