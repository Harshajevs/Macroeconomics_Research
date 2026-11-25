# Post-results revision log — Stage 4 v3.2

**Date:** 15 November 2026  
**Trigger:** Independent audit by Claude of `food-inflation-project-stage4-v3.1.zip`.  
**Status:** The original v3.1 run has been preserved. Changes below are explicitly post-results; no claim is made that v3.2 was frozen before the first regression results existed.

## Preserved original record

- Original deliverable: `food-inflation-project-stage4-v3.1.zip` (outside this package; user already received it).
- Original outputs copied unchanged to `outputs/archive/stage4_v3.1_pre_review/`.
- Exact v3.1 specification copied to `documentation/archive/stage4_v3.1/econometric_model_specification.md`.
- Its SHA-256 remains `ef410a03e0b1a14efedbd2832b53c25c7cfc6b3df86fcdfe0935880f608a7b38`; the corresponding hash record is retained beside the archived specification.

## Audit findings addressed

1. **June 2013 exposure under p/q above 3:** the design builder now raises an error if any specification with `max(p,q)>3` starts before January 2014. The q=6, p=6 January sample is tested to ensure its sixth lag reaches July 2013, not June 2013. If the q=3 October baseline ever triggers the p=0…6 fallback, every fallback candidate is re-estimated on a common January-2014 sample.
2. **Unused June pulse:** the June flag remains provenance metadata only. The active regression does not include a June pulse that could never be activated in the declared sample windows.
3. **COVID lag exposure:** the model now uses one pooled `covid_affected_window` control spanning March–September 2020 plus subsequent months whose included lagged regressors reach an event month. Its end date is computed from `max(p,q)`: October 2020 for a one-month horizon, December 2020 for a three-month horizon and March 2021 for a six-month horizon. This avoids the unpulsed October–December 2020 exposure in six-lag designs.
4. **Distinct COVID exclusion:** the sensitivity removes March 2020–December 2021 outcome rows after full-calendar lags are constructed. All-zero event controls are removed. This is not algebraically identical to the baseline event-window specification.
5. **Fallback reproducibility:** Ljung–Box uses `model_df=p`; invalid horizons where lag ≤ p are explicitly NA. Trigger wording is both BG and LB rejecting at the same valid horizon. The fallback chooses the smallest p clearing all valid diagnostics. If none clears, it minimizes the count of failed valid tests, then BIC, then p. Original and all candidate tables are written to disk.
6. **Wald/F inference:** the code calculates a HAC quadratic form, reports its chi-square reference p-value and its finite-sample F transformation, and makes clear these are not independent robustness tests. HC3 is calculated separately. Coefficient intervals and p-values consistently use a residual-df t reference convention.
7. **Lag-sum labels:** q=1 is labelled beta1; q=3 is beta1–beta3; q=6 reports both the three-lag comparable sum and the full beta1–beta6 sum.
8. **Expanded diagnostics:** ARCH-LM(6/12), White and Breusch–Pagan, RESET, residual ACF/PACF and Q-Q, CUSUM, recursive coefficients, 15%-trimmed sup-F with block-wild bootstrap calibration, influence tables and leave-out checks were added. Reverse direction, post-2021 interactions and an aligned bidirectional comparison were estimated.
9. **Status consistency:** README, run summary, specification and tracker now distinguish the original pre-results v3.1 outputs from the active post-results v3.2 estimates. README requires Python 3.11+ for the pinned dependency set.
10. **Audit protection:** behavioural tests now exercise lag alignment, sample guards, COVID masking, all-zero control removal, Ljung–Box degrees of freedom, a synthetic fallback trigger and both branches of the fallback-selection rule.
11. **April–May 2020 CPI vintage:** verified the initial reduced-basket release and the later MoSPI/NSO imputation note. The source index levels in the project match the later business-continuity reconstructed table. The processed file now has a separate month-level flag for April–May imputed components; it does not imply every series component was imputed. April–May-only and broad pandemic exclusions are both documented.

## Important methodological change: pooled COVID control

The seven one-row pulse indicators in the first implementation could fit each event month perfectly. In some specifications this caused unit-leverage observations and undefined HC3/Cook's-distance calculations. The revised model pools the March–September event months and the subsequent lag-exposure months into one affected-window indicator. This is a post-results modelling decision. It is made explicit rather than presented as a clerical correction.

## New estimation status

