# Baseline regression — preliminary formal estimate (v3.1)

**Model:** q=3, p selected by BIC from 0–3; October 2013–December 2025; raw monthly log changes; 11 month indicators; March–September 2020 pulse indicators. June 2013 and July–September 2013 are outside the primary window. No external oil or exchange-rate controls are included, so common external shocks remain a limitation.

## Primary result

- Selected own-lag order: p=1 (BIC).
- Observations: 147.
- Joint HAC(6) test of lagged food terms beta1=beta2=beta3=0: p=0.4822 (F-form p=0.4822).
- Sum of delayed coefficients beta1+beta2+beta3: 0.00135.
- HAC(6) 95% interval: [-0.04425, 0.04694].
- The interval includes zero and the joint test does not reject at conventional levels.

The baseline therefore provides **no statistically persuasive evidence in this sample that lagged food inflation predicts subsequent non-food monthly inflation conditional on the specified controls**. This is not proof that transmission never occurs; it is a result conditional on this sample, index construction, lag horizon and specification.

The contemporaneous food coefficient is approximately 0.0351 with HAC(6) p=0.0374. This is same-month conditional co-movement and must not be described as delayed spillover.

## Pre-declared sensitivities

| Specification | p selected | n | Joint HAC(6) p | Delayed sum beta1–beta3 | 95% CI |
|---|---:|---:|---:|---:|---:|
| Baseline q=3, Oct-2013 start | 1 | 147 | 0.482 | 0.0013 | [-0.0442, 0.0469] |
| q=3, Jan-2014 start | 1 | 144 | 0.527 | 0.0014 | [-0.0492, 0.0519] |
| q=1, Jan-2014 start | 1 | 144 | 0.678 | -0.0059 | [-0.0340, 0.0221] |
| q=6, Jan-2014 start | 1 | 144 | 0.807 | -0.0005 | [-0.0542, 0.0532] |
| FIT period, q=3 | 1 | 117 | 0.215 | 0.0078 | [-0.0560, 0.0716] |
| COVID outcome rows masked after lag creation | 1 | 140 | 0.476 | 0.0013 | [-0.0465, 0.0492] |
| STL-adjusted q=3 sensitivity | 1 | 147 | 0.767 | 0.0035 | [-0.0724, 0.0795] |

The direction and uncertainty of the delayed coefficient sum are broadly consistent across these pre-declared specifications: none rejects the joint null. The contemporaneous coefficient should be discussed separately.

## Diagnostics

For the primary model, BG(6) p=0.503, BG(12) p=0.740; Ljung–Box(6) p=0.532 and Ljung–Box(12) p=0.603. ARCH-LM(6) p=0.996; Breusch–Pagan p=0.959; RESET p=0.101. The pre-declared residual serial-correlation fallback was not triggered. Cook's-distance calculations are undefined for some isolated pulse observations with unit leverage; those are event dummies with single-month support. Treat influence diagnostics cautiously and use the separately specified leave-out runs before final interpretation.

## Important limits

1. This is a conditional predictive association, not causal identification.
2. Oil, exchange-rate and other common shocks are not controlled in this Tier-A baseline.
3. The pulse dummies absorb event-month means; they do not model all pandemic-era changes in variance or transmission.
4. The q=1/q=6 comparisons use January 2014 as a common start; do not compare their BIC mechanically with the October-2013 q=3 baseline.
5. The post-2021 interaction, reverse-direction equation, Granger tests, sup-F stability, HC3 and block/wild-bootstrap Wald checks remain to be implemented.
6. The outcome-only residual diagnostics Claude supplied were not treated as food-spillover evidence.

**Interpretation discipline:** the primary delayed-spillover hypothesis is not supported by this baseline estimate. Do not alter the lag horizon or sample after seeing this result to seek significance. Any additional model must be justified as a declared sensitivity or a clearly labelled exploratory extension.
