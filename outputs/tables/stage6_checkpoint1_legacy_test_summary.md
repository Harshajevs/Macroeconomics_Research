# Checkpoint 1 — legacy v3.3 test suite results

**Run date:** 18 November 2026
**Working tree:** Checkpoint 1 copy of the HS455 v3.3 package

| Command | Result | What it checks |
|---|---|---|
| `python tests/test_pipeline.py` | PASS | Pipeline construction and structural behaviour (synthetic fixtures) |
| `python tests/test_real_data.py` | PASS | Authentic historical Combined CPI integration: 156 raw months, six groups, headline/CFPI, official spot checks and processed 156-row dataset |
| `python tests/test_econometric_design.py` | PASS | Descriptive/specification structure, STL/YoY labels, decomposition and subgroup weights |
| `python tests/test_postreview_econometrics.py` | PASS | Post-review econometric behaviour tests |
| `python tests/test_baseline_model.py` | PASS | Baseline output structure and software behaviour; not causal identification |
| `python tests/test_v33_econometrics.py` | PASS | v3.3 econometric behavioural tests |

These tests confirm that the Checkpoint 1 additions have not broken the established v3.3 pipeline/tests. They do not close Claude's outstanding v3.3 audit remediation items, and they do not validate any Urban CPI dataset. The new Stage 6 test discovery run is recorded separately in `stage6_checkpoint1_test_log.txt` (27 passed).
