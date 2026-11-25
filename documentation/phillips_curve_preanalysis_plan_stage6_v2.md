# Stage 6 Phillips-curve workstream — pre-analysis plan v2 (Checkpoint 1)

**Prepared:** 18 November 2026  
**Status:** Revised after Claude's 17 November adversarial audit. **Draft for independent review; not frozen. No Phillips-curve estimates have been produced.**  
**Data gate:** All-India Urban CPI file not yet acquired. State-level CPI/PLFS panel not yet collected.

## 1. Research question and scope

The combined question is whether the inflation–unemployment relationship in India is negative and whether it becomes more negative when food inflation is excluded, alongside the separate food contribution to headline inflation. Existing v3.3 results directly address the food share and food/non-food pass-through. This workstream concerns the Phillips-curve comparison only.

Any design using the quarterly PLFS CWS bulletin is an **Urban** analysis. It does not represent rural India or the full national labour market. A negative association is not necessarily causal: unemployment may be endogenous, and supply, expectations, monetary policy and other common shocks affect inflation.

## 2. Candidate data designs — decision pending independent review

### Candidate A: matched all-India Urban time series (already transcribed PLFS input)

- PLFS all-India Urban CWS unemployment, persons aged 15+, 27 quarters from 2018Q2 to 2024Q4.
- MoSPI all-India Urban 2012-base CPI General and six group indices, monthly 2013-01 to 2025-12 (not yet acquired).
- Urban group-based core excludes groups 1 Food and Beverages and 5 Fuel and Light. Retained groups 2, 3, 4, 6 use official national Urban weights normalised to 100: 2.3396%, 9.5820%, 37.2785%, 50.7999%.
- Important caveats: Housing is 37.28% of this core; Miscellaneous retains petrol/diesel and precious metals; it is not an exact RBI item-purged core.

**Identification limitation:** in the 27 UR observations, 2020Q2 alone contributes about 61.4% of total time-series variation; 2020Q2, 2020Q3 and 2021Q2 together contribute about 75.4%. Excluding those three leaves 24 observations. The remaining observations' within-sample sum of squares, re-centred on the 24-quarter mean, is 17.39% of the original 27-quarter centred sum of squares; measured around the original 27-quarter mean, the retained observations account for 24.57%. The sample variance after exclusion is 19.66% of the full-sample variance, and the unemployment rate remains strongly downward-trending (correlation -0.870 with compressed row order; -0.846 with original calendar time). These are distinct definitions, not conflicting shares. Therefore, the aggregate regression cannot be treated as a confirmatory test. Its role should be descriptive/exploratory, with the two samples shown together.

### Candidate B: state-quarter Urban panel (new feasibility route)

- PLFS Table 7: state-wise Urban CWS UR, persons aged 15+, by quarter; use the accompanying RSE table for the UR estimate from the same bulletin vintage.
- MoSPI CPI Warehouse: state-wise 2012-base Urban group/general indices available for major states from January 2013; state-specific group weights are in CPI Changes in the Revised Series, Annexure II.
- Candidate state panel template has 21 state/UT units drawn from the PLFS Table 7 and excludes Jammu & Kashmir pending the J&K/Ladakh geographic concordance review. Do not include a state until CPI coverage, PLFS Table7/RSE availability and boundary coding are confirmed.
- Construct each state's operational core from its own state-specific group weights, not the all-India Urban weights.
- **Pandemic data gap:** MoSPI says state-level CPI indices were not compiled in April and May 2020. Do not fill these with all-India imputed indices, interpolation or RBI nowcasts. Consequently, 2020Q2 quarterly average is unavailable, q/q change in 2020Q3 is also unavailable if defined against 2020Q2, and state-level YoY for 2021Q2 is unavailable because its 2020Q2 base is missing. The exact usable balanced/unbalanced panel must be computed from the received extract.
- The PLFS state-wise UR table publishes estimates and separate RSE tables. State-quarter estimates may be noisy; retain RSE and consider predeclared reliability sensitivity, not ad hoc deletion.

A state panel may address the extreme leverage of one aggregate UR time-series observation by using cross-state differences, as in the general subnational-data motivation of Behera, Wahi and Kapur (RBI WPS 08/2017). However, it is not automatically better: state CPI gaps, changing sample coverage, state boundaries, PLFS estimation uncertainty and small-cluster inference may undermine it. **Claude must recommend whether B should be primary, secondary, or abandoned.**

## 3. Inflation measures (co-primary if the data permit)

1. **Quarter-on-quarter seasonally adjusted annualised log change (q/q SAAR):** use the long monthly index history, adjust each monthly log index before quarter averaging, then take the quarterly log change and multiply by 400. The method must be robust to the April/May 2020 all-India component-specific macro-imputation flags; state-panel missing months require a separate review. Do not interpolate missing state CPI months for STL. Also inspect the January–May 2013 Urban Housing/General back-series issue: the official current series held these values at 100 before the full rent sample, while MoSPI later published a research back-series. Use the Current Series for primary CPI levels unless Claude recommends otherwise; if a back-series is used, restrict it to a clearly labelled seasonal-adjustment-history sensitivity, never splice it into the primary price level or YoY series.
2. **Year-on-year log change of quarterly-average index:** `100 * [log(mean(I in q)) - log(mean(I in q-4))]`. This avoids seasonal adjustment but adjacent quarters overlap in the underlying monthly changes (MA(3)-type dependence); with 27 observations, independent information is very limited (roughly seven non-overlapping annual windows).

Do not include an extra average of monthly YoY rates as another sensitivity: it is nearly redundant with the quarterly-average YoY series. Do not add lagged YoY inflation to the primary model; it would absorb much of the limited variation and further weaken identification.

## 4. Samples and pandemic treatment

