# Stage 6 — Phillips-curve comparison: proposed pre-analysis plan

**Prepared:** 17 November 2026  
**Status:** Draft for team discussion and independent Claude review. **Not frozen; no Phillips-curve regressions have been run.** The 27-quarter PLFS unemployment input has been transcribed and source-checked; matched Urban CPI data remain outstanding.  
**Research objective:** test whether the inflation–unemployment relationship is more negative when food inflation is excluded.

## 1. Research question and relationship to the existing project

The combined project question is:

1. Does the negative relationship between inflation and unemployment in India become stronger when food inflation is excluded and inflation is measured using core CPI?
2. How much of the variation in headline inflation is attributable to food?

The second question is already substantially addressed by the v3.3 covariance-aware variance decomposition. The first is a separate empirical question and has not yet been estimated. The food-to-non-food/core distributed-lag analysis is a supporting workstream: it studies conditional predictive co-movement between price-basket components, not the Phillips Curve itself.

The economic motivation is that supply-driven food-price changes may move headline inflation even when labour-market slack has not changed in the same direction. A food-excluded measure could therefore have a clearer relationship with labour-market tightness. This is the hypothesis to test, not a result established by the earlier variance decomposition or spillover regressions.

## 2. Hypotheses and estimands

Let \(\pi^H_q\) denote quarterly Urban headline CPI inflation, \(\pi^C_q\) denote quarterly Urban operational-core inflation, and \(U_q\) denote the all-India Urban PLFS CWS unemployment rate for persons aged 15 years and above in quarter \(q\).

Separate descriptive slopes are:

\[
\pi^H_q=\alpha_H+\beta_H U_q+\varepsilon^H_q,
\qquad
\pi^C_q=\alpha_C+\beta_C U_q+\varepsilon^C_q.
\]

**Directional expectations:** \(\beta_H<0\) and \(\beta_C<0\). The central comparative estimand is:

\[
\Delta\beta=\beta_C-\beta_H.
\]

A stronger negative relationship under core inflation requires \(\Delta\beta<0\). The primary comparative null is no steepening, \(H_0:\Delta\beta=0\), against the pre-stated directional alternative \(H_1:\Delta\beta<0\). A result should only be described as evidence of strengthening if the estimated difference is negative and its uncertainty is sufficiently inconsistent with zero. A negative point estimate alone is not enough.

The separate signs of \(\beta_H\) and \(\beta_C\) must also be shown. A more negative core slope is not, by itself, proof that both series exhibit a negative Phillips-curve relationship.

## 3. Primary sample and variable definitions

### 3.1 Geography and unemployment measure

Use matched all-India Urban data. This means the study estimates an **Urban India** relationship, not a rural-plus-urban national Phillips Curve. The unemployment variable is the official quarterly PLFS CWS unemployment rate for persons aged 15 years and above. Do not substitute annual usual-status estimates, interpolate monthly unemployment or blend the pre-2025 and redesigned post-2025 survey series.

The source-transcribed PLFS input covers April–June 2018 through October–December 2024 (27 quarterly observations). This is the maximum unemployment calendar, not yet the final regression sample: the Urban CPI input and all inflation transformations must be validated before the matched sample size can be stated.

### 3.2 Headline and core inflation

- Headline: official MoSPI all-India Urban CPI General Index, base 2012=100.
- Core: Urban operational core formed by fixed-weight aggregation of Pan/Tobacco, Clothing/Footwear, Housing and Miscellaneous group indices, using official Urban weights normalised to sum to 100. Food and Beverages and Fuel and Light are excluded.
- Core label: always write “Urban operational core (excluding Food and Beverages and Fuel and Light groups)” at first use. It is not an exact item-purged RBI core because petrol/diesel and precious metals embedded in Miscellaneous cannot be removed from the old-base Urban group-only series.
- Inflation: primary rate is the year-on-year log change in the quarterly average index, \(100[\ln(\bar I_q)-\ln(\bar I_{q-4})]\). The same calendar-quarter comparison reduces recurring within-year seasonality and keeps both outcomes on a common transformation.

Monthly Urban CPI inputs should be averaged within quarter before calculating year-on-year inflation. A pre-specified sensitivity can average the three monthly year-on-year log inflation rates instead. The final transformation must be agreed before examining its relationship with unemployment.

### 3.3 Common sample

Both inflation outcomes and unemployment must use exactly the same quarter rows. Any missing quarter in any required variable removes that quarter from both outcome regressions; do not let the headline and core estimates use different samples.

## 4. Primary model and direct slope-difference test

The two headline/core regressions use the same unemployment variable, intercept and quarters. The primary comparison can therefore be estimated directly using the paired inflation difference:

\[
D_q=\pi^C_q-\pi^H_q
     =\delta_0+\Delta\beta U_q+\eta_q.
\]

With identical sample and regressors, the OLS slope in this paired-difference regression is exactly \(\widehat\beta_C-\widehat\beta_H\). This is preferable to deciding that slopes differ because one separate regression is significant and the other is not. It also preserves the within-quarter dependence between headline and core outcomes.

Report all of the following:

1. \(\widehat\beta_H\) and \(\widehat\beta_C\), with units (percentage points of annual inflation per one-percentage-point increase in the unemployment rate);
2. \(\widehat{\Delta\beta}\), its confidence interval and direct test;
3. Pearson and Spearman correlations as descriptive summaries, not as substitutes for the slope test;
4. R-squared values, clearly described as in-sample fit and not as evidence of slope steepening;
5. scatterplots with fitted lines, clearly showing the small number of quarterly observations.

