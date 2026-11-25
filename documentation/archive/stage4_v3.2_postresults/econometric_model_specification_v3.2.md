# Econometric model specification — post-results revision v3.2

**Revision date:** 15 November 2026  
**Status:** Post-results methodological revision following independent audit of v3.1. This is not represented as a pre-estimation freeze. The original v3.1 code and outputs are preserved under `outputs/archive/stage4_v3.1_pre_review/` and in the original Stage 4 ZIP. New estimates are labelled `postreview_*`.

**Primary question:** Do current and lagged food-price movements predict subsequent non-food inflation in India, conditional on non-food dynamics, calendar seasonality and documented exceptional observations?

## 1. Outcome, transformations and sample windows

- Primary outcome: group-built non-food CPI monthly log change, multiplied by 100.
- Primary regressor: Food and Beverages CPI monthly log change, multiplied by 100.
- YoY analysis (January 2014–December 2025) is descriptive only because adjacent 12-month changes overlap.
- The primary q=3 specification starts October 2013. This is safe only while the maximum included lag order is at most three.
- January 2014–December 2025 is always reported alongside October 2013–December 2025. The January window is the common comparison sample for q=1, q=3 and q=6 and is also the only permitted start for any model with p or q above three.
- FIT-period sensitivity begins April 2016.
- If the residual-diagnostic fallback is triggered from the October q=3 baseline, the p=0,…,6 candidate exercise is conducted on the common January-2014 sample; its output is explicitly labelled as a fallback re-estimation. The original October BIC-selected model and all fallback candidates are retained in separate files.

## 2. June 2013 Housing step

The raw Housing index rises from 100.5 in May 2013 to 106.6 in June 2013. Its cause remains unestablished and is not guessed. The raw observation is retained. The June flag in the processed data is provenance metadata; it is not an active regressor in the October-2013 or January-2014 equations. A regression with any lag horizon above three is programmatically prevented from starting before January 2014. Thus June 2013 cannot re-enter through a fourth, fifth or sixth lag. The June observation is also checked in the leave-out audit; it is expected to be outside the primary outcome/lag window.

## 3. Dynamic equation and seasonal treatment

For the food-to-non-food direction:

\[
m^{NF}_t=\alpha+\sum_{i=1}^{p}\rho_i m^{NF}_{t-i}
+\sum_{j=0}^{q}\beta_jm^F_{t-j}
+\sum_{k=2}^{12}\gamma_kD_{k,t}
+\delta C^{covid}_t+\varepsilon_t.
\]

- Baseline q=3; q=1 and q=6 are sensitivity horizons.
- Select p by BIC over {0,1,2,3} on an identical outcome sample for every candidate.
- Include 11 month-of-year indicators with January omitted.
- A single `covid_affected_window` indicator covers March–September 2020 and every subsequent outcome month whose included lagged food or non-food regressors reach any of those event months. It extends through October 2020 for a one-month horizon, December 2020 for a three-month horizon and March 2021 for a six-month horizon.
- The control is pooled across the directly affected and lag-exposure months rather than using seven one-row pulse dummies plus a potentially single-row tail indicator. The latter can saturate observations, produce unit leverage and make HC3 covariance or Cook's distance undefined. The pooled affected-window control avoids that mechanical saturation while retaining a horizon-aware COVID adjustment.
- The regression uses raw monthly log changes plus month indicators. External oil and exchange-rate controls remain outside the Tier-A baseline; domestic Fuel and Light is not an ordinary control because it is part of non-food CPI.

## 4. COVID exclusion sensitivity

The COVID-exclusion sensitivity drops outcome rows from March 2020 through December 2021. All lags are created on the full uninterrupted calendar first; only then are outcome rows masked. This is deliberately different from the baseline event-window controls and removes the pandemic/reopening period rather than simply re-expressing the seven event rows. Any all-zero controls after masking are removed before estimation. The April–May 2020 collection-gap flags and imputed-component provenance flag remain separate source metadata and are not substituted for the event control. The project index levels for those two months follow MoSPI/NSO’s later business-continuity reconstruction; the observed-price coverage and imputation caveat is documented in `data/raw/source_metadata.md` §13.

## 5. Estimands and inference

- The delayed-lag joint null is \(H_0:\beta_1=\cdots=\beta_q=0\), tested using HAC(6).
- The primary-comparable delayed sum is beta1 for q=1 and beta1+beta2+beta3 for q=3 or q=6. For q=6 the full beta1+…+beta6 sum is additionally reported and clearly labelled; it is not substituted for the primary-comparable sum.
- beta0 is contemporaneous co-movement and is not called delayed spillover.
- The HAC quadratic-form statistic is reported under both its chi-square reference distribution and its finite-sample F transformation. These are two reference-distribution presentations of the same quadratic form, not independent robustness checks.
- HAC(6) is primary; HAC(12) and HC3 are sensitivities. Coefficient confidence intervals and p-values use residual-degrees-of-freedom t reference values. The summed-coefficient interval uses the same t convention.
- A restricted null block-wild bootstrap with six-month Rademacher blocks is reported as a further sensitivity. Its output is named a bootstrap tail probability, not a hypothesis-test p-value. The requested bootstrap count and successful replications are recorded.
- Results are conditional predictive associations. They do not identify causal transmission.

