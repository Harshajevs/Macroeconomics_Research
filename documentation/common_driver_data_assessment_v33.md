# Common-driver data assessment — Tier-B extension (v3.3)

**Date:** 15 November 2026  
**Purpose:** establish which external monthly controls can be added to the project without weakening source reliability or inventing missing observations. These controls are not part of the Tier-A baseline.

## 1. Why a common-driver tier is relevant

Food and non-food prices may co-move because of forces outside the food basket: imported energy costs, exchange-rate movements, transport and distribution costs, and macroeconomic/policy responses. The forward and reverse reduced-form equations do not independently identify these channels. A common-driver extension can test whether the predictive lag coefficients persist when some observable external factors are conditioned on. It still will not make the coefficients causal, especially because some controls (notably policy rates) respond endogenously to inflation.

## 2. Candidate sources checked

### Indian basket crude oil

The Government of India's Petroleum Planning & Analysis Cell (PPAC) maintains an official Indian-basket crude-oil FOB price page with financial-year/month selection and a historical report facility: https://ppac.gov.in/prices/international-prices-of-crude-oil . PPAC identifies the Indian crude basket as a composite proxy, not a single Brent price. Its historical report/download interface uses registration/verification and its public page renders the monthly table dynamically; a complete 2013–2025 monthly file was not successfully captured in this run.

A reliable annual context series was available through a Lok Sabha annexure to Unstarred Question 43 answered 29 January 2026, sourced to PPAC. The annual Indian-basket average in Rs/barrel rises from Rs 6,383.26 in FY2013-14 to Rs 7,488.59 in FY2022-23, before easing to Rs 6,643.80 in FY2024-25. The full series is stored at `data/external/ppac_indian_basket_annual_prices_2013_14_to_2024_25.csv`. Because the data are annual/fiscal-year averages, they are not used as regressors in a monthly distributed-lag equation.

Official source: https://sansad.in/getFile/loksabhaquestions/annex/187/AU43_KocyKN.pdf?source=pqals

### USD/INR exchange rate

The RBI Database on Indian Economy table for daily interbank forex rates (USD vis-à-vis INR) is available from 8 August 2000. Its table page reports the RBI as the source and provides CSV/JSON download options: https://dbie.rbihub.in/tables?table=financial_markets.r691_daily_interbank_forex_rates_usd_vis_a_vis_inr . The RBIH/DBIE portal also exposes a separate monthly table for the exchange rate of the rupee vis-à-vis the SDR, US dollar, pound sterling, euro and yen (monthly average and high/low), with observations from April 2008 through October 2026 and CSV/JSON download options: https://dbie.rbihub.in/tables?table=external_sector.r1505_exchange_rate_of_the_indian_rupee_vis_vis_the_sdr_us_doll . RBI Handbook Table 205 independently publishes monthly-average and end-month USD/INR values (the currently retrieved edition covers 2022 onward); the Handbook notes that RBI reference rates are used from May 2012 and FBIL has disseminated reference rates since 10 July 2018. These routes establish that an official-source monthly FX series exists. However, the complete raw CSV spanning the project sample was not captured and validated in this execution, so no FX values have been manufactured or inserted. A data mirror is not substituted as if it were the authoritative original.

### Policy repo rate

RBI's official information disclosure states that historical repo-rate information from April 2005 through March 2026 is accessible through DBIE: Statistics → Financial Sector → Key Rates → Major Monetary Policy Measures — Bank Rate, CRR & SLR. This is a primary source route: https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=624 . The dated repo-rate change history is available as an official RBI key-rate series, but it has not yet been extracted into a reproducible monthly input. It will need an explicit monthly aggregation rule (e.g. month-end rate or average effective policy rate) before use.

## 3. Why these controls are not yet included

1. The PPAC Indian-basket monthly series is discoverable on an official page, but its historical report facility currently requires registration/verification and the displayed table is dynamically populated. The clean file acquired so far is annual/fiscal-year frequency; converting those annual averages into monthly values would fabricate within-year variation.
2. An RBI monthly USD/INR table is now identified, in addition to the daily interbank table. The download interface exists, but the full sample CSV has not yet been captured and checked against RBI publication tables. Repo-rate history is also available through RBI DBIE, but needs a defensible monthly timing convention.
3. Monthly repo changes are endogenous policy responses and may be part of the transmission mechanism. They should be introduced as a pre-declared sensitivity with explicit timing (e.g. lagged repo rate/changes), not automatically added as an ordinary exogenous common shock.
4. Adding multiple highly correlated external controls to a short sample of 147 observations can create overfitting and change the estimand. The common-driver tier should be deliberately small and reported as a sensitivity.

## 4. Recommended protocol for the next research checkpoint

- Obtain the monthly PPAC Indian-basket data for April 2013–December 2025 directly from PPAC (or a government source reproducing PPAC monthly data) and preserve the original workbook/PDF, access date and checksum.
- Prefer the RBI DBIE monthly USD/INR average table (April 2008–October 2026) for a direct like-frequency control. If using the daily series instead, aggregate to calendar-month means using all valid business-day observations and record each month’s observation count and missing dates. Cross-check selected months against RBI Handbook Table 205.
- Convert oil prices to INR only if using a USD-denominated series: `INR oil price = USD crude price × INR per USD`. Do not double-convert if the Indian-basket series is already in Rs/barrel.
- Use log changes or carefully documented lagged changes, not raw trending levels, alongside the same outcome and food-lag structure. Test oil and FX lags parsimoniously and pre-declare the small set of alternatives.
- Treat repo rate separately as policy-response sensitivity, with lag timing and endogeneity caveats. Do not interpret it as a clean exogenous shock.
- Report how sample coverage changes; if common controls materially reduce the sample, provide an identical-sample baseline before attributing changes to controls.

## 5. Decision

No monthly common-driver regressor has been fabricated or added to the current results. The annual PPAC observations provide useful historical context only. The RBI monthly FX and repo tables are now identified as feasible official sources, but the source files and harmonisation rules still need to be acquired and checked. Before report preparation, decide whether the primary-source monthly data can be captured reproducibly. If not, transparently defer the common-driver model and retain the present non-causal conditional-association interpretation.
