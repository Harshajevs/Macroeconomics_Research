# Post-review baseline results — Stage 4 v3.2

**Status:** These are post-results revised estimates following the independent audit of the first Stage 4 run. The original Stage 4 v3.1 outputs are preserved unchanged in `outputs/archive/stage4_v3.1_pre_review/`. They are not overwritten or silently reconciled with this note.

## 1. Primary q=3 food-to-non-food model

The primary model uses monthly log changes (index changes multiplied by 100), 11 month-of-year indicators, a pooled COVID-affected-window control, and non-food own lags. It covers October 2013–December 2025 (147 observations). The BIC-selected own-lag order is p=1. The residual-diagnostic fallback does not trigger: BG and Ljung–Box tests adjusted for `model_df=p` do not jointly reject at either the 6- or 12-month horizon.

| Quantity | Estimate / result |
|---|---:|
| Selected non-food own-lag order | p = 1 |
| Food lag horizon | q = 3 |
| Observations | 147 |
| R-squared | 0.3159 |
| Joint delayed-food HAC(6) Wald chi-square p | 0.2966 |
| Same quadratic form, finite-sample F p | 0.3012 |
| Delayed sum beta1 + beta2 + beta3 | -0.00349 |
| 95% t-based HAC(6) interval for delayed sum | [-0.04653, 0.03955] |
| HC3 joint chi-square p | 0.5457 |
| HAC(12) joint chi-square p | 0.2058 |
| Restricted block-wild bootstrap tail probability | 0.425 (999 successful draws) |

The joint null that the three delayed food coefficients are zero is not rejected. The delayed-sum interval contains zero and is relatively wide. This is **no persuasive evidence of a delayed food-to-non-food predictive association in this baseline**, not proof that transmission never occurs or that no other channels exist.

The contemporaneous food coefficient is 0.03773 (HAC(6) t-based p=0.0341). This is same-month co-movement, not delayed spillover. Its significance should not be re-labelled as evidence for the delayed-lag hypothesis. The three individual delayed coefficients are also not individually significant at 5% under HAC(6).

## 2. Diagnostic assessment

| Diagnostic | p-value / result | Reading |
|---|---:|---|
| Breusch–Godfrey, lag 6 | 0.5223 | No rejection |
| Breusch–Godfrey, lag 12 | 0.7235 | No rejection |
| Ljung–Box, lag 6, model_df=1 | 0.4625 | No rejection |
| Ljung–Box, lag 12, model_df=1 | 0.5621 | No rejection |
| ARCH-LM, lag 6 | 0.9984 | No rejection |
| ARCH-LM, lag 12 | 0.0610 | Close to, but above, 5% |
| Breusch–Pagan | 0.8548 | No rejection |
| White LM | 0.0714 | Close to, but above, 5% |
| RESET | 0.3245 | No rejection |
| CUSUM | p = 0.2570; 5% critical = 1.36 | No rejection |
| 15%-trimmed sup-F | 2.0126; maximizing split June 2021 | Borderline stability evidence |
| sup-F block-wild bootstrap tail probability | 0.050 (999 successful draws) | At the conventional 5% boundary; interpret cautiously |
| Maximum finite Cook's distance | 0.1398 (September 2023) | Above the 4/n screening heuristic (about 0.027); investigate influence, but do not treat the heuristic as an automatic deletion rule |

The sup-F result and CUSUM result are not identical tests. CUSUM does not reject, while the sup-F bootstrap tail probability is at the 5% boundary and the maximum statistic occurs at June 2021. Treat this as a warning to report time variation and the post-2021 interaction sensitivity—not as confirmation of a uniquely dated structural break. The bootstrap probability is Monte Carlo calibrated and carries simulation uncertainty.

The primary model has no unit-leverage observations and no undefined Cook's distances. September 2023 is the highest-Cook observation; May 2021 and April 2022 are also among the largest values. Their dedicated leave-out checks are reported below. Residual ACF, PACF and Q-Q plots, expanding-window recursive coefficient tables, and all diagnostic outputs are in `outputs/figures/model_diagnostics/` and `outputs/model_results/`.

## 3. Forward-direction robustness

