# Hypotheses, tests and post-results decision record

**Original design record:** v3.1 (15 November 2026).  
**Active operational analysis:** v3.3 post-results revision; see `econometric_model_specification.md`. This is not a claim of a new pre-estimation freeze. Earlier result revisions and their reasons are retained in `post_results_revision_log.md`. Team-authored reasoning and partner approval remain pending; no student approval is claimed.

## Research questions

1. Is seasonally adjusted monthly food inflation more volatile than non-food inflation?
2. Do current and lagged food-price movements predict subsequent non-food inflation, conditional on non-food persistence, calendar seasonality and documented shock periods?
3. Does the forward result remain similar when the dependent variable is the operational core CPI excluding Food and Beverages and Fuel and Light?
4. Is there evidence of reverse non-food-to-food predictive association, or of a change in the lag relationship after 2021?

## H1 — food inflation volatility

**Statement:** Food inflation is more volatile than non-food inflation after seasonal adjustment.

**Evidence:** Paired stationary-bootstrap confidence intervals for the standard-deviation difference and log standard-deviation ratio. Support requires the 95% interval for the difference to lie above zero (and/or the log ratio interval above zero). This is a descriptive volatility comparison, not a causal statement.

**Working rationale for study:** Food prices are exposed to harvest conditions, weather, perishability and supply interruptions, while non-food combines several categories whose movements may offset one another. Comparing seasonally adjusted monthly volatility helps isolate the scale of price movements after removing recurring calendar patterns.

## H3 — delayed food-to-non-food association

**Statement:** Lagged food inflation is positively associated with subsequent non-food inflation, conditional on non-food's own lags, month effects and a pooled horizon-aware COVID control.

**Primary q=3 estimand:** joint null \(H_0:\beta_1=\beta_2=\beta_3=0\); effect size \(\beta_1+\beta_2+\beta_3\). The contemporaneous coefficient \(\beta_0\) is reported separately and is not interpreted as delayed spillover.

**Active post-results inference:** restricted-null, fixed-regressor, six-month-block Rademacher wild-bootstrap tail probability using 4,999 replications is primary for joint tests. HC3 and HAC(6)/HAC(12) are reported as sensitivities; HAC-t and studentised bootstrap-t intervals are used for linear contrasts. The change from the earlier HAC-primary rule follows the independent v3.2 audit's conditional-null size experiments. See specification v3.3 §5 and `outputs/model_results/null_size_simulation.csv`.

**Current reading:** The non-food delayed-lag joint null is not rejected (bootstrap tail probability 0.4326), and the delayed sum is -0.00349 with 95% HAC-t interval [-0.04653, 0.03955]. Its core-outcome counterpart is also not rejected (bootstrap tail probability 0.4578), with delayed sum -0.01882 and interval [-0.05396, 0.01632]. This is not proof of a zero effect. The current-plus-three-lag sum intervals include +0.048, so the analysis does not rule out a small positive overall short-run association similar in magnitude to the January-2024 RBI ARDL estimate. See `core_alternative_outcome_and_effect_size_v33.md`.

**Working rationale for study:** Food-price changes may influence non-food prices through input costs, transport and distribution expenses, wage and household-budget responses, and inflation expectations. These channels need not operate immediately, motivating a lagged conditional association test. Common shocks may affect both baskets, so the estimate is predictive rather than causal.

## Alternative outcome — operational core

Core is a pre-declared robustness outcome, not a separate causal estimand. It excludes the complete Food and Beverages and Fuel and Light groups from the 2012-base CPI basket, but retains some petrol/diesel and precious-metal items within Miscellaneous. The data source does not provide monthly item-level indices needed to remove those items. This construction caveat must accompany every reference to core.

## Reverse direction — exploratory

Non-food-to-food tests are hypothesis-generating. Bootstrap tail probabilities vary across COVID treatment and STL variants (approximately 0.027–0.099 in v3.3), and the result is not interpreted as evidence that non-food inflation causes food inflation. It is not described as structural Granger causality.

## Post-2021 interaction — exploratory

January 2021 is an ex-post interaction split, not a known break date. The HAC(6) F-reference p-value is 0.0595, while the block-wild bootstrap tail probability is 0.1542. The result does not establish a change in the lag relationship. The food-lag partial sup-F test also does not reject stability.

## Retired / exploratory hypothesis

**H2 (retired as confirmatory):** “Food inflation has greater skewness/heavier tails than non-food inflation.” The original YoY descriptive moments did not support it (food skewness -0.30; excess kurtosis -0.48). YoY moments remain descriptive because adjacent 12-month windows overlap. STL-adjusted MoM moment differences are reported as exploratory; shape moments vary materially with STL seasonal-window choices.

## Descriptive-only measures and exclusions

- YoY mean, median, SD, skewness and excess kurtosis: descriptive only; no iid inference on overlapping 12-month changes.
- Headline 2–6% band counts: YoY headline inflation only.
- Food contribution to headline CPI and covariance-aware variance decomposition: accounting/statistical decomposition, not causal transmission.
- CFPI: near-duplicate robustness measure, not independent validation.
- October 2026 CPI: separate 2024-base vintage; it is not appended to the 2012-base 2013–2025 regression sample.

## Approval and AI-use record

The working rationales are draft study notes. They are not evidence that both students have personally reviewed or approved the wording. Partner confirmation and instructor feedback must be recorded separately. AI-assisted code, research synthesis and editing are documented in `ai_usage_log.md`; students must verify the analysis, understand the methods, rewrite/adapt their submitted narrative in their own words, and comply with the instructor's AI-use limit and disclosure requirements.
