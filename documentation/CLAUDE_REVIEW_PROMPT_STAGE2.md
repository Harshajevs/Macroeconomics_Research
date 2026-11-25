# Independent review request — econometric design milestone

We are sharing the current project ZIP for an independent methodological review. This project is led in another working session; your role is to challenge assumptions and identify weaknesses, not rebuild or overwrite the project.

Research question: To what extent does food inflation contribute to inflation volatility in India, and do food-price shocks spill over into non-food inflation?

Data: authentic All-India Combined CPI, base 2012=100, monthly, Jan 2014-Dec 2025 (144 observations); raw index data Jan 2013-Dec 2025. Primary food index is CPI Food and Beverages. CFPI is an alternative measure. Primary outcome is group-built non-food CPI; robustness outcomes are core CPI and headline-derived non-food CPI.

Please read:
- `README.md`
- `RUN_SUMMARY.md`
- `documentation/econometric_design_review.md`
- `documentation/chatgpt_independent_tracker.md`
- `documentation/design_implications.md`
- `outputs/tables/econometric_stationarity_tests.csv`
- `outputs/tables/econometric_seasonality_tests.csv`
- `outputs/tables/econometric_engle_granger_tests.csv`
- `outputs/tables/econometric_ardl_bounds_sensitivity.csv`
- `outputs/tables/econometric_cointegration_seasonal_sensitivity.csv`
- `outputs/tables/econometric_short_run_screen_exploratory.csv`

Current proposed direction:
- Use monthly log changes for the primary short-run model; retain YoY inflation for stylised facts.
- Include 11 month-of-year indicators.
- Candidate equation: one or a few lags of non-food monthly log inflation plus current and 1-6 lags of food monthly log inflation and calendar-month indicators.
- Select the non-food autoregressive order parsimoniously by BIC; hold the food lag horizon fixed at six months for the main joint test.
- Primary spillover test: HAC Wald test of food lags 1-6 jointly equal to zero. Treat the current-month coefficient as contemporaneous association.
- Do not estimate an ECM/long-run multiplier unless cointegration is supported robustly. Current food-to-non-food Engle-Granger and ARDL bounds results do not support that condition.
- Compare the full sample with FIT-only and April-May 2020 exclusion samples.
- Use core CPI, headline-derived non-food and CFPI as robustness measures.
- Do not add repo rate to the baseline. Crude oil and exchange-rate changes may be added only in a separately documented extended model after validation.

Your review must answer:
1. Are monthly log changes with calendar-month effects appropriate for the main short-run spillover question? What are the drawbacks?
2. Is the no-cointegration conclusion adequately supported, or are there credible additional tests/specifications needed before ruling out an ECM?
3. Is a six-month fixed food-lag window reasonable for 144 monthly observations? Should 12 months be a sensitivity?
4. Is the group-built non-food CPI construction defensible, and how should the small headline reconstruction residual be handled?
5. Do the exploratory screens suggest specification instability, sample dependence or possible reverse predictability?
6. What is the minimum defensible diagnostic suite for the final model?
7. Which extensions add genuine economic value and which are unnecessary for a 3,000-4,000-word course report?

For every criticism, state its severity (critical / important / optional), why it matters, and a concrete remedy. Distinguish published RBI findings from your own assessment. Do not report exploratory screens as final empirical results, invent data or papers, or change raw data. Return a concise decision memo only.
