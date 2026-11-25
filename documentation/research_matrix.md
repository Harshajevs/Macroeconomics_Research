# Research matrix (AI-drafted study notes, 13 Nov 2026)

Reading-depth key: FULL = full text retrieved and read; SUMMARY = only abstract or summary page seen; CITED = known only from another paper's citation.
Use: read the papers yourselves, then correct and rewrite these rows in your own words. These notes are paraphrased and are NOT report text.
Numbers are the papers' own; re-check against the source before citing.

## 1. Patra, John and George (2024a) "Are Food Prices the 'True' Core of India's Inflation?" RBI Bulletin, 18 Jan 2024 [FULL]
| Field | Notes |
|---|---|
| Question | Does food inflation behave like core inflation on four tests: volatility, persistence, spillover into non-food, cyclical sensitivity? |
| Data | Monthly CPI group/sub-group Jan 2012 to Oct 2023 (moments); persistence Oct 2016 to Oct 2023; ARDL on seasonally adjusted monthly data Jan 2011 to Oct 2023; quarterly Q1 2011 to Q3 2023 for output-gap sensitivity |
| Methods | Mean, SD, skewness, kurtosis and their cross-correlations; contribution and variance decomposition; Bayesian time-varying persistence; ARDL bounds test (Pesaran, Shin and Smith 2001); time-varying regressions on the output gap; scenario runs in the RBI's quarterly projection model |
| Findings | Food average close to headline and core (2016-23); food much more volatile; food about 43% of average headline inflation; vegetables about 38% of headline variance, covariances about 30%; food and non-food cointegrated; error correction in the food equation (food moves toward non-food within about a year), none in non-food; small positive short-run food effect on non-food (about 0.05), so only large, persistent shocks spill over; about 10% of food inflation is demand-driven |
| Limits (our reading) | Two-variable ARDL, no controls reported; sample ends Oct 2023; seasonal adjustment method not described in the text |
| Use for us | Template for stylized facts, ARDL idea, definition of core (ex food and fuel) |

## 2. Patra, John and George (2024b) "Are Food Prices Spilling Over?" RBI Bulletin, 19 Aug 2024 [FULL]
| Field | Notes |
|---|---|
| Question | Why is food inflation persistent, does it raise inflation expectations, and is it spilling into core? |
| Data | Monthly food inflation Jan 2011 to Jun 2024; quarterly household expectations 2012-13 to Q1 2024-25; PMI price indices; an index of informal service charges |
| Methods | Counting months of high food inflation by sub-group; decomposing food inflation into intrinsic persistence, demand-driven persistence, a time-varying trend and shocks; regression of expectations on food inflation; bivariate correlations; historical decomposition in the RBI's model |
| Findings | Food inflation averaged 6.3% in Jun 2020 to Jun 2024 versus 2.9% in 2016-20; at or above 6% in about 57% of months; rising persistence driven by an upward trend (read as expectations) and repeated supply shocks; food inflation raises expectations (long-run elasticity about 0.22); food inflation correlates with PMI input and output prices; spillover to core rising since 2022-23 but offset by tight policy |
| Limits (our reading) | Spillover evidence is mostly bivariate correlations and a model; not a direct non-food-on-food regression |
| Use for us | Motivation and policy discussion (expectations, offsetting policy) |

## 3. Mohan, Hasan, Sarkar and John (2026) "Retail Inflation Volatility in India: Sources, Determinants, and Implications" RBI Bulletin, 20 Feb 2026 [FULL]
| Field | Notes |
|---|---|
| Question | What drives headline CPI volatility during flexible inflation targeting (2016-25), and what role do volatility spillovers and supply-side policy play? |
| Data | CPI Combined, base 2012=100. Stylized facts Apr 2016 to Aug 2025; vegetable VAR on monthly changes Apr 2015 to Aug 2025; Ball-Mankiw regression Apr 2015 to Aug 2025; GARCH Feb 2020 to Jul 2025 |
| Methods | Variance decomposition with covariances (following Borio et al 2023); generalised forecast error variance decomposition (Diebold and Yilmaz 2012) for spillovers among tomato, onion, potato, garlic, ginger and other vegetables; regression of changes in seasonally adjusted annualised headline inflation on changes in cross-sectional SD and skewness (Ball and Mankiw 1995); GARCH(1,1) with an index of government supply-side actions |
| Findings | 2016-25 headline YoY: mean 4.9, SD 1.5; rolling SD fell from 2.4 (2012-16) to 1.5; above 6% in 26% of months, below 2% three times; food far more volatile, but only some sub-groups; vegetables dominate headline variance (over 80% in 2025-26 to Aug 2025); sub-group covariances turned negative from 2022-23, read as shocks no longer spreading; within vegetables, covariances above 50% of variance; ex-TOP vegetable shocks spill onto TOP; volatility and skewness of the cross-section raise headline inflation; government interventions dampen the effect and conditional volatility |
| Limits (authors and ours) | Aggregated analysis, authors call for disaggregation; ARCH effects were present in all their mean regressions, so serial heteroskedasticity is real in this data; intervention index is a binary, CPI-weighted construct |
| Check against our data | Our official series reproduces its mean, SD, below-2% count and (when Apr-May 2020 index values are used) the 26% above-band share. See outputs/tables/replication_rbi_feb2026.txt |
| Use for us | Closest competing work; motivates variance decomposition and ARCH diagnostics; defines FIT-period robustness sample |

## 4. Das and George (2023) "Consumer Price Index: The Aggregation Method Matters" RBI Bulletin, 21 Mar 2023 [FULL]
| Field | Notes |
|---|---|
| Question | Why do published CPI inflation and inflation derived by users from item-level data diverge, and what should be done? |
| Method | Describes NSO compilation (Jevons elementary indices, Laspeyres-type aggregation with 2011-12 weights); compares published (horizontal aggregation across states and sectors) with derived (vertical aggregation) 2015-23; t-tests of divergence; decomposition by group |
| Findings | In principle both routes agree barring missing or zero prices and rounding; divergence mainly from missing prices and zero-price treatment; modest and two-sided before COVID; since 2021 the fuel group created a one-sided gap; Jan-Feb 2023 gap came from cereals (zero PDS prices); group and headline do not add exactly (a residual exists) |
| Recommendations | Align aggregation with international practice, treat zero prices as prices, rebase on time |
| Use for us | Justifies using published group indices; tells us to expect a small headline residual, larger from 2021 and in fuel; supports a core-inflation robustness check |

## 5. Patra, Behera and John (2021) "Is the Phillips Curve in India Dead, Inert and Stirring to Life or Alive and Well?" RBI Bulletin, 15 Nov 2021 [SUMMARY]
Seen: abstract and press summary only. Examines time variation and convexity of the Indian Phillips curve; reports a convex curve that flattened for over six years from 2014 and is recovering. Read in full before citing in detail. Use: background for slack versus supply shocks in explaining non-food inflation.

## 6. Walsh (2011) "Reconsidering the Role of Food Prices in Inflation" IMF Working Paper 11/71 [SUMMARY]
Seen: abstract only. Argument: in lower-income countries food inflation is more volatile and often more persistent than non-food, and food shocks propagate into non-food, so core measures that exclude food can mislead policy. Read in full before citing in detail. Use: the main international argument we test on Indian data.
