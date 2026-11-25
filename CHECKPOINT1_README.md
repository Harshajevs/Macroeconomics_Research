# HS455 Stage 6 — Checkpoint 1 (18 November 2026)

This package is a revision of the Stage 6 Phillips-curve design after Claude's 17 November adversarial audit. It preserves the earlier v3.3 project files and results.

## Key additions
- `documentation/claude_stage6_audit_reconciliation_checkpoint1.md`
- `documentation/phillips_curve_preanalysis_plan_stage6_v2.md`
- `documentation/state_panel_feasibility_stage6.md`
- `documentation/CLAUDE_REVIEW_PROMPT_STAGE6_CHECKPOINT1.md`
- `documentation/stage6_api_version_assessment.md`
- `src/validate_stage6_urban_cpi.py` (strengthened intake gate)
- `src/stage6_aggregate_null_size_simulation.py` (synthetic null-size experiment)
- state-level PLFS/CPI/weights templates and all-India CPI anchors template
- aggregate UR leverage diagnostics

## Critical status
No actual Urban CPI data are included. The CPI files are blank templates. No Phillips-curve regressions or correlations have been run. All test outcomes apply to synthetic test fixtures and existing PLFS structural data only.

Run Stage 6 tests from the project root:
`python -m unittest discover -s tests -p 'test_stage6*.py' -v`

Run synthetic null-size calibration (default 2,000 repetitions per design):
`python src/stage6_aggregate_null_size_simulation.py`

The old v3.3 input/output manifests both verify; all six legacy v3.3 test scripts pass. The Checkpoint 1 manifest covers the new package files. The old v3.3 manifests and results are not to be overwritten. Student review and approval remain pending.