## 6. Residual-diagnostic lag fallback

1. Select p by BIC over {0,1,2,3} on the fixed October-2013 sample (for q=3) and record the original model and candidate table.
2. Check Breusch–Godfrey and Ljung–Box at lags 6 and 12. Ljung–Box uses `model_df=p`; when lag ≤ p, that Ljung–Box horizon is undefined and recorded as NA.
3. Trigger the fallback only when BG and Ljung–Box both reject at 5% at the same valid horizon (lag 6 or lag 12).
4. On trigger, re-evaluate p=0,…,6 on a common sample beginning January 2014, which prevents June-2013 exposure for p up to six. Write every candidate and the original selection to disk.
5. Select the smallest p for which all valid BG and Ljung–Box diagnostics at 6 and 12 fail to reject at 5%. No BIC tie-break is needed because p is unique under this rule.
6. If no candidate clears all valid diagnostics, select the candidate with the fewest rejected valid BG/Ljung–Box tests; break ties by BIC and then p. Report that no candidate cleared.

## 7. Reverse direction and stability

- Estimate non-food-to-food using the same January-2014 sample, monthly transformations, event controls and own-lag selection design. Report it as a reverse-direction conditional association, not a causal test.
- Report the joint HAC test of lagged predictor terms as bidirectional Granger-style predictive evidence.
- The post-2021 interaction is exploratory: it interacts the lagged food regressors with a 2021-and-later indicator and tests the interaction terms jointly. It does not assume January 2021 is a known structural break.
- Report CUSUM, recursive coefficients, and Quandt–Andrews-style sup-F with 15% trimming. The sup-F tail probability is calibrated by a six-month block-wild bootstrap under a stable-model null; no pointwise F p-value is passed off as a sup-F p-value.

## 8. Required diagnostics and influence checks

Report BG and Ljung–Box at 6 and 12; ARCH-LM at 6 and 12; White and Breusch–Pagan heteroskedasticity tests; RESET; residual ACF/PACF and Q-Q plots; CUSUM; recursive coefficients; 15%-trimmed sup-F; Cook's distance; leave-out checks for June 2013, March–September 2020, July 2023, November–December 2013 and the April–May 2020 collection/imputation months; food-lag VIF; HAC(6/12), HC3, chi-square/F reference forms and block-wild bootstrap Wald sensitivity. Undefined leverage-based diagnostics must be reported as undefined, not silently discarded.

## 9. STL sensitivity

The main volatility comparison uses robust STL (period=12, seasonal=7, trend default, low-pass default, robust=True) on log CPI levels, subtracts the seasonal component, then differences. Seasonal-window sensitivities 7, 13, 25, a near-periodic finite-window approximation (s=99), and non-robust s=7 are reported in the descriptive appendix. The s=99 case is a large-window approximation, not an exact periodic STL option. The STL-adjusted regression sensitivity retains month indicators as a separate, deliberately more conservative seasonal treatment; it is not the baseline and is reported as such.

## 10. Variance decomposition and measurement caveats

Report raw and STL-adjusted MoM bases separately with a `basis` field. YoY rows are labelled overlapping-window descriptive. Covariance shares are a composition statistic based on Cov(component contribution,total)/Var(total), include cross-covariance, and are neither causal transmission nor standalone economic importance.

Core excludes Food and Beverages and Fuel and Light but retains petrol/diesel and precious-metal items inside Miscellaneous. Item-level indices are unavailable; no adjusted-core series is fabricated. Food-ex-vegetables is a derived Laspeyres-type proxy using rounded 2012 subgroup weights, not an official CPI series. CFPI is near-duplicate and differs in coverage; interpret cautiously.

## 11. Change log

- **v3.0 (14 Nov 2026):** initial model design.
- **v3.1 (15 Nov 2026):** October-2013 start for q=3; January-2014 sample sensitivity; March–September COVID pulses; pre-declared fallback; descriptive and provenance corrections.
- **v3.2 post-results revision (15 Nov 2026):** following the independent Claude audit, corrected the >3-lag June-exposure rule; pooled COVID event-window control and added lag-exposure control through max(p,q); added distinct March-2020–December-2021 exclusion; defined Ljung–Box model degrees of freedom and fallback no-clear rule; corrected chi-square/F presentation and q-dependent delayed-sum labels; expanded diagnostics, influence checks and reverse-direction/stability analysis; reconciled status and freeze records. All v3.2 estimates are post-results revisions; v3.1 outputs remain archived unchanged.
