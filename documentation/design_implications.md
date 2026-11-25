# Design implications and implementation decisions — v3.0

1. Use YoY inflation for policy-band counts and descriptive comparison with RBI papers; do not use iid p-values or confidence intervals on overlapping YoY observations.
2. Use seasonally adjusted monthly log changes for descriptive volatility and distributional comparisons. STL is applied to log indices before differencing.
3. Use month-of-year indicators directly in the baseline regression, with March–June 2020 pulse indicators.
4. Keep group-built non-food CPI as the primary dependent variable and operational core as robustness. Document that core retains certain vehicle-fuel and precious-metal weights inside Miscellaneous.
5. Retire H2 as confirmatory; the YoY stylised facts do not support it. Any MoM skewness/kurtosis comparison is exploratory.
6. Use the 12 official food subgroup series for additional stylised facts and a derived food-ex-vegetables proxy. Do not call the proxy an official MoSPI series.
7. Compare each non-food group with food before interpreting the food-vs-composite volatility gap; aggregate diversification can lower non-food volatility.
8. Use covariance-aware contribution-to-variance shares for group decomposition; do not describe them as causal spillovers.
9. Baseline regression q=3; choose own lags p by BIC from 0–3 on a common sample; use q=1 and q=6 sensitivities.
10. The primary delayed-spillover test is the joint HAC test of food lags 1–3; the primary effect-size is their sum. Same-month co-movement is separate.
11. Do not include domestic Fuel and Light as an ordinary control in the non-food equation. Oil/FX external controls are deferred to a validated Tier-B model.
12. No ECM/long-run multiplier is a primary claim unless a defensible cointegrating relationship is established. The previous food-to-non-food level tests were not robust.
13. Keep a reproducible audit trail and do not replace raw source observations.
