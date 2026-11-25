# Run summary — v3.3 post-results research revision

**Date:** 15 November 2026  
**Canonical historical data:** official 2012-base All-India Combined CPI, January 2013–December 2025.  
**Separate current-data vintage:** MoSPI/NSO October 2026 release, 2024=100 base; not spliced into historical series.  
**Runtime:** Python 3.13 in the producing environment; pinned pandas 2.2.3, NumPy 2.3.5, SciPy 1.17.0, statsmodels 0.14.6, Matplotlib 3.10.8 and seaborn 0.13.2.

## Status and preservation

The v3.3 work is a post-results revision after Claude's adversarial v3.2 audit. The delivered v3.2 package is preserved separately; v3.2's econometric specification is copied to `documentation/archive/stage4_v3.2_postresults/`. Earlier v3.1 output files remain archived under `outputs/archive/stage4_v3.1_pre_review/`. No revised estimate is represented as pre-estimation frozen.

## Primary outcomes and inference

The primary dependent variable is group-built non-food monthly log inflation. The alternative dependent variable is operational core monthly log inflation excluding Food and Beverages and Fuel and Light. Core retains petrol/diesel and precious-metal items inside Miscellaneous; its construction caveat must accompany all core references.

Following Claude's independent conditional-null size experiments, primary joint inference is the restricted-null, fixed-regressor six-month-block Rademacher wild-bootstrap tail probability with 4,999 replications. HAC(6), HAC(12) and HC3 are reported as sensitivities. The bootstrap holds the observed design matrix fixed, including lagged dependent variables; it is not a recursive time-series bootstrap. HAC-t and studentised block-wild bootstrap-t intervals are reported for linear contrasts.

## Main results

| Outcome / specification | p | q | n | HAC(6) joint chi-square p | Block-wild joint tail probability | Delayed sum β1–β3 | 95% HAC interval |
|---|---:|---:|---:|---:|---:|---:|---:|
| Food → non-food, Oct-2013 | 1 | 3 | 147 | 0.2966 | 0.4326 | -0.00349 | [-0.04653, 0.03955] |
| Food → operational core, Oct-2013 | 1 | 3 | 147 | 0.4495 | 0.4578 | -0.01882 | [-0.05396, 0.01632] |

Neither model detects a robust positive delayed relationship. The non-food studentised block-wild bootstrap-t interval is [-0.04470, 0.03911]; the core interval is [-0.05100, 0.01420]. This is not proof of a zero effect.

## Economic magnitude and the January-2024 RBI benchmark

The January-2024 RBI ARDL article reports a short-run sum of food-change coefficients of 0.048 in its non-food equation. That is not the same estimand as our delayed-only sum. The project's current-plus-three-lag sum β0+β1+β2+β3 is 0.03424 for non-food (bootstrap-t 95% interval [-0.02581, 0.09259]) and 0.01801 for core ([-0.04073, 0.07441]); both intervals include 0.048. Thus the project does not rule out a small positive overall short-run association of this approximate magnitude. The narrower delayed-only claim is that the current specification does not find robust evidence of a systematic positive delayed association.

## Robustness and stability

- January-2014 common-sample, q=1 and q=6, FIT-period, March–December 2020 exclusion, March 2020–December 2021 exclusion, April–May 2020 imputed-month exclusion, and STL-adjusted results are in `outputs/model_results/postreview_model_comparison_summary.csv`.
- Food-lag partial sup-F block-wild bootstrap tail probability: 0.2496 for non-food and 0.8276 for core, each with 4,999 draws. No break date is identified or reported.
- Reverse non-food-to-food results are exploratory and sensitive to COVID treatment: block-wild tail probabilities range approximately 0.027–0.099 across the included variants. Do not interpret them as causal or structural Granger evidence.
- Post-2021 interaction: HAC(6) F p=0.0595; block-wild tail probability 0.1542. January 2021 is an ex-post split, not an identified break date.
- White cross-product test omitted because near-saturated; Koenker Breusch–Pagan is reported. STL regression does not use the pooled COVID control, disclosed in the specification.

## Supplementary null-size simulation

`outputs/model_results/null_size_simulation.csv` contains a design-specific conditional-null experiment (120 Monte Carlo repetitions, 199 inner bootstrap draws). Under iid sign errors the empirical rejection rates were 17.5% for HAC(6) chi-square, 4.2% for HC3 and 2.5% for block-wild; under six-month block signs they were 12.5%, 1.7% and 4.2%, respectively. Wilson intervals are wide. This is a low-resolution calibration exercise, not a universal guarantee; Claude's independent larger simulations are also documented.

## Literature and current observations

`documentation/literature_reconciliation_nov2026.md` distinguishes: (i) the January-2024 RBI ARDL short-run mean relationship, (ii) the August-2024 RBI expectations/input-cost/QPM mechanisms, and (iii) the February-2026 RBI inflation-volatility and vegetable-volatility analysis. These are not interchangeable estimands.

MoSPI's 12 November 2026 release reports October 2026 headline CPI inflation of 6.09% and CFPI food inflation of 8.94% (both provisional), against final September rates of 5.54% and 7.74%. The Food and Beverages division rate is 8.51%, a different measure from CFPI. These observations use the 2024 CPI base and are kept separate from the historical 2012-base regressions. CSV extracts and limitations are in `data/external/` and `documentation/current_data_update_october_2026.md`.

## Reproduction and remaining work

Run from the project root:

```bash
python tests/test_pipeline.py
python tests/test_real_data.py
python src/spotcheck_groups.py
python src/headline_analysis.py
python src/replicate_rbi_stylised_facts.py
python src/build_dataset.py
python src/corrected_descriptive_analysis.py
python src/stl_window_sensitivity.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch forward
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch core
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch reverse
python src/null_size_simulation.py
python tests/test_econometric_design.py
python tests/test_postreview_econometrics.py
python tests/test_v33_econometrics.py
python tests/test_baseline_model.py
```

**Remaining before claim freeze:** Claude's full v3.3 audit; common-driver sensitivity using reliable INR crude/exchange-rate/policy series if obtainable and defensibly aligned; source-by-source citation check; final student review and instructor-compliant AI-use disclosure. Report writing is not yet started.
