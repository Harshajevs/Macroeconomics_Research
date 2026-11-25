# Food Inflation and Unemployment in India

HS455 research project, Indian Institute of Technology Ropar.

[Read the final report](report/HS455_Report.pdf).

The project compares inflation and unemployment in matched Urban data and measures food's contribution to headline-inflation variation. A secondary monthly analysis examines delayed food–non-food predictability.

The matched sample contains 27 quarters, 2018Q2–2024Q4. The data do not support a stronger negative unemployment relationship after excluding food. Food receives 88.71% of monthly and 80.96% of annual Combined headline variance under covariance accounting. These are sample findings, not identified causal effects. The spillover estimates remain inconclusive for small effects.

## Files

- `src/`, `tests/`: CPI processing, descriptive statistics, monthly models and tests.
- `data/`: the Combined CPI source workbook, source metadata, inputs and processed series.
- `outputs/`: model estimates, validation results, tables and figures.
- `stage7/src/`, `stage7/tests/`: matched unemployment analysis, variance accounting, inference checks and tests.
- `stage7/data/`: official CPI/PLFS response archives, matched data, source register and input hashes.
- `stage7/results/`, `stage7/figures/`: research estimates, sensitivity comparisons and plots.
- `report/`: one final report, its LaTeX source, figure/table generators and supporting numerical results.

## Run

Use Python 3.12. From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r stage7/requirements.txt
python stage7/run_research.py
```

The default run works offline from the included official-source responses and uses the saved high-draw simulation results. To recompute those simulations too:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python stage7/run_research.py --full
```

To run the tests separately:

```bash
python -m unittest discover -s stage7/tests -v
for test in tests/test_*.py; do python "$test" || exit 1; done
```

## Report source

The PDF is ready to read. To compile the included source and check its calculations:

```bash
cd report
tectonic --keep-logs --keep-intermediates report.tex
python verify_report.py
```

Tectonic writes `report.pdf`; `HS455_Report.pdf` is the preserved final release checked by the verifier. Figure/table regeneration uses `make_figures.py`, `make_tables.py` and `additional_analysis.py` in the same folder.

The source register links to the MoSPI/NSO releases, PLFS bulletins and RBI research. Original index bases and survey definitions are kept separate. Variance allocations include co-movement; correlations and predictive regressions do not by themselves establish causation.
