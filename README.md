# Food Inflation and Unemployment in India

HS455 research project, Indian Institute of Technology Ropar.

**[Read the final report](report/HS455_Report.pdf)** · **[LaTeX source](report/report.tex)** · **[Research evidence](stage7/RESEARCH_CHECKPOINT.html)** · **[Claim ledger](stage7/documentation/claim_ledger.csv)**

The project answers two questions: does excluding food strengthen the negative relationship between inflation and unemployment, and how much variation in headline inflation is attributable to food? A secondary extension examines whether food inflation predicts later non-food or core inflation. The methods centre on descriptive statistics, matched-sample correlations, ordinary least squares and exact variance accounting, with additional checks for data quality, influential observations and uncertainty.

## Main findings

| Question | Answer from the studied sample | Interpretation |
| --- | --- | --- |
| Does excluding food strengthen the negative inflation–unemployment relationship? | The matched Urban sample does not support this hypothesis. Operational-core slopes remain positive in the primary comparisons; food-only exclusion gives the same qualitative answer. | This does not establish that a structural Phillips curve is absent in India. The quarterly sample is short and strongly influenced by pandemic observations. |
| How much headline-inflation variation is attributable to food? | Food receives **88.71%** of monthly and **80.96%** of annual Combined headline variance. Urban allocations are **79.85%** and **64.69%**. | These are historical covariance allocations, including co-movement with other components. They are neither basket weights nor identified causal food-shock shares. |
| Does food inflation predict later non-food or core inflation? | The primary monthly specification does not detect clear positive delayed predictability. | Limited power leaves small effects unresolved; non-rejection does not establish zero spillover. |

The price history uses the 2012-base CPI from January 2013 to December 2025. The unemployment analysis matches Urban CPI to PLFS Urban Current Weekly Status unemployment for persons aged 15 and above, covering **27 quarters, 2018Q2–2024Q4**. Later CPI bases and the redesigned 2025 PLFS are not spliced into these series. Operational core excludes food and fuel; food-only exclusion is an explicit sensitivity check.

## Repository contents

| Location | Contents |
| --- | --- |
| [`report/`](report/) | Current 13-page report, editable LaTeX, vector figures, tables, report data, generation scripts and 213-check verification record. |
| [`stage7/`](stage7/) | Completed research: official-source acquisition, input validation, unemployment models, variance allocations, spillover audits, simulations and evidence tables. |
| [`stage7/data/`](stage7/data/) | Archived official responses/publications and processed matched samples, including documented PLFS corrections. |
| [`stage7/results/`](stage7/results/) | Estimates, sensitivity comparisons, bootstrap results and calibration outputs. |
| [`stage7/documentation/`](stage7/documentation/) | Source register, claim ledger, methodological decisions, provenance and prior checkpoint records. |
| [`src/`](src/), [`tests/`](tests/), [`data/`](data/), [`outputs/`](outputs/) | Preserved earlier research pipeline, tests, inputs and results used by the completed analysis. |

Only the final report and its supporting source are published in `report/`; intermediate report versions are excluded. Earlier research checkpoint documents describe the state of the project at their creation. For current conclusions, use the final report and Stage 7 claim ledger. The former root README is preserved in [`documentation/archive/pre_report_README.md`](documentation/archive/pre_report_README.md). The final report contains 3,970 main-text words, 12 figures and 10 tables; its 13 pages include the cover, references and appendices.

## Run the research

Use Python 3.12 and an isolated environment. Commands below run from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r stage7/requirements.txt
python stage7/run_research.py
```

The standard run uses archived official-source responses and needs no new data download. It rebuilds inputs, runs the Stage 7 tests, re-estimates the main comparisons and accounting checks, and rebuilds the evidence checkpoint. It uses saved high-draw simulation results. To recompute the bootstrap and simulation exercises as well:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python stage7/run_research.py --full
```

The full run takes longer. `stage7/src/acquire_official.py` is for a deliberate new source-vintage acquisition, rather than ordinary offline reproduction. The root `requirements.txt` describes the earlier research runtime; `stage7/requirements.txt` records the completed research runtime.

## Run the checks

```bash
python -m unittest discover -s stage7/tests -v
for test in tests/test_*.py; do python "$test" || exit 1; done
```

Synthetic fixtures are used only for software tests. The empirical results come from the archived CPI and PLFS inputs. Tests cover source reconciliation, matched rows, regression arithmetic, direct slope differences, variance accounting and bootstrap implementation.

## Build the report

The published PDF is ready to read. To compile from source, open `report/report.tex` in Overleaf or run:

```bash
cd report
tectonic --keep-logs --keep-intermediates report.tex
python verify_report.py
```

Tectonic writes `report.pdf`; `HS455_Report.pdf` is the preserved release PDF that the verifier checks. To publish a newly compiled revision, copy `report.pdf` to `HS455_Report.pdf` before verification. Standard pdfLaTeX is also supported; run the necessary reference passes. Python is only needed for numerical verification or regenerating figures/tables. See [`report/README.txt`](report/README.txt) for those commands and the word-count scope.

## Sources and interpretation

The source register links to MoSPI/NSO CPI releases, the PLFS bulletins and RBI research. The original workbook, official response archives, data corrections and methodological limitations remain documented. The project distinguishes a descriptive relationship, an accounting allocation and a predictive regression; none alone identifies a causal policy effect.
