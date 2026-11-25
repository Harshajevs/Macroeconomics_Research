# Econometric model specification — v3.3 post-results revision

**Revision date:** 15 November 2026  
**Status:** Post-results methodological revision after the independent Claude audit of v3.2 and the alternative-core analysis. It is not represented as a pre-estimation freeze. The prior v3.2 specification is archived at `documentation/archive/stage4_v3.2_postresults/econometric_model_specification_v3.2.md`; the v3.2 package was separately delivered and is not overwritten. Earlier v3.1 outputs are retained in the v3.2 archive.

**Primary question:** Do current and lagged food-price movements predict subsequent non-food inflation in India, conditional on non-food dynamics, calendar seasonality and documented exceptional observations? Is the conclusion similar when the outcome is operational core inflation?

## 1. Outcomes, transformations and sample windows

- Primary outcome: group-built non-food CPI monthly log change, multiplied by 100.
- Pre-declared alternative outcome: operational core CPI monthly log change, multiplied by 100. It excludes the full Food and Beverages and Fuel and Light groups from the 2012-base CPI basket. It retains petrol/diesel and precious-metal items located in Miscellaneous; it is therefore a group-level operational core measure, not a fully item-pure core index. See `documentation/core_measure_composition.md`.
- Primary predictor: Food and Beverages CPI monthly log change, multiplied by 100.
- YoY analysis (January 2014–December 2025) is descriptive only because adjacent 12-month changes overlap.
- Primary q=3 specification starts October 2013. The minimum permissible start is calculated from the maximum lag horizon: `earliest_start = 2013-06 + max(p,q) + 1 month`. This ensures June 2013 cannot enter as an outcome or lagged regressor. For max(p,q)=3, the earliest start is October 2013; for max(p,q)=6, it is January 2014.
- January 2014–December 2025 is always reported alongside October 2013–December 2025 and is the common sample for q in {1,3,6} and p in {0,1,2,3}. Any fallback candidate with p up to 6 is also re-estimated on a common sample no earlier than January 2014.
- FIT-period sensitivity begins April 2016.
- April–May 2020 are flagged as imputed-component data-vintage months and omitted in a dedicated cross-series sensitivity; the flag does not imply that every CPI component was imputed.

## 2. June 2013 Housing step

The raw Housing index rises from 100.5 in May 2013 to 106.6 in June 2013. Its cause remains unestablished and is not guessed. The raw observation is retained. The June flag is provenance metadata, not an active regressor in the declared October-2013 and January-2014 models. The programmatic guard calculates the earliest permissible sample start from `max(p,q)` rather than relying on a fixed three-lag rule. The June observation cannot enter through longer lags in a q=6 or p=6 model.

## 3. Dynamic equation and seasonal treatment

For the forward food-to-non-food direction:

\[
m^{NF}_t=\alpha+\sum_{i=1}^{p}\rho_i m^{NF}_{t-i}
+\sum_{j=0}^{q}\beta_jm^F_{t-j}
+\sum_{k=2}^{12}\gamma_kD_{k,t}
+\delta C^{covid}_t+\varepsilon_t.
\]

The alternative core equation uses the same right-hand-side structure and timing, with operational core inflation as the dependent variable.

- Baseline q=3; q=1 and q=6 are sensitivity horizons.
- Select p by BIC over {0,1,2,3} on an identical outcome sample for every candidate. For q=1, the COVID exposure horizon is fixed at max(q, maximum candidate p)=3 so candidates do not differ in the event-control window. For q=3 it is three; for q=6 it is six.
- Include 11 month-of-year indicators with January omitted.
- A single pooled `covid_affected_window` indicator covers March–September 2020 and subsequent outcome months whose included lagged food or outcome regressors reach any event month. Its terminal month is horizon-dependent: October 2020 for max horizon 1, December 2020 for horizon 3, and March 2021 for horizon 6.
- The pooled control avoids a separate one-observation dummy for every month, which can mechanically fit individual observations and create unit leverage. The control is a parsimonious event-window adjustment, not a claim that all pandemic effects are adequately summarised by a single mean shift.
- The raw baseline uses month indicators. The STL-adjusted regression is a separate sensitivity; it does not include the pooled COVID control, and this difference is reported explicitly. The raw no-COVID-control estimate is also available as a separate specification.
- External oil and exchange-rate controls are not part of the Tier-A baseline. A common-driver extension is retained as a remaining research task before interpreting either direction economically. Domestic Fuel and Light is not treated as an external control because it is part of the non-food basket.

## 4. COVID and imputation sensitivities

