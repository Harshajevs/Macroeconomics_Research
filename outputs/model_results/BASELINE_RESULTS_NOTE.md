# Baseline results and interpretation — v3.3 post-results revision

**Date:** 15 November 2026. **Status:** Post-results revision following Claude's v3.2 audit. The prior v3.2 package and the v3.1 results remain preserved. All estimates are conditional predictive associations, not causal effects.

## 1. Primary model and inference

The primary model regresses monthly non-food CPI log inflation (times 100) on contemporaneous and three lagged Food and Beverages inflation changes, BIC-selected non-food own lags, month-of-year effects and a horizon-aware pooled COVID-affected-window control. The October 2013 q=3 sample selects p=1 and has n=147. January 2014 is also reported; q=1 and q=6 sensitivities use a common January-2014 start.

Following Claude's size audit, the primary joint test is a restricted-null, fixed-regressor, six-month-block Rademacher wild-bootstrap tail probability of the HAC(6) quadratic-form statistic (4,999 draws). HAC(6), HAC(12) and HC3 are reported as sensitivities. The bootstrap holds the observed regressors fixed, including lagged dependent variables; it is not a recursive bootstrap.

## 2. Main results: food-to-non-food and food-to-core

| Outcome | n | p | HAC(6) joint chi-square p | HAC(6) F-reference p | HC3 joint p | 4,999-draw block-wild tail probability |
|---|---:|---:|---:|---:|---:|---:|
| Non-food | 147 | 1 | 0.2966 | 0.3012 | 0.5457 | 0.4326 |
| Operational core | 147 | 1 | 0.4495 | 0.4523 | 0.7553 | 0.4578 |

The q=3 delayed sum is:

| Outcome | Delayed sum β1+β2+β3 | HAC-t 95% interval | Studentised block-wild bootstrap-t 95% interval |
|---|---:|---:|---:|
| Non-food | -0.00349 | [-0.04653, 0.03955] | [-0.04470, 0.03911] |
| Operational core | -0.01882 | [-0.05396, 0.01632] | [-0.05100, 0.01420] |

Neither model detects a systematic positive average delayed food association. The intervals include zero; this is not proof of no effect. The operational core measure excludes the full Food and Beverages and Fuel and Light CPI groups but retains some vehicle-fuel and precious-metal components inside Miscellaneous. It is a fixed-weight group-level core measure, not item-pure core. See `documentation/core_measure_composition.md`.

## 3. Contemporaneous and short-run effect size

The non-food contemporaneous food coefficient is 0.03773 (HAC(6) coefficient p=0.0341), but its single-coefficient block-wild bootstrap tail probability is 0.0548. It is borderline and represents same-month co-movement, not delayed spillover. The core contemporaneous coefficient is approximately 0.03683, with block-wild tail probability 0.1828.

A separate current-plus-three-lag sum calibrates the January-2024 RBI ARDL result:

| Outcome | β0+β1+β2+β3 | Studentised block-wild bootstrap-t 95% interval |
|---|---:|---:|
| Non-food | 0.03424 | [-0.02581, 0.09259] |
| Operational core | 0.01801 | [-0.04073, 0.07441] |

The January-2024 RBI article's 0.048 is a short-run sum of food-change terms in an ARDL non-food equation. It is not identical to our delayed-only coefficient sum or to our fixed-q regression. Both current-plus-lag intervals include 0.048. Therefore, do not claim that this project rules out an RBI-sized small total short-run association.

## 4. Pre-declared sensitivities

`postreview_model_comparison_summary.csv` contains 20 forward, alternative-outcome and reverse-direction model variants. The forward non-food and core delayed-lag bootstrap tail probabilities remain above conventional rejection thresholds across the reported q/sample/period/COVID/imputation/STL variants. Selected examples:

| Sensitivity | Non-food block-wild tail probability | Core block-wild tail probability |
|---|---:|---:|
| January-2014 q=3 | 0.5156 | 0.4154 |
| January-2014 q=1 | 0.4024 | 0.3852 |
| January-2014 q=6 | 0.5528 | 0.6226 |
| Exclude April–May 2020 imputed months | 0.4966 | 0.5760 |
| Exclude March 2020–December 2021 | 0.7824 | 0.4502 |
| Exclude March–December 2020 (non-food) | 0.6380 | — |
| STL-adjusted non-food (no pooled COVID control) | 0.7806 | — |

The FIT-period model's bootstrap tail probability is 0.5610. All model definitions and confidence intervals are retained in the comparison CSV and individual summary files.

## 5. Partial stability test

The food-lag-only partial sup-F statistic is 2.4505 for non-food; its 4,999-draw block-wild tail probability is 0.2496. For core, the statistic is 0.8406 and the tail probability is 0.8276. These tests restrict the break to food-lag coefficients, unlike the earlier full-parameter sup-F, whose date profile was plateau-like and driven largely by seasonal/COVID nuisance coefficients. No break date is identified or reported.

## 6. Reverse direction and post-2021 interaction

The non-food-to-food direction remains exploratory:

| Reverse specification | Bootstrap tail probability |
|---|---:|
| Pooled COVID window | 0.0798 |
| Exclude March–December 2020 | 0.0274 |
| Exclude March 2020–December 2021 | 0.0794 |
| Exclude April–May 2020 | 0.0642 |
| STL-adjusted, no pooled COVID control | 0.0994 |

This sensitivity is material; it does not establish a robust reverse causal mechanism. It must not be called structural Granger causality.

The post-2021 interaction HAC(6) F-reference p-value is 0.0595; the 4,999-draw block-wild tail probability is 0.1542. January 2021 is an ex-post split, not an identified break date. No evidence of a changed food-lag relationship is claimed.

## 7. Diagnostics and calibration

For the primary non-food equation, BG(6/12) p-values are approximately 0.522/0.723 and Ljung–Box(6/12, model_df=1) values approximately 0.462/0.562. ARCH-LM(6/12) p-values are approximately 0.998/0.061; Koenker Breusch–Pagan p is approximately 0.855; RESET p is approximately 0.354. White cross-product LM is omitted because its auxiliary regression is near-saturated.

Claude's independent conditional-null experiments found HAC Wald over-rejection in these designs. The local supplementary simulation (120 Monte Carlo repetitions, 199 bootstrap draws per test) likewise shows HAC(6) rejection rates of 17.5% under iid sign errors and 12.5% under six-month block sign errors, versus 4.2%/1.7% for HC3 and 2.5%/4.2% for the block-wild procedure. Wilson intervals are wide; the local experiment is design-specific and low-resolution, not a universal guarantee. See `null_size_simulation.csv`.

## 8. Research interpretation and limitations

The January 2024, August 2024 and February 2026 RBI studies address distinct estimands: ARDL short-run mean-inflation association; expectations, cost-channel and QPM transmission; and volatility/covariance and within-vegetable spillovers. The project's non-significant delayed coefficient does not refute the broader expectations or cost mechanisms in the August 2024 paper, nor the volatility findings in February 2026. See `documentation/literature_reconciliation_nov2026.md`.

October 2026 CPI observations use the new 2024 base and remain a separate current-data update. They are not used in this historical 2012-base regression. See `documentation/current_data_update_october_2026.md` and `data/external/`.

The defensible claim is bounded: the current conditional monthly model does not detect a robust positive average delayed food-to-non-food or food-to-core association. It does not establish a zero effect, rule out small contemporaneous/total short-run associations, test all expectation/cost channels, or identify causal transmission. The external common-driver tier remains pending before any interpretation of either directional equation as an economic mechanism.