| Specification | n | Selected p | HAC(6) joint p | Delayed-sum estimate | 95% HAC(6) interval |
|---|---:|---:|---:|---:|---:|
| Primary q=3, Oct-2013 start | 147 | 1 | 0.2966 | -0.00349 | [-0.04653, 0.03955] |
| q=3, Jan-2014 start | 144 | 1 | 0.3440 | -0.00441 | [-0.05152, 0.04270] |
| q=1, Jan-2014 start | 144 | 1 | 0.3497 | -0.01459 | [-0.04544, 0.01627] |
| q=6, Jan-2014 start | 144 | 1 | 0.2721 | -0.00844 (lags 1–3) | [-0.05852, 0.04165] |
| q=6 full sum, Jan-2014 | 144 | 1 | — | -0.01134 (lags 1–6) | [-0.11315, 0.09047] |
| FIT-period, Apr-2016 start | 117 | 1 | 0.3278 | -0.00308 | see model summary |
| COVID exclusion, Mar-2020–Dec-2021 rows removed | 125 | 1 | 0.6174 | -0.00426 | [-0.05414, 0.04563] |
| STL-adjusted regression sensitivity | 147 | 1 | 0.6950 | -0.00394 | [-0.07856, 0.07069] |

Across the forward specifications, the joint delayed-lag null is not rejected and the delayed-sum intervals include zero. The q=6 output reports both the three-lag comparable sum and the complete six-lag sum; they answer different horizon questions and should not be conflated.

The COVID exclusion is a genuinely distinct, broad sensitivity: outcome rows March 2020–December 2021 are omitted only after the full-calendar lags have been constructed. This leaves 125 observations. April–May 2020 are not ordinary fully observed-price months: the index levels used here match the later MoSPI/NSO business-continuity reconstruction with imputed components. A separate two-month leave-out check is reported; the source details are in `data/raw/source_metadata.md` §13. The event-window control in the baseline is instead a pooled indicator that extends past September 2020 for as long as included lagged regressors can reach the event months.

## 4. Reverse-direction and post-2021 analysis

On the common January 2014–December 2025 sample, the reverse non-food-to-food q=3 equation selects p=2. Its joint HAC(6) lagged-non-food test has p=0.0149 and the HAC(12) test p=0.0237; the HC3 joint chi-square p is 0.1234. This reverse-direction result is therefore sensitive to the covariance estimator and is exploratory. It may reflect common macroeconomic drivers, basket construction or model dynamics; it is not proof that non-food inflation causes food inflation.

The post-2021 interaction test for lagged food terms has HAC(6) F=2.5398 and p=0.0595. This is suggestive but does not meet a 5% threshold; the analysis is exploratory and is considered alongside the borderline sup-F result, not as proof of a break in January 2021.

The bidirectional comparison is written to `outputs/model_results/bidirectional_granger_style_summary.csv`.

## 5. Leave-out checks

| Exclusion | n | HAC(6) joint p | Delayed-sum estimate |
|---|---:|---:|---:|
| March–September 2020 outcomes | 140 | 0.4359 | -0.00679 |
| July 2023 | 146 | 0.3036 | -0.00323 |
| September 2023 (highest Cook’s D) | 146 | 0.4327 | 0.00547 |
| May 2021 (high Cook’s D) | 146 | 0.3852 | -0.00310 |
| April 2022 (high Cook’s D) | 146 | 0.1364 | -0.01359 |
| November–December 2013 | 145 | 0.3046 | -0.00993 |
| April–May 2020 collection-gap months | 145 | 0.4206 | -0.00550 |
| June 2013 | — | Not in primary outcome/lag sample | No exposure under the declared p,q horizon |

No leave-out variant changes the main forward-direction conclusion. The broad COVID exclusion and the seven-month event-row leave-out serve different purposes and are reported separately.

## 6. STL seasonal-window sensitivity

The STL descriptive sensitivity table is now available in `outputs/tables/stl_seasonal_window_sensitivity.csv`. For Food and Beverages, the standard deviation is 0.9883 under robust s=7, 0.9621 under s=13, 0.9801 under s=25, and 0.9869 under the robust s=99 near-periodic finite-window approximation. For Non-food, the corresponding values are 0.2418, 0.2375, 0.2377 and 0.2364. The robust window choices are fairly close to the s=7 baseline. The non-robust s=7 specification produces substantially lower standard deviations (0.7812 for Food and 0.1944 for Non-food), consistent with the sensitivity of non-robust STL to shock allocation. The s=99 case is a finite-window approximation, not an exact periodic STL setting. All entries are descriptive; no iid inference is attached.

## 7. Interpretation limits and remaining work

These models are reduced-form monthly predictive regressions, not a structural model. Food and non-food inflation may respond to common shocks, policy, expectations, wages, fuel costs and input-output linkages. The model does not isolate a causal channel. The reverse-direction result and potential time variation make this caveat especially important.

The April–May 2020 index-vintage issue is now verified against the contemporaneous partial release and the later MoSPI technical note on imputation. The index levels in this project match the later business-continuity reconstruction, not a fully observed-price series; the published headline YoY comparison fields remain blank. Continue primary-source RBI literature reconciliation and obtain student review of the empirical choices and explanations before final reporting. The LaTeX report should not be drafted as final until these items and the instructor's AI-use disclosure requirement have been checked.
