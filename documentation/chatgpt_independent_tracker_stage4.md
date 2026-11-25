# Independent project tracker — Stage 5 / post-results v3.3

**As of:** 15 November 2026  
**Active working package:** food-inflation-project-stage5-v3.3-postresults.zip (to be created after final validation)  
**Current completion:** 71/100 weighted project-progress points. This is a progress estimate, not a course grade or percentage of report pages.

| Workstream | Weight | Credited | Evidence / remaining work |
|---|---:|---:|---|
| Scope and setup | 10 | 8 | Research question and measurements established; final instructor requirement mapping remains. |
| Literature review | 12 | 8 | Direct comparison of original January/August 2024 and February 2026 RBI papers completed; common-driver and broader literature cross-check remains. |
| Data acquisition and cleaning | 15 | 15 | Authentic 2012-base CPI series, source reconciliation, weights, imputation-vintage flags and tests; October 2026 2024-base update stored separately. |
| Descriptive analysis | 12 | 11 | Stylised facts, raw/STL MoM moments, YoY descriptive treatment, subgroup analysis, stationary bootstrap and STL-window sensitivities. Shape moments are less stable than SDs. |
| Decomposition | 8 | 6 | Raw/STL covariance-aware bases and group decomposition available; interpretations remain descriptive, not causal. |
| Econometric design and baseline | 15 | 13 | v3.3 post-results inference revision, core outcome, full-calendar lag guard, horizon-aware COVID adjustment, BIC/fallback, behavioral tests and bootstrap calibration. Common-driver tier still open. |
| Formal estimation and robustness | 8 | 7 | 4,999-draw joint bootstrap tests, HAC/HC3 sensitivities, core/non-food comparison, COVID/imputation exclusions, reverse direction, partial sup-F, leave-out and stability outputs. Independent v3.3 audit pending; working-copy and clean-extraction verification pass. |
| Report | 15 | 0 | Deliberately not started; awaiting empirical claim freeze and user's LaTeX template/sample PDF. |
| Submission QA | 5 | 3 | Working-copy and clean-extraction tests, three estimator batches, deterministic null-size simulation and input/output manifests pass; independent review and instructor disclosure check remain. |

## Current evidence status

- **Food volatility:** strongly supported by the descriptive/bootstrapped analysis. Food and Beverages monthly inflation is markedly more volatile than non-food after seasonal adjustment; subgroup and covariance decomposition provide context but not causality.
- **Delayed food-to-non-food:** no robust positive average delayed association detected in the current monthly conditional model. Primary q=3 delayed sum -0.00349, HAC 95% interval [-0.04653, 0.03955], block-wild joint tail probability 0.4326.
- **Delayed food-to-core:** similarly inconclusive; operational core delayed sum -0.01882, HAC 95% interval [-0.05396, 0.01632], block-wild joint tail probability 0.4578.
- **Economic magnitude:** the current-plus-three-lag sum intervals include +0.048, the short-run sum reported by the January-2024 RBI ARDL study. The project cannot claim to rule out an RBI-sized small overall short-run association. That RBI coefficient is still not exactly comparable because of different models, samples and estimands.
- **Reverse non-food-to-food:** exploratory and sensitive to COVID treatment; block-wild tail probabilities across variants range about 0.027–0.099. No directional causal claim.
- **Post-2021 interaction:** exploratory; bootstrap tail probability 0.1542. January 2021 is an ex-post split, not a break date.
- **Stability:** partial sup-F tests restricted to food lags do not reject; no food-coefficient break date is claimed.
- **Current data:** October 2026 official CPI observation is a separate 2024-base vintage and is not appended to the old 2012-base regression.

## Preserved versions and audit trail

- v3.1 package: `food-inflation-project-stage4-v3.1.zip`; original v3.1 outputs remain archived under `outputs/archive/stage4_v3.1_pre_review/`.
- v3.2 package: `food-inflation-project-stage4-v3.2-postresults.zip`; v3.2 specification is retained under `documentation/archive/stage4_v3.2_postresults/`.
- v3.3 is an explicitly post-results revision; it does not relabel any earlier estimate as pre-estimation frozen.

## Remaining checkpoints before report preparation

1. Obtain a defensible common-driver monthly series set (preferably INR crude/oil proxy, USD/INR and policy-rate timing) from official sources, align its timing and missingness, and estimate it as a clearly labelled Tier-B sensitivity—not as a replacement for the Tier-A baseline. If source restrictions prevent a clean reproducible series, document why and do not fabricate one.
2. Complete v3.3 code/data/output reproduction and send the clean-extraction-verified v3.3 ZIP plus review prompt to Claude for an independent audit. Reconcile any material findings.
3. Freeze the empirical claims, tables, source register and limitations; then obtain the user's LaTeX template/sample PDF and begin report preparation.

## Student and academic-integrity review

Student-authored rationale, code comprehension, interpretation review and partner approval remain pending. The AI-use log is maintained. No student approval or independent student action is claimed. Before submission, students must understand and check the analysis, adapt the narrative in their own words, and follow the instructor's stated AI-use cap and disclosure requirements.
