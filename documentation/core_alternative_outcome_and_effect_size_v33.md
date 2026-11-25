# Core alternative outcome, effect-size assessment and claim boundaries — v3.3 post-results

**Date:** 15 November 2026  
**Status:** Post-results extension of the v3.2 analysis. All v3.2 files remain preserved in the original package; v3.3 outputs are additive and do not overwrite the earlier run.

## 1. Purpose and construction

The primary outcome remains the group-built non-food CPI index. The alternative outcome is the project's operational core CPI, a fixed-weight group aggregate excluding Food and Beverages and Fuel and Light from the 2012-base CPI basket. It is constructed using the same official group indices and fixed weights. This is a group-level operational core measure, not an item-pure core series: petrol/diesel and precious-metal items remain within the Miscellaneous group. The source workbook does not provide item-level monthly indices needed to remove these items. The limitation is documented in `documentation/core_measure_composition.md`.

Both outcomes use the same food predictor, monthly log-change transformation, full-calendar lag construction, month-of-year effects and horizon-aware pooled COVID treatment. The same p-selection and q-comparison rules are applied. Cross-series models additionally exclude April–May 2020 as a sensitivity because the later NSO business-continuity data vintage contains imputed components for those months.

## 2. Core and non-food results

The q=3 October-2013 baseline selects p=1 in both outcome equations (n=147).

| Outcome | HAC(6) joint chi-square p | Restricted-null 6-month block-wild tail probability (4,999 draws) | Delayed sum β1–β3 | 95% HAC-t interval |
|---|---:|---:|---:|---:|
| Non-food | 0.2966 | 0.4326 | -0.00349 | [-0.04653, 0.03955] |
| Operational core | 0.4495 | 0.4578 | -0.01882 | [-0.05396, 0.01632] |

Studentised six-month block-wild bootstrap-t intervals are [-0.04470, 0.03911] for non-food and [-0.05100, 0.01420] for core. Both include zero. Partial sup-F tests restricted to the delayed food coefficients find no instability: bootstrap tail probability 0.2496 for non-food and 0.8276 for core (4,999 draws). These tests do not identify or justify reporting a break date.

The result is stable across the main pre-declared variations:

- January-2014 common sample: non-food bootstrap joint tail probability 0.5156, delayed sum -0.00441; core 0.4154, delayed sum -0.02509.
- q=1 and q=6 horizons on January-2014 common sample: all food-lag joint bootstrap tail probabilities exceed 0.38 for both outcomes; cumulative estimates remain negative and confidence intervals include zero.
- April–May 2020 imputed-month exclusion: non-food tail probability 0.4966, core 0.5760.
- March 2020–December 2021 exclusion: non-food 0.7824, core 0.4502.
- STL-adjusted non-food sensitivity (no pooled COVID control is applied to this transformed series): bootstrap tail probability 0.7806, delayed sum -0.00394, HAC 95% interval [-0.07856, 0.07069]. The transformed-series sensitivity is reported with that treatment caveat.

These are non-rejections, not proof of a zero effect. They indicate that this model does not detect a stable average delayed association in the studied sample.

## 3. Economic magnitude and relation to the RBI 2024 estimate

The January-2024 RBI article reports a short-run food-change coefficient sum of 0.048 in its ARDL non-food equation. That coefficient is the article's sum of short-run ΔFood terms; it is not directly the same estimand as our delayed-only β1+β2+β3 sum. Direct comparison would conflate contemporaneous and delayed effects and ignore differences in model, sample, index construction and controls.

For a closer, but still not identical, calibration, we separately calculate the sum including contemporaneous and three delayed food terms, β0+β1+β2+β3:

| Outcome | β0+β1+β2+β3 | Studentised block-wild bootstrap-t 95% interval |
|---|---:|---:|
| Non-food | 0.03424 | [-0.02581, 0.09259] |
| Operational core | 0.01801 | [-0.04073, 0.07441] |

Both intervals include +0.048. Therefore the project cannot claim to rule out an RBI-sized small **overall short-run** association. The delayed-only intervals do not establish a positive delayed effect, but they are not a formal equivalence test and no equivalence margin was pre-registered. We should not describe the evidence as demonstrating “no spillover” or as excluding all economically meaningful effects.

The appropriately bounded interpretation is:

> In the monthly 2012-base CPI sample, the estimated conditional delayed food-to-non-food and food-to-core associations are small and statistically inconclusive across the declared specifications. The results do not show a robust average delayed relationship. However, uncertainty remains, and the broader current-plus-lag short-run multiplier is compatible with a small positive magnitude similar to the short-run sum reported in the January-2024 RBI ARDL study. This is not evidence that the true relationship is zero.

## 4. Inference revision after Claude's v3.2 audit

Claude's conditional-null simulations found conventional HAC(6) multi-parameter Wald tests rejected substantially more often than their nominal 5% rate in the tested project designs (approximately 11–17%); the result persisted under iid and six-month block-sign error designs and in further GARCH/AR-error experiments. We therefore no longer use an asymptotic HAC Wald p-value as primary inference for joint food-lag tests.

The v3.3 primary joint-test reference is a restricted-null, fixed-regressor, six-month-block Rademacher wild bootstrap applied to the HAC(6) quadratic-form statistic, with 4,999 replications. HAC(6) and HC3 p-values are displayed as sensitivities. Single linear contrast intervals are reported using HAC-t and studentised block-wild bootstrap-t intervals. The bootstrap conditions on the observed regressors, including lagged dependent variables; it is not a full recursive data-generating-process bootstrap. Its scope and assumptions are stated explicitly.

A supplementary conditional-null simulation in this package uses only 120 Monte Carlo replications and 199 bootstrap draws per replication. In this design-specific check, HAC(6) rejects at 17.5% under iid sign errors and 12.5% under six-month block-sign errors; HC3 rejects at 4.2% and 1.7%; the block-wild bootstrap rejects at 2.5% and 4.2%. Wilson intervals are wide because of the modest number of simulations. This small experiment is supporting evidence, not a universal size guarantee; Claude's larger independent simulations are recorded in the audit memo.

## 5. Directional and stability findings

The reverse non-food-to-food model is exploratory only. Across pooled COVID, dropped March–December 2020, dropped March 2020–December 2021, April–May 2020 exclusion and STL variants, its block-wild joint-test tail probability ranges from 0.027 to 0.099. The conclusion is sensitive to event-window treatment and therefore does not establish a robust reverse mechanism. No causal or structural Granger-causality language is used.

The post-2021 interaction is also exploratory. Its HAC(6) F reference p-value is 0.0595, but its block-wild bootstrap tail probability is 0.1542. January 2021 was selected as an ex-post split; it is not an identified break date. The all-parameter sup-F maximum is not reported as a break date because its profile is plateau-like and appears driven by seasonality/COVID-related nuisance coefficients. The food-coefficient-only partial sup-F does not reject stability.

## 6. Diagnostics and caveats

- White's cross-product auxiliary test is omitted because the auxiliary regression is near-saturated. Koenker's Breusch–Pagan test is reported instead.
- The STL-adjusted regression is a sensitivity and does not include the pooled COVID control; this is explicitly noted. The raw forward model's no-COVID-control sensitivity is shown separately.
- The June-2013 data discontinuity cause remains unestablished. The programmatic earliest-start guard uses the full maximum lag horizon.
- April–May 2020 are imputed-component data-vintage months and are omitted in dedicated cross-series sensitivities.
- No causal interpretation is supported. Results are conditional predictive associations in aggregate monthly data.