The initial primary model is intentionally parsimonious. The 27-quarter Urban sample is too small to justify a large control set. Any conclusion must be scoped to the urban labour market and cannot be generalised to rural India or to the entire national labour force without additional evidence. Do not add controls based on which specification gives the desired sign or p-value.

## 5. Inference plan — provisional pending Claude review

Quarterly CPI year-on-year rates and macroeconomic series can be serially dependent, while the sample is very short. Ordinary iid OLS standard errors and a simple comparison of separate p-values are not appropriate as the only inference.

The proposed reporting stack for the paired-difference slope is:

- HC3 standard errors and confidence intervals as a small-sample heteroskedasticity-robust reference;
- Newey–West/HAC standard errors with a small, pre-declared quarterly bandwidth (initial candidate: 3 lags, with 1- and 2-lag sensitivities), explicitly acknowledging that these estimates are fragile at \(n\leq27\);
- a paired time-block bootstrap that resamples the joint quarterly vector \((\pi^H_q,\pi^C_q,U_q)\), never resampling headline and core separately. Candidate expected block lengths of 2 and 4 quarters can be compared as sensitivity, not selected after looking at the coefficient.

No one inference method should be declared definitive before the independent reviewer examines finite-sample behaviour for this exact short sample and regression. The final method, bandwidth and bootstrap procedure must be written into the frozen plan before estimation. Report the point estimate and interval even when no test rejects; do not interpret failure to reject as evidence of no Phillips relationship.

## 6. Limited, pre-declared sensitivity checks

1. **Alternative quarterly aggregation:** quarterly average of monthly YoY log inflation versus YoY log change in quarterly average CPI.
2. **Pandemic sensitivity:** retain the full old-method sample as the starting specification; separately check a pre-declared exclusion of 2020Q2 and a broader pandemic window (provisionally 2020Q2–2020Q3). Before running this check, verify the Urban CPI data-vintage/imputation note and PLFS bulletin fieldwork notes for the relevant quarters.
3. **Dynamic sensitivity:** at most one lag of the relevant inflation measure may be tested as an explicitly secondary specification. It is not the primary model because the sample is small and adding dynamics reduces observations and power. Report the lag choice and sample change transparently.
4. **Post-2025 observations:** a separate descriptive appendix may show the redesigned monthly/quarterly PLFS period alongside the newer CPI base, but it must not be joined to the main 2012-base old-method regression.
5. **Influence:** show leave-one-quarter-out slope-difference estimates or an influence diagnostic. Do not delete an observation from the primary specification merely because it is influential.

The sensitivity list is a proposed maximum, not permission to add exploratory specifications without logging them.

## 7. Diagnostic and interpretation rules

- Plot all three series and inspect time paths before estimation.
- Report sample size, min/max, mean, standard deviation, median and correlations.
- Examine influential observations and pandemic-quarter sensitivity.
- Check whether the small sample is dominated by trend or a small number of extremes. Unit-root tests may be displayed as low-power diagnostics, not used as a mechanical switch to select a favourable model.
- If a trend-adjusted or gap-based measure is proposed, create a separate, fully documented sensitivity with an explicit method; do not replace the unemployment rate in the main question silently.
- The regression measures conditional association. It does not identify the causal effect of unemployment on inflation.
- With at most 27 observations, statistical power will be low. A wide interval or non-rejection must be described as inconclusive, not proof that the Phillips Curve is absent or that food exclusion has no effect.
- A stronger core slope is compatible with a weaker headline relationship only if the paired difference is directly supported. The 90.59% food variance share is motivation for this test, not proof of the expected slope difference.

## 8. Pre-estimation gates

| Gate | Requirement | Status |
|---|---|---|
| A. Data | PLFS 27-quarter bulletin transcription and Urban 2012-base CPI group data validated | PLFS portion complete; CPI portion pending |
| B. Measurement | Quarterly aggregation, operational-core formula and common sample fixed | Drafted; pending data check and team discussion |
| C. Independent review | Claude reviews the data choices, model, difference test and short-sample inference before estimation | Pending |
| D. Team understanding | Both students can explain the unemployment measure, core formula, slope contrast and limitations | Pending |
| E. Freeze | Versioned specification with date and SHA-256 hash | Pending |
| F. Estimation | Run only against the frozen specification; any later changes labelled post-results | Not started |

## 9. Explicitly prohibited interpretation

Do not claim that:

- the Phillips Curve is proven in India because a bivariate coefficient is negative;
- core inflation has a stronger Phillips relationship solely because its p-value is smaller than headline's;
- food inflation causes the headline Phillips curve to flatten based on variance decomposition alone;
- the operational group-exclusion core is identical to RBI's item-excluded core;
- a statistically insignificant estimate proves the slope is zero;
- the 2025 PLFS redesign observations are directly comparable with the old quarterly urban PLFS series without a separately justified bridge.

## 10. Review question for Claude

Please review the accompanying `CLAUDE_REVIEW_PROMPT_STAGE6_PHILLIPS_DESIGN.md` as an independent adversarial reviewer. The requested review is of source feasibility, variable definitions, sample construction, the paired slope-difference estimand and short-sample inference. **Do not estimate models or edit the project in the review pass.** Return blocking/material/minor findings and a clear recommendation on whether this design is safe to freeze.
