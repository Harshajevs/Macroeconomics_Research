# Econometric model specification — v3.1 pre-estimation freeze

**Version:** 3.1  
**Date:** 15 November 2026  
**Status:** Pre-estimation design amended following independent review. No food-to-non-food regression has yet been estimated.
**Primary question:** Do current and lagged food-price movements predict subsequent non-food inflation in India, conditional on non-food dynamics, calendar seasonality and documented exceptional observations?

## 1. Outcomes, transformations and windows

- Primary outcome: group-built non-food CPI monthly log change, multiplied by 100.
- Primary regressor: Food and Beverages CPI monthly log change, multiplied by 100.
- YoY analysis (January 2014–December 2025) is descriptive only.
- Monthly descriptive data begin February 2013, but the **primary common regression window begins October 2013**. This excludes June 2013 and the three subsequent outcomes (July–September) that would carry the June observation through up to three own lags.
- January 2014–December 2025 is a co-primary sample sensitivity, not merely a footnote.
- q=6 sensitivity uses a common window beginning January 2014 so q=1,3,6 can be compared on identical observations.
- FIT-period sensitivity begins April 2016.

## 2. June 2013 Housing step

The raw Housing index rises from 100.5 in May 2013 to 106.6 in June 2013. The cause is not established and must not be guessed. The raw observation is retained. A June 2013 pulse is available in the processed data for transparent sensitivity work. The primary regression starts October 2013 to prevent the June observation entering the dependent variable or its three own lags. The January 2014 start is reported as a pre-declared sensitivity. STL estimates near the sample endpoint are treated cautiously; the primary regression uses raw monthly changes with month indicators, not STL-adjusted outcomes.

## 3. Baseline model

\[m^{NF}_t=\alpha+\sum_{i=1}^{p}\rho_i m^{NF}_{t-i}+\sum_{j=0}^{3}\beta_jm^F_{t-j}+\sum_{k=2}^{12}\gamma_kD_{k,t}+\sum_{r=Mar}^{Sep}\delta_rC_{r,t}+\eta J_{Jun2013,t}+\varepsilon_t.\]

- Select p by BIC over {0,1,2,3}, with a fixed common estimation sample.
- Baseline q=3; sensitivities q=1 and q=6.
- Month indicators: 11 calendar-month dummies, January omitted.
- COVID event pulses: March through September 2020. These cover both outcome shocks and the subsequent three months in which March–June food observations can enter lagged regressors.
- June 2013 pulse is retained for sensitivity and diagnostic comparisons; it is outside the October 2013 primary window.
- Do not include domestic Fuel and Light as an ordinary control because it is part of non-food CPI. External oil and exchange-rate controls remain a separate extension after source validation.

## 4. COVID row-mask rule

The primary model retains all source observations and includes March–September 2020 pulse indicators. In the COVID-exclusion sensitivity, construct all lagged variables on the uninterrupted full monthly calendar first, then mask outcome rows March–September 2020. **Never delete months before creating lags**, because doing so would misalign time. The separate April–May 2020 MoSPI collection-gap flags are metadata, not substitutes for the event pulses.

## 5. Primary estimand and inference

Primary delayed association: \theta_{1:3}=\beta_1+\beta_2+\beta_3. Confirmatory null: H0: \beta_1=\beta_2=\beta_3=0. Report beta0 separately as contemporaneous co-movement. The four-month sum is secondary. Primary covariance: Newey-West/HAC with six lags; sensitivity 12 lags, HC3, an F-form test and a block/wild-bootstrap Wald test. Interpret as conditional predictive association, not causal transmission.

## 6. Pre-declared lag fallback

First select p by BIC over {0,1,2,3} on the fixed common sample. Then test residual serial correlation using both Breusch-Godfrey and Ljung-Box at lags 6 and 12. If **both** tests reject at 5% at either lag horizon, expand the candidate set to p in {0,...,6} and select the smallest p that clears both tests, breaking ties by BIC. Report the original BIC-selected model and every fallback candidate. Do not use BG alone: cross-check it because isolated outliers can make it sensitive. This rule is fixed before seeing food coefficients.

## 7. Reverse direction and stability

Estimate the reverse equation using the same sample and event treatment. Run bidirectional Granger-style joint tests. The post-2021 interaction is a secondary exploratory stability analysis; add sup-F/Quandt-Andrews with 15% trimming alongside CUSUM. Do not treat January 2021 as a uniquely determined structural break.

## 8. Descriptive methods

- YoY moments and plots are descriptive only because adjacent 12-month changes overlap. No iid p-values or confidence intervals.
- Main volatility comparison uses robust STL (period=12, seasonal=7, trend default, low-pass default, robust=True) on log CPI levels, subtracts the seasonal component, then differences.
- Report STL seasonal-window sensitivities 7, 13, 25, near-periodic, and non-robust s=7; the non-robust result is sensitivity only because shocks may be absorbed into seasonality.
- Regression baseline uses raw monthly log changes plus month indicators; STL-adjusted regression is a separate sensitivity. State these are different seasonal treatments.
- Paired stationary bootstrap uses shared indices. Report expected block lengths 1, 2, 3, 6, 12 and 24 as relevant sensitivities. The Politis-White selector targets the sample mean; for SD statistics also inspect dependence in squared deviations. The code's finite-sample floor/rounding are local modifications and are not claimed to be exact unmodified Politis-White output. Tail probability is a bootstrap percentile tail probability, not a hypothesis-test p-value.

## 9. Variance decomposition

Report raw and STL-adjusted MoM bases separately with an explicit `basis` field. YoY rows are labelled overlapping-window descriptive. Covariance shares are a composition statistic based on Cov(component contribution,total)/Var(total), include cross-covariance, and are not causal transmission or standalone economic importance.

## 10. Core and food subgroup definitions

Core excludes Food and Beverages and Fuel and Light but retains petrol/diesel and precious-metal items inside Miscellaneous. Item-level indices are unavailable; no adjusted-core series is fabricated. Food-ex-vegetables is a derived Laspeyres-type proxy using rounded 2012 subgroup weights, not an official CPI series. CFPI is a near-duplicate and differs in coverage; interpret cautiously.

## 11. Required diagnostics and influence checks

BG and Ljung-Box at 6 and 12; ARCH-LM at 6 and 12; White/Breusch-Pagan; RESET; residual ACF/PACF and Q-Q; CUSUM, recursive coefficients and sup-F; Cook's distance and leave-out checks for June 2013, March–September 2020, July 2023, November–December 2013; VIF among food lags; HAC 6/12, HC3, F-form and bootstrap Wald; reverse-direction tests. q=1,3,6 comparisons use a common sample.

## 12. Change log

- **v3.0 (14 Nov 2026):** initial pre-estimation design.
- **v3.1 (15 Nov 2026):** B2 June-2013 Housing step addressed by October-2013 primary start and January-2014 co-primary sensitivity; B3 COVID pulses extended through September and row-mask rule specified; B4 serial-correlation fallback rule pre-declared; B1 stale figures archived; B5 selector modifications documented; B6 variance decomposition basis split; B7 AI-use log updated; B8 version hash recorded after freeze.