- The distinct pandemic exclusion drops outcome rows from March 2020 through December 2021. Lags are constructed on the full uninterrupted calendar first; only then are outcomes masked. All-zero columns are removed before fitting.
- A shorter exclusion drops March–December 2020 outcome rows, again after full-calendar lag construction. This is separately reported because Claude found that reverse-direction inference is sensitive to this treatment.
- April–May 2020 are separately omitted in cross-series regressions because the 2012-base project levels follow MoSPI/NSO's later business-continuity reconstruction containing imputed components. This is not conflated with the broad COVID event-window control.
- Pooled event-window, March–December 2020 exclusion, March 2020–December 2021 exclusion and April–May 2020 imputation exclusions are all reported where relevant, for both directions and both outcomes. Sensitivity variants are not selected according to which produces statistical significance.

## 5. Estimands and primary inference

- Primary delayed-lag joint null: \(H_0:\beta_1=\cdots=\beta_q=0\). For the q=3 primary, this is a three-restriction test of food lags 1–3.
- The primary joint-test p-value is the restricted-null, fixed-regressor, six-month-block Rademacher wild-bootstrap tail probability of the HAC(6) quadratic-form statistic, based on 4,999 successful replications. The randomisation distribution is generated under the joint null while holding the observed design matrix fixed, including lagged dependent variables. This is not a recursive bootstrap of the full time-series data-generating process.
- HAC(6) chi-square and finite-sample F reference p-values are reported as asymptotic/reference sensitivities, not primary evidence. HC3 is reported as a separate covariance sensitivity. HAC(12) is an additional serial-correlation sensitivity.
- The supplementary `null_size_simulation.csv` is a conditional, design-specific calibration experiment with 120 Monte Carlo replications and 199 bootstrap draws per replication. It is explicitly low-resolution and not a universal size guarantee. Claude's larger independent size simulations are documented in the v3.2 audit memo and are part of the rationale for using bootstrap calibration.
- The primary-comparable delayed sum is beta1 for q=1 and beta1+beta2+beta3 for q=3 or q=6. For q=6, the full beta1+…+beta6 sum is also reported and clearly labelled.
- beta0 is contemporaneous co-movement, never called delayed spillover.
- Single linear-contrast intervals are reported using HAC-t (residual-df reference) and studentised six-month block-wild bootstrap-t intervals where available.
- The broad short-run sum beta0+beta1+beta2+beta3 is calculated separately to help calibrate the January-2024 RBI ARDL estimate. It is not identical to that paper's estimand. Both current and delayed coefficients are included in this calibration; no direct coefficient equivalence is claimed.
- A non-rejection is not evidence that the true effect is exactly zero. The intervals and economically meaningful effect sizes must be discussed. No formal equivalence test or equivalence margin was pre-registered; a post-hoc threshold may only be shown as a descriptive calibration, not as confirmatory equivalence evidence.
- All results are conditional predictive associations. They do not identify causal transmission.

## 6. Residual-diagnostic lag fallback

1. Select p by BIC over {0,1,2,3} on the fixed sample and record all candidates.
2. Check Breusch–Godfrey and Ljung–Box at lags 6 and 12. Ljung–Box uses `model_df=p`; when lag ≤ p, the horizon is undefined and recorded as NA.
3. Trigger the fallback only when BG and Ljung–Box both reject at 5% at the same valid horizon (lag 6 or lag 12).
4. On trigger, re-evaluate p=0,…,6 on a common sample beginning no earlier than January 2014, and write the original BIC-selected model and every fallback candidate to disk.
5. Select the smallest p for which all valid BG and Ljung–Box diagnostics at 6 and 12 fail to reject at 5%.
6. If no candidate clears all valid diagnostics, select the candidate with the fewest rejected valid tests; break ties by BIC and then p. State that no candidate cleared.

## 7. Reverse direction and stability

- Estimate non-food-to-food using the same January-2014 common sample, monthly transformations, event controls and own-lag selection design. It is exploratory and reported across the pooled COVID control, March–December 2020 exclusion, March 2020–December 2021 exclusion, April–May 2020 exclusion and STL variants. A variable's role in a predictive equation is not interpreted as structural causality.
- Report block-wild inference for reverse-direction joint tests alongside HC3 and HAC sensitivities. Because inference varies by COVID treatment, report the range and do not select a preferred variant by its p-value.
- The January-2021 post-period interaction is exploratory and ex-post. Its bootstrap result is reported; January 2021 is not an identified break date.
- The all-parameter sup-F profile is diagnostic only. No maximizing date is reported because the profile is plateau-like and Claude's audit found the date unstable and largely driven by seasonal/COVID nuisance coefficients.
- The stability test of interest is the 15%-trimmed partial sup-F restricted to the delayed food coefficients, calibrated by the six-month block-wild bootstrap. It tests coefficient stability; it does not search for or announce a structural break date.
- CUSUM and recursive coefficients are supporting diagnostics, not substitutes for the partial-sup-F test.

