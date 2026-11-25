# HS455 Food Inflation Project — Stage 3 Context Handoff

**Status date:** 14 November 2026  
**Lead implementation session:** ChatGPT  
**Independent reviewer:** Claude (review only; do not replace the canonical project files without an explicit decision)  
**Canonical package:** `food-inflation-project-stage3-corrected.zip`

## 1. Research question

To what extent does food inflation contribute to inflation volatility in India, and do persistent food-price shocks spill over into non-food inflation?

The project is a reproducible empirical study using official All-India Combined CPI, base 2012=100. Do not claim novelty on the existence of food inflation volatility or spillovers; RBI research has already examined those questions. The defensible student contribution is a transparent longer sample through December 2025, consistent variable construction, a parsimonious dynamic regression, and careful robustness/diagnostic work.

## 2. Canonical data and windows

- Raw data: `data/raw/cpi_2012_combined_groups.csv`, January 2013–December 2025 (156 months).
- Original Excel export and row-wise export are preserved unchanged in `data/raw/`.
- Ten Housing observations (December 2018–September 2019) were recovered from official monthly releases; see `housing_index_recovery_sources.csv`.
- December 2025 Pan/Tobacco export value 215.9 was reconciled to the official release/spot-check value 215.8; see `source_reconciliation.csv`.
- Food and Beverages and all six CPI groups are present; CFPI is included but is a near-duplicate food series.
- Twelve Food and Beverages subgroup indices and official rounded Combined weights are available; weights sum to 45.86%.
- YoY descriptive window: January 2014–December 2025 (144 values).
- MoM analysis window: February 2013–December 2025 (155 monthly changes).
- For q=3/p≤3 candidate-model comparison, common regression start is May 2013.
- April–May 2020 published headline YoY values were not compiled. Source index observations are retained; the two collection-gap flags are not the same as the four March–June 2020 event pulse indicators.
- The data end in December 2025 and use the 2012 base; this is not live 2026 CPI data.

## 3. Resolved methodological corrections from Claude's memo

- M1: YoY moments remain descriptive only; iid YoY p-values and inferential claims were removed from active outputs. Legacy outputs are archived.
- M2: The one-sided raw YoY lead-lag table is archived and excluded from inference. Directional predictability is deferred to the formal regression and bidirectional Granger tests.
- M3: H1 uses a paired stationary bootstrap on STL-adjusted MoM, with automatic Politis–White/PPW expected block length, fixed 6/12/24 sensitivities, 4,999 replications and explicit Monte Carlo resolution. The selector's formula/tuning structure is documented and checked against the published `arch` algorithm reference. Standard stationary bootstrap has random endpoint wrapping; this is disclosed.
- M4: H2 (food has greater skewness/heavier tails) is retired as confirmatory. STL-MoM shape differences are exploratory only. Students must write their own hypothesis reasoning before sign-off.
- M5: Group-built non-food is primary outcome; operational core is pre-declared robustness; headline-built non-food is construction sensitivity.
- M6: March–June 2020 pulse indicators are in the processed dataset. April–May collection-gap flags remain separate. Regression with and without pulses remains pending.
- M7: STL is applied to log CPI index levels before differencing for descriptive MoM. Month-of-year dummies are in the baseline regression design; STL-based regression is sensitivity.
- R1: MoM sample now begins February 2013.
- R2: CFPI is not presented as independent validation. Twelve food subgroups and a derived (not official) food-ex-vegetables proxy have been added.
- R3: Operational core excludes Food and Beverages and Fuel and Light, but still retains selected vehicle fuel and precious-metal items in Miscellaneous, totaling 3.58866% of the overall basket. Item-level monthly indices are not in the supplied workbook, so an adjusted core excluding these items is not fabricated.
- R4: Volatility is compared with each non-food group, not just the non-food composite; diversification caveat is documented.
- R5: Independent tracker arithmetic is reconciled.

## 4. Current descriptive results (not spillover-regression estimates)

STL-adjusted MoM log inflation, February 2013–December 2025, n=155:

- Food SD: 0.9883 percentage points.
- Non-food SD: 0.2418 percentage points.
- Food-minus-non-food SD difference: 0.7465 pp; stationary-bootstrap 95% CI [0.5391, 0.9483] under automatic expected block length 2.
- Log SD ratio: 1.4077; 95% CI [1.1377, 1.6763].
- Fixed expected block lengths 6, 12 and 24 also produce positive lower bounds for the SD difference.
- Exploratory MoM skewness and kurtosis difference intervals include zero; H2 remains retired.
- Weighted subgroup-rebuilt Food & Beverages index: mean absolute gap 0.0333 and max absolute gap 0.0934 index points relative to the official Food & Beverages index.
- Food-ex-vegetables is a fixed-weight derived proxy, not an official MoSPI series.
- Covariance-aware group decomposition uses Cov(component contribution, total contribution)/Var(total contribution), includes cross-covariance and is not causal.
- Individual group volatility is in `outputs/tables/nonfood_group_volatility_comparison.csv`; the non-food composite is less volatile partly because it aggregates different components.

## 5. Frozen pre-estimation model

Baseline:

`mNF_t = alpha + sum(i=1..p) rho_i*mNF_(t-i) + sum(j=0..3) beta_j*mFood_(t-j) + month indicators + Mar-Jun-2020 pulses + error`

- `mNF` and `mFood` are 100 × monthly log changes.
- `p` is selected by BIC from {0,1,2,3} using the common q=3 sample May 2013–December 2025.
- q=3 is baseline; q=1 and q=6 are sensitivity horizons.
- Primary delayed-spillover estimand: `beta1 + beta2 + beta3`.
- Primary null: `beta1 = beta2 = beta3 = 0` (HAC Wald test).
- `beta0` is same-month co-movement and must not be described as delayed spillover.
- HAC/Newey-West maxlags 6 is primary; maxlags 12 is sensitivity. Conventional and HC3 are supplementary.
- No domestic Fuel and Light control in the non-food equation because it is part of the dependent basket.
- External Brent and exchange-rate controls are Tier-B extensions after source validation.
- No primary ECM/long-run claim unless cointegration evidence and stability support it.

## 6. Still pending

1. Both students should fill and approve the “Team's own reasoning” cells in `documentation/hypotheses.md`; do not fabricate their reasoning.
2. Verify the exact variable transformation used in the cited RBI 2024 ARDL methodology before describing our model as replication.
3. Estimate formal baseline q=3 model and select p by BIC on common sample.
4. Report HAC Wald test and confidence interval for delayed cumulative food effect.
5. Run BG, ARCH-LM, White/BP, RESET, residual ACF/PACF, CUSUM/recursive stability, Cook's distance and influence sensitivities.
6. Run q=1/q=6, core, headline-built non-food, food-ex-vegetables, STL regression, FIT-only, post-COVID interaction and COVID exclusion sensitivities.
7. Run reverse-direction equation and bidirectional Granger tests.
8. Consider validated Tier-B oil and exchange-rate controls.
9. Complete student-written literature synthesis and final 3,000–4,000-word report.

## 7. Reproduction

From the project root:

```bash
python -m compileall -q src tests
python tests/test_pipeline.py
python tests/test_real_data.py
python src/spotcheck_groups.py
python src/headline_analysis.py
python src/replicate_rbi_stylised_facts.py
python src/build_dataset.py
python src/corrected_descriptive_analysis.py
python tests/test_econometric_design.py
```

All commands passed from a fresh extraction of the Stage-3 ZIP on 14 November 2026. See `documentation/final_archive_smoke_test.md` and `RUN_SUMMARY.md`.
