# Literature reconciliation: Indian food inflation, spillovers and volatility

**Prepared:** 15 November 2026  
**Purpose:** distinguish the estimands and methods in the central RBI studies from the project's own monthly conditional-predictive regressions. This is an evidence comparison, not a claim that the designs are interchangeable.

## 1. RBI Bulletin, January 2024

**Reference:** Patra, M. D., John, J. and George, A. T. (18 January 2024), *Are Food Prices the ‘True’ Core of India’s Inflation?*, RBI Bulletin.  
**Official source:** https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=22323

### Question and method

The article examines whether food inflation displays core-like properties, including volatility, persistence, spillovers and cyclical sensitivity. Its food/non-food spillover section uses seasonally adjusted monthly data from January 2011 to October 2023 and an ARDL cointegration/bounds-testing framework (Pesaran et al., 2001), estimated with the Kripfganz–Schneider ARDL module in Stata.

### Results relevant to this project

The article reports a positive, statistically significant short-run sum of food-inflation change coefficients in the non-food equation: **ΣΔFood = 0.048**, significant at 5%. The corresponding sum of non-food changes in the food equation is **-0.136** and is not marked statistically significant. The bounds-test F-statistic is 7.424 (5% significance) for the non-food equation and 5.050 (10% significance) for the food equation. The error-correction term is 0.009 and not significant in the non-food equation, while -0.080 is significant at 1% in the food equation. The authors describe the short-run food coefficient as low in magnitude and argue that large and persistent food shocks are more likely to affect non-food prices.

### Comparison with this project

Our principal 2012-base sample is October 2013–December 2025, with a January 2014 common-sample sensitivity. It estimates a finite distributed-lag equation in monthly log changes, includes month-of-year indicators and a pooled COVID-affected window, selects non-food own-lag order by BIC and uses a fixed-regressor block-wild bootstrap for joint inference. It does not estimate a cointegrating long-run relationship or an error-correction model.

For the October-2013 non-food model, the primary delayed food-lag sum (β1+β2+β3) is -0.0035; its HAC(6) 95% interval is [-0.0465, 0.0395], and its 4,999-draw fixed-regressor block-wild bootstrap-t interval is [-0.0447, 0.0391]. The joint delayed-lag bootstrap tail probability is 0.4326. The core-outcome delayed sum is -0.0188, with HAC(6) 95% interval [-0.0540, 0.0163] and bootstrap-t interval [-0.0510, 0.0142]; the joint bootstrap tail probability is 0.4578.

These delayed-only estimates do **not** directly replicate the RBI table's ΣΔFood coefficient, which is a short-run distributed-change sum in an ARDL setting and may include contemporaneous as well as lagged changes. To avoid a false apples-to-apples claim, the project separately reports β0+β1+β2+β3. That broader short-run sum is 0.0342 for non-food (bootstrap-t 95% interval [-0.0258, 0.0926]) and 0.0180 for core ([-0.0407, 0.0744]); both intervals include 0.048. Thus, this project does not rule out an RBI-sized total short-run association. What it does find is no robust evidence for a systematic positive **delayed-only** three-month association in its own specification.

## 2. RBI Bulletin, August 2024

**Reference:** Patra, M. D., John, J. and George, A. T. (19 August 2024), *Are Food Prices Spilling Over?*, RBI Bulletin.  
**Official source:** https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=22787

### Question and method

This article is broader than a direct food-to-non-food monthly lag regression. It analyses the changing persistence of food inflation, its relationship with household inflation expectations, correlations with manufacturing/services price indicators, and food-price pass-through in the RBI's semi-structural Quarterly Projection Model (QPM).

- A time-varying parameter framework allows the persistence coefficients, trend and shock volatility to change over time; parameters are estimated by Bayesian MCMC on monthly data from January 2011 to June 2024.
- The expectations equation relates household inflation expectations to year-on-year food inflation, the inflation target and the policy repo rate, using quarterly data from 2012-13 to Q1 2024-25. The food inflation coefficient is 0.12 (p=0.047); the estimated long-run elasticity is 0.22. The repo-rate coefficient is negative (-0.31) but only marginal at p=0.097, so it should not be described as significant at the conventional 5% level. The dynamic multiplier suggests that an isolated food-inflation shock affects expectations for up to two quarters.
- Quarterly correlations for Q1 2012 to Q2 2024 connect food inflation and inflation expectations to PMI input/output price measures and a less-formal service-charge index. These are correlations, not causal pass-through estimates.
- The QPM has distinct food, fuel and core inflation blocks and an expectations-augmented Phillips curve. Its historical decomposition attributes upward pressure on core inflation to food-price spillovers, particularly from 2022-23 and with a rise in Q1 2024-25; the article argues that restrictive monetary policy offset much of this pressure.

