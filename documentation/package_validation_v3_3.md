# v3.3 package validation record

**Date:** 15 November 2026  
**Status:** Working-copy and fresh-extraction validation complete for the v3.3 package contents.

## Environment

- Python runtime used in this environment: 3.12-compatible project environment.
- Dependencies pinned in `requirements.txt`.
- BLAS thread oversubscription limited for estimation commands using `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`.

## Passed working-copy commands

The following all exited successfully:

```bash
python tests/test_pipeline.py
python tests/test_real_data.py
python src/spotcheck_groups.py
python src/headline_analysis.py
python src/replicate_rbi_stylised_facts.py
python src/build_dataset.py
python src/corrected_descriptive_analysis.py
python src/stl_window_sensitivity.py
python tests/test_econometric_design.py
python tests/test_postreview_econometrics.py
python tests/test_v33_econometrics.py
python tests/test_baseline_model.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch forward
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch core
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_v33_estimations.py --batch reverse
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/null_size_simulation.py
```

The three estimator batches completed successfully when run separately and rebuilt the 20-row model comparison in both the working directory and a clean extraction of the ZIP. A combined multi-batch shell invocation exceeded the execution window before completing all batches; the batches were then rerun separately and all completed successfully. The clean extraction also reran the null-size simulation and both manifests passed again after estimation. The monolithic `src/estimate_baseline.py` entry point is not the recommended full-project runner; use `src/run_v33_estimations.py` as documented in README.

## Integrity manifests

- `postreview_input_manifest_v3_3.sha256`: hashes 73 analysis code, tests, raw/external/processed data and research-design/documentation inputs.
- `postreview_output_manifest_v3_3.sha256`: hashes 247 stable CSV/PNG outputs, processed dataset and the main interpretation note.
- OLS plain-text summary files are not in the output manifest because statsmodels includes a wall-clock `Time:` header that changes between otherwise identical fits. Their coefficients and reported statistics are independently captured in the deterministic CSV outputs.
- Run both checks from the project root:

```bash
sha256sum -c documentation/postreview_input_manifest_v3_3.sha256
sha256sum -c documentation/postreview_output_manifest_v3_3.sha256
```

## Statistical and research cautions retained

1. The fixed-regressor block-wild bootstrap conditions on observed regressors, including lagged dependent variables. It is not a recursive bootstrap and does not recreate the full stochastic path of the lagged outcome.
2. The local null-size simulation is design-specific and relatively low-resolution (120 outer replications and 199 inner bootstrap draws). Claude's independent larger simulation is important supporting audit evidence, not a universal size theorem.
3. Non-significant forward food-lag tests do not prove a zero spillover effect. The current-plus-three-lag intervals include the approximate 0.048 short-run sum reported in the January 2024 RBI ARDL table.
4. The operational core outcome excludes the full Food and Beverages and Fuel and Light groups but retains some vehicle-fuel and precious-metal items in Miscellaneous.
5. Reverse-direction models are exploratory and COVID-treatment-sensitive. No causal or structural Granger interpretation is made.
6. The common-driver monthly crude/FX/repo sensitivity remains open. Annual PPAC crude observations are context only; no annual values have been interpolated into monthly regressors.
7. October 2026 CPI observations are based on the new 2024 CPI base and remain separate from the historical 2012-base model.

## Readiness

The v3.3 package has passed working-copy and clean-extraction tests, all three estimator batches, null-size simulation and both manifests. It is ready for an independent Claude audit. It is **not yet at final empirical claim freeze**. The next required stage is to reconcile the independent review and decide whether a reproducible monthly common-driver dataset can be assembled from the identified primary-source routes. Report drafting remains deliberately deferred.