- Active estimator: `src/estimate_baseline.py`.
- Active estimates: `outputs/model_results/postreview_*`.
- Main summary: `outputs/model_results/postreview_model_comparison_summary.csv`.
- Interpretation: `outputs/model_results/BASELINE_RESULTS_NOTE.md`.
- Inputs and source-code hashes: `documentation/postreview_input_manifest_v3_2.sha256`.
- Output hashes: `documentation/postreview_output_manifest_v3_2.sha256`.

The post-review estimates are not a replacement for the original evidence record. They are the updated, audit-responsive specification and should be reviewed independently before being treated as final.

---

# Post-results revision v3.3 — 15 November 2026

**Trigger:** Independent Claude audit of the v3.2 package.  
**Preservation:** The complete v3.2 package was retained as the prior deliverable. The active v3.2 specification has been copied to `documentation/archive/stage4_v3.2_postresults/`; v3.3 results are generated under new `postreview_*` labels. No v3.2 result file is intentionally overwritten in the delivered v3.3 archive (the working folder is a cloned successor package).

## Main changes

1. Changed the primary joint-inference procedure from asymptotic HAC Wald reference p-values to a restricted-null, fixed-regressor, six-month-block Rademacher wild-bootstrap tail probability with 4,999 successful replications. HAC(6), HAC(12) and HC3 remain visible sensitivities. The fixed-regressor conditioning and limitations are stated explicitly.
2. Added an alternative dependent variable, operational core CPI excluding Food and Beverages and Fuel and Light, with the retained-item caveat in `core_measure_composition.md`.
3. Re-estimated core and non-food forward equations on the primary and common January-2014 samples and on q=1/q=6, COVID exclusion, and April–May imputed-month exclusion variants.
4. Added a more comparable current-plus-three-lag sum, beta0+beta1+beta2+beta3, and bootstrap-t interval to calibrate—but not equate—the January-2024 RBI ARDL short-run sum of 0.048.
5. Ran a 4,999-draw partial sup-F test restricted to food-lag coefficients for both non-food and core outcomes. Stopped presenting the full-parameter sup-F maximising month as a structural break date.
6. Added bootstrap inference for the post-2021 interaction and reverse-direction variants; reverse results remain treatment-sensitive and exploratory.
7. Added a supplementary design-specific null-size simulation, behavioural tests for five previously surviving mutations, fixed the June-start formula, common q=1 BIC COVID horizon, dropped-row pandemic variants and April–May 2020 exclusions.
8. Replaced near-saturated White cross-product diagnostic reporting with Koenker Breusch–Pagan; documented that the STL regression sensitivity does not apply the pooled COVID control.
9. Added direct RBI literature reconciliation and a separate October-2026/2024-base CPI data update. Current data are not spliced into the historical 2012-base model.
10. Added refreshed AI-use log, tracker, model comparison output, interpretation note and reviewer prompt.

## v3.3 central estimates

- Food → non-food q=3 October-2013: p=1, n=147; bootstrap joint-test tail probability 0.4326; delayed sum -0.00349; HAC 95% interval [-0.04653, 0.03955].
- Food → operational core q=3 October-2013: p=1, n=147; bootstrap tail probability 0.4578; delayed sum -0.01882; HAC interval [-0.05396, 0.01632].
- Both models' delayed-food partial sup-F tests do not reject stability (bootstrap tail probabilities 0.2496 and 0.8276, respectively).
- Current-plus-three-lag sum intervals include +0.048 for both outcomes. This prevents a claim that all RBI-sized small short-run associations are ruled out.
- Reverse direction and post-2021 interaction remain exploratory; no causal direction or break date is claimed.

## Remaining limitations

- The block-wild bootstrap is fixed-regressor and therefore conditions on observed lagged dependent variables; it is not a fully recursive bootstrap. The conditional-null simulation is design-specific and relatively low resolution (120 Monte Carlo repetitions and 199 inner bootstrap draws); Claude's independent larger simulations remain the stronger audit evidence.
- The custom core index is group-level and retains some fuel/precious-metal content inside Miscellaneous.
- The operational common-driver extension (INR crude, exchange rate and policy-rate controls) remains a research task before any economic interpretation of reverse-direction associations. The Tier-A results are conditional predictive associations only.
- A further Claude audit of the full v3.3 code, data, results and citation-level literature reconciliation is pending.