### Comparison with this project

The RBI article identifies potential channels that our bivariate monthly CPI design does not separately estimate: inflation expectations, wage/cost pressures, service charges, output pricing and monetary-policy responses. Our reduced-form lag equation asks a narrower question: whether monthly food CPI changes predict subsequent non-food/core CPI changes after conditioning on the outcome's own lags and calendar effects. A non-significant direct lag coefficient cannot rule out transmission through expectations or input-cost channels, especially when policy responses offset price pressure before it appears in the measured CPI outcome.

## 3. RBI Bulletin, February 2026

**Reference:** Mohan, R., Hasan, S., Sarkar, S. and John, J. (20 February 2026), *Retail Inflation Volatility in India: Sources, Determinants, and Implications*, RBI Bulletin.  
**Official source:** https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23980

### Question and method

The study uses the earlier CPI-Combined 2012=100 series and focuses on the sources and transmission of **inflation volatility**, not the mean food-to-non-food lag coefficient. Its coverage of the flexible inflation-targeting period is 2016–2025. The analysis decomposes headline inflation variance into subgroup volatility and covariance contributions; it also applies generalised forecast-error variance decomposition (GFEVD) to six vegetable components (tomato, onion, potato, garlic, ginger and other vegetables) using monthly data from April 2015 to August 2025, with a 12-month horizon.

### Results relevant to this project

The paper reports that food has a 45.9% weight in the 2012-base CPI basket and that vegetables, particularly tomato, onion and potato, are major drivers of headline inflation volatility. It reports that covariance among CPI subgroups turned negative from 2022-23, suggesting weaker broad cross-subgroup co-movement even when some individual food-price series remain volatile. In its vegetable-level GFEVD, volatility from non-TOP vegetables can spill over to TOP vegetables, while TOP shocks are less likely to generalise to one another. The paper also highlights policy interventions that dampen volatility transmission.

### Comparison with this project

This study is closely related to our volatility and covariance-decomposition sections, but its results should not be treated as direct validation of our mean-inflation regression. Covariance-based volatility contributions and GFEVD of vegetable-price volatility are different estimands from the regression coefficient on lagged food inflation in a non-food/core equation. The RBI findings support a nuanced narrative: large food-specific volatility can coexist with limited broader propagation across CPI groups, and within-food spillovers may be stronger than food-to-core mean pass-through.

## 4. Synthesis and contribution of this project

The three RBI papers do not produce one interchangeable “spillover coefficient.” They examine, respectively: (i) a short-run mean-inflation relationship in an ARDL/cointegration framework; (ii) expectations, costs and policy-mediated transmission in a broader semi-structural macro framework; and (iii) volatility decomposition and within-vegetable volatility transmission.

The project's result is best stated as follows:

> Food inflation is substantially more volatile than non-food inflation in the historical 2012-base CPI data. However, in our conditional monthly distributed-lag specification over 2013–2025, we do not find robust evidence of a systematic positive delayed food-to-non-food or food-to-core association. This does not rule out contemporaneous co-movement, small average effects, episodic transmission during persistent shocks, or indirect propagation through expectations and input costs. The broader RBI evidence suggests that such channels and volatility dynamics need not appear as a stable average delayed coefficient in a single aggregate CPI equation.

The result should not be described as proof of “no spillover” or as a causal null. The reverse-direction specification is also covariance- and COVID-treatment-sensitive and is retained as exploratory only.

## 5. Primary-source citation register

1. Patra, John and George (2024a), RBI Bulletin, January 18: https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=22323
2. Patra, John and George (2024b), RBI Bulletin, August 19: https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=22787
3. Mohan, Hasan, Sarkar and John (2026), RBI Bulletin, February 20: https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23980