For the aggregate PLFS time series, predeclare both:

- Full old-design sample: 27 quarters, 2018Q2–2024Q4.
- Pandemic-excluded sample: 24 quarters excluding 2020Q2, 2020Q3 and 2021Q2.

For YoY inflation, 2021Q2 must be flagged because the 2020Q2 state CPI base months are unavailable (and the all-India Urban indices in Apr/May 2020 are macro-imputed). For q/q inflation, 2020Q2 and 2020Q3 are affected by the two missing/not-compiled state months; all-India Urban CPI has imputed group/General data and must preserve the component flags.

The state panel cannot be assumed balanced. Show each state's missingness, all common-sample counts and exact exclusion rules. Do not use `dropna` silently. Never choose the pandemic window after inspecting slopes.

## 5. Estimands and model structure

For aggregate Candidate A, estimate headline and operational-core slopes using identical quarter rows and the same intercept and unemployment regressor:

`pi_H,q = a_H + b_H * U_q + e_H,q`  
`pi_C,q = a_C + b_C * U_q + e_C,q`

The direct comparison is the paired difference:

`D_q = pi_C,q - pi_H,q = a_D + delta_b * U_q + v_q`

With identical sample and regressors, OLS `delta_b` equals `b_C - b_H`. Do not compare separate p-values. Do not bootstrap headline and core independently.

For Candidate B, the comparable baseline panel equations are:

`pi_m,i,q = state_FE_i + quarter_FE_q + beta_m * U_i,q + e_m,i,q`, for `m in {H,C}`.

The direct panel difference is `D_i,q = pi_C,i,q - pi_H,i,q`, regressed on identical state and quarter fixed effects and `U_i,q`. The slope on unemployment is `delta_beta`. This identifies a **within-state, within-quarter conditional association**, not the national time-series Phillips curve. This model is a candidate only; it needs independent review of state clustering, temporal/spatial dependence, PLFS RSE and the missing-CPI pattern. A 21-unit/27-quarter panel does not license large asymptotic claims without calibration.

Do not add contemporaneous oil/exchange-rate/repo controls unless collected for each state/quarter or nationally aligned and predeclared; report them as later sensitivities. No state-level control can be invented from aggregate annual data.

## 6. Hypotheses and language rule

- H1: `beta_H < 0` (headline slope is negative).
- H2: `beta_C < 0` (core slope is negative).
- H3: `delta_beta = beta_C - beta_H < 0` (core slope is more negative).

Only describe the relationship as “strengthening” when H1 and H2 have negative point estimates, H3 has a negative point estimate, this sign pattern survives the predeclared full/excluded samples and both inflation transformations, and influence/coverage diagnostics do not show that the finding is generated by a single quarter or a small set of states. If headline slope is positive, a negative difference is not a strengthening of a negative Phillips curve.

Because null simulations show serious finite-sample size/power problems in the aggregate sample, no nominal p-value alone will be described as confirmatory evidence. Report effect sizes, uncertainty, calibration caveats and sensitivity. If the slope sign is unstable or the inference is uncalibrated, conclude “inconclusive/not supported by this sample”, not “no Phillips curve”.

## 7. Inference and calibration (not frozen)

For aggregate Candidate A, show HC3 and HAC(3/4) as sensitivity summaries only; prior synthetic audits show poor calibration. Do not promote HAC to primary. A fixed-regressor wild block bootstrap may be shown as another sensitivity, but its extreme leverage/short sample can cause severe conservatism; it is not presumed valid.

For panel Candidate B, request independent review of:
- CR2/Satterthwaite or state-clustered wild bootstrap with about 21 state/UT clusters;
- time dependence and common shocks (time fixed effects; possible cross-sectional dependence);
- two-way clustering given only 21 state/UT units and 27 quarters;
- RSE-based reliability diagnostics for the PLFS state UR input;
- null simulations using the actual state-quarter U matrix and the final missingness mask.

Before estimation, run a null-size simulation on the exact final regressors and mask, with persistent inflation error processes and appropriate cross-sectional/time dependence. Keep the DGPs and seeds recorded; do not pick the procedure with the lowest observed rejection rate. If no procedure demonstrates credible calibration, analysis remains descriptive.

## 8. Additional predeclared core sensitivity

For all-India Urban data, keep the existing four-group operational core primary. Add a no-Housing core (groups 2, 3 and 6) as a secondary composition sensitivity because Housing accounts for 37.28% of the primary core. For the state panel, use state-specific group weights and discuss Transport & Communication / Personal Care & Effects subgroup exclusions only if the actual subgroup data, official weights and sample integrity support them; do not make the larger sensitivity set an excuse for specification mining.

## 9. Diagnostics and disclosure

- Show quarterly time paths and scatter plots with pandemic periods flagged.
- Report full and excluded sample sizes, range, mean, SD, median, skewness, RSE distribution for state UR, and state coverage.
- Report leverage, variance shares, leave-one-quarter-out (aggregate) and leave-one-state-out (panel) sign checks.
- Show the full panel coverage/missingness map and balance/attrition diagnostics.
- Distinguish actual published indices, macro-imputed all-India 2020 values, state-level not-compiled months and provisional/final vintages.
- Disclose urban scope, old 2012 CPI base, PLFS old survey design, state-weight differences, housing share of core, excluded group definitions, serial dependence and low power.

## 10. Freeze gates

No regression until (i) official CPI source data and raw hash exist; (ii) all-India anchor checks / group-composite consistency pass; (iii) state-panel availability and boundary concordance are resolved if Candidate B retained; (iv) PLFS UR/RSE provenance is checked; (v) Claude has reviewed this revision; (vi) students have discussed and approved the specification; and (vii) the final plan and input manifest are frozen. No report text is drafted before claims are frozen and the students have reviewed the evidence.
