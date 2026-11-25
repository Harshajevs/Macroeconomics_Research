# Literature digest: what the reading tells us (study aid, 13 Nov 2026)

This is a briefing so you can hold the whole literature in your head quickly. It is not report text.
Read the papers yourselves; your literature review must come from your reading and your own wording.

## A. The big picture in plain language
Central banks usually watch "core" inflation, which strips out food and fuel because they swing a lot. India's CPI basket is about 46% food, so ignoring food ignores nearly half of what households pay for. Walsh (2011) argued that where food is volatile and persistent and its shocks spread into other prices, dropping food can mislead policy. The RBI's staff then tested that on India three times: do food prices act like core (Jan 2024), are they spilling over and feeding expectations (Aug 2024), and where does headline volatility actually come from (Feb 2026). Their consistent message: food is far more volatile than core; usually it fades and converges to non-food; but large, repeated shocks (since 2020, mostly weather) have made it more persistent and have spilled over a little. Our project asks the spillover question again with a direct regression of non-food inflation on food inflation, with controls, over a longer sample that includes the 2025 food deflation.

## B. Concepts to be comfortable with
- **Core inflation.** Headline minus the volatile parts. In the RBI papers it means CPI excluding food and fuel. Whether that is a good "underlying trend" depends on whether the excluded parts are noise or signal.
- **Relative price shock.** A big move in one price group (like vegetables) relative to others. Ball and Mankiw (1995) say such shocks can push up the overall inflation rate, especially when they are lopsided (skewed).
- **Four "core-like" tests** (Patra et al 2024a): volatility (higher is noise), persistence (does it last), spillover (does it leak into non-food), cyclical sensitivity (does it respond to demand).
- **ARDL, bounds test, error-correction term (ECT).** ARDL regresses a variable on its own lags and lags of another. The bounds test checks for a long-run link. A significant negative ECT in an equation means that variable moves back toward the long-run relationship; in the RBI result it is food that corrects toward non-food, not the reverse.
- **Variance decomposition with covariances.** Headline variance equals the sum of each component's variance plus twice the covariances. A large covariance share means shocks move together (spread through the basket); the Feb 2026 paper found covariances turned negative from 2022-23.
- **Horizontal versus vertical aggregation** (Das and George 2023). MoSPI builds all-India group and headline indices by aggregating across states and sectors. A user adding up item or group indices may get a slightly different headline. Expect a small residual.
- **FIT and the 2-6% band.** India's flexible inflation targeting: target 4%, tolerance band 2-6%, used in the RBI papers from April 2016.
- **YoY versus MoM.** Year-on-year is smooth and persistent and uses overlapping windows; month-on-month is noisier but better for dynamic regression, after removing seasonality.

## C. How the papers connect
Walsh (2011) gives the argument. Das and George (2023) is the measurement warning: be careful how indices are aggregated. Patra et al (2024a) gives the tests and the ARDL spillover result. Patra et al (2024b) adds expectations and the policy angle. Mohan et al (2026) focuses on volatility, finds vegetables dominate, and uses ARCH-type tools because the data show changing variance. Patra, Behera and John (2021) is background on slack versus supply shocks.

## D. Benchmarks we can check ourselves against
- Food and beverages weight: 45.86 (MoSPI, Combined). CFPI weight 39.06.
- Headline YoY Apr 2016 to Aug 2025: mean about 4.9, SD about 1.5, above 6% in about 26% of months, below 2% three times. We reproduced these (outputs/tables/replication_rbi_feb2026.txt).
- Short-run effect of food on non-food in the 2024a ARDL: about 0.05 (month-on-month, seasonally adjusted). A very different coefficient in ours needs explaining.
- Food inflation averaged 6.3% in Jun 2020 to Jun 2024 against 2.9% in 2016-20 (2024b).

## E. What we can safely claim, and what we cannot
Safe: food is more volatile than non-food; food shocks matter for headline because of weight; our estimates agree or disagree with the RBI's on specific numbers; Granger-type or regression evidence of association.
Risky: that food "causes" non-food inflation (common drivers like oil and exchange rates, and reverse effects through transport costs, are not removed); that the RBI proved spillovers are large (their own short-run coefficient is small); anything about 2026 (base change).

## F. Where we can add something without overclaiming
(1) A direct dynamic regression of non-food on food with controls; (2) a sample through Dec 2025 that includes the late-2025 food deflation, so we can test whether positive and negative food shocks behave differently; (3) a check whether the relationship differs before and after COVID; (4) a test in both directions. The RBI work covers the descriptive and volatility ground, so we should say plainly that those sections replicate known results.

## G. Questions an examiner could ask (think through your own answers)
1. Why food and beverages instead of CFPI? 2. Why month-on-month for the regression and year-on-year for descriptives? 3. Why can't you say food causes non-food inflation? 4. What did you do about April-May 2020? 5. Why does the RBI find food converging to non-food, and does your model allow for that? 6. What does a small coefficient imply for monetary policy? 7. How is your non-food series built, and what does Das and George (2023) say about its limits? 8. Why does your sample start in 2014 when the RBI papers use the FIT period? 9. What would change your conclusion?

## H. Building your literature review (your writing)
Suggested shape, one short paragraph each: (1) why food matters in an emerging-economy CPI and the core-inflation debate (Walsh 2011; Cecchetti-type caution via the RBI papers); (2) the theory of relative price shocks (Ball and Mankiw 1995); (3) Indian evidence on food inflation and spillovers (Patra et al 2024a, 2024b); (4) volatility and its sources (Mohan et al 2026); (5) measurement caution (Das and George 2023) and the gap your report addresses. Write from your notes in your own voice; I can give feedback on a draft you write.