## 8. Diagnostics and influence checks

Report BG and Ljung–Box at 6 and 12; ARCH-LM at 6 and 12; Koenker Breusch–Pagan; RESET; residual ACF/PACF and Q-Q plots; CUSUM; recursive coefficients; all-parameter sup-F as diagnostic only; food-coefficient partial sup-F; Cook's distance; leave-out checks for June 2013, March–September 2020, July 2023, November–December 2013 and April–May 2020; food-lag VIF; HAC(6/12), HC3 and block-wild joint inference. White's cross-product auxiliary test is omitted because its auxiliary regression is near-saturated in this sample; do not quote its near-saturated p-value as evidence of homoskedasticity. Undefined leverage-based diagnostics must be reported as undefined, not silently discarded.

## 9. STL sensitivity

The main volatility comparison uses robust STL (period=12, seasonal=7, trend default, low-pass default, robust=True) on log CPI levels, subtracts the seasonal component, then differences. Seasonal-window sensitivities 7, 13, 25, a near-periodic finite-window approximation (s=99), and non-robust s=7 are reported in the descriptive appendix. The s=99 case is a large-window approximation, not exact periodic STL. Standard deviations are relatively stable across robust windows; shape moments, particularly non-food skewness and kurtosis, are not stable and should not be called robust. The STL-adjusted regression retains month indicators as a separate, deliberately conservative seasonal treatment, but it has no pooled COVID control; this is explicitly disclosed.

## 10. Variance decomposition and measurement caveats

Report raw and STL-adjusted MoM bases separately with a `basis` field. YoY rows are labelled overlapping-window descriptive. Covariance shares are a composition statistic based on Cov(component contribution,total)/Var(total), include cross-covariance, and are neither causal transmission nor standalone economic importance.

Core excludes Food and Beverages and Fuel and Light but retains petrol/diesel and precious-metal items inside Miscellaneous. Item-level indices are unavailable; no adjusted-core series is fabricated. Food-ex-vegetables is a derived Laspeyres-type proxy using rounded 2012 subgroup weights, not an official CPI series. CFPI is near-duplicate and differs in coverage; interpret cautiously.

## 11. Literature and current-data comparison

The literature comparison is documented in `documentation/literature_reconciliation_nov2026.md`:

- The January-2024 RBI ARDL paper estimates a short-run food-change sum of 0.048 in its non-food equation. This is not directly comparable with our delayed-only lag sum; the v3.3 note also reports beta0+beta1+beta2+beta3 for a closer but non-identical calibration.
- The August-2024 RBI paper examines expectations, producer/input costs and the RBI QPM transmission mechanism, not just a monthly CPI distributed-lag equation.
- The February-2026 RBI paper studies headline volatility, subgroup covariance and within-vegetable volatility spillovers; it does not estimate the same food-to-non-food conditional mean effect.
- October-2026 CPI observations are reported as a separate 2024-base vintage in `documentation/current_data_update_october_2026.md`. They are not spliced into the 2012-base 2013–2025 estimation sample.

## 12. Change log

- **v3.0 (14 Nov 2026):** initial model design.
- **v3.1 (15 Nov 2026):** October-2013 start for q=3; January-2014 sample sensitivity; COVID event pulses; pre-declared fallback; descriptive and provenance corrections.
- **v3.2 post-results revision (15 Nov 2026):** after Claude's audit, corrected >3-lag June exposure, pooled COVID treatment, distinct pandemic exclusion, Ljung–Box degrees of freedom, fallback selection and reporting, expanded diagnostics and reverse/stability analyses. Original v3.1 outputs remain archived.
- **v3.3 post-results revision (15 Nov 2026):** after Claude's v3.2 audit, changed primary joint inference to the restricted-null fixed-regressor six-month block-wild bootstrap; added a core alternative outcome, April–May 2020 imputation exclusions across cross-series equations, March–December 2020 sensitivities, partial sup-F for food coefficients, post-period bootstrap, common q=1 BIC exposure horizon, behavioral mutation-resistant tests, effect-size/RBI benchmark calibration and separate 2024-base October-2026 observations. The original v3.2 run is not overwritten. All v3.3 changes are post-results.
