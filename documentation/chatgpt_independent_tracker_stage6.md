# Independent project tracker — Stage 6 / Phillips-curve workstream added

**As of:** 18 November 2026  
**Current stage:** Stage 6 — data feasibility and pre-analysis design for the newly added Phillips-curve objective.  
**Previous baseline:** Stage 5 / v3.3 tracker reported 71/100 under the earlier work breakdown. That figure is retained as a historical Stage 5 score and is not directly comparable with the rebased Stage 6 score below.  
**Current Stage 6 score:** **50/100 weighted progress points**. This is a planning/progress measure, not a course grade, percent of final report, or claim that the empirical work is complete.

## 1. Rebased project tracker

| Workstream | Weight | Credited | Evidence and remaining work |
|---|---:|---:|---|
| Scope, governance and research framing | 8 | 7 | Combined two-part problem statement and supporting spillover strand are clear; assignment/report constraints and integrity rules documented. Confirm the final combined scope with instructor/team; student review pending. |
| Literature review and source grounding | 10 | 7 | Prior RBI food-transmission literature plus RBI 2017 state-level Phillips-curve paper, PLFS definitions and official CPI metadata now reviewed; further study of state-panel methodology and expectations/output-gap alternatives remains. |
| Data acquisition and validation | 20 | 13 | 2012-base Combined CPI remains validated. All-India Urban PLFS 27Q input retained; state-quarter UR/RSE and state CPI source routes are documented and blank templates prepared. Urban CPI data still not acquired; state-wise Apr/May 2020 not compiled. |
| Descriptive facts and variance decomposition | 12 | 10 | Food/non-food volatility and covariance-aware decomposition substantially complete. Need matched Urban inflation/unemployment descriptive statistics and plots for the Phillips workstream. |
| Food-to-non-food/core spillover workstream | 15 | 8 | v3.3 estimates, core comparison and diagnostics exist and reproduce. Claude's v3.3 audit has blocking/material code/inference fixes; common-driver monthly data remain outstanding; claims not frozen. |
| Phillips-curve comparison | 20 | 4 | Aggregate leverage diagnostic reproduced; pre-analysis plan revised after Claude; state-level panel identified as candidate and RBI literature benchmarked. No Urban CPI values or Phillips estimates yet. |
| Empirical claim/source freeze | 5 | 0 | Pending all data validation, v3.3 audit reconciliation and Phillips-curve inference. |
| Student-authored report | 7 | 0 | Deliberately not started. Students will write in their own words after the evidence/claims are settled; required 3,000–4,000 main-text words, with course AI-use limit respected. |
| Submission QA and disclosure | 3 | 2 | Reproducible Stage 5 package and logs exist. Stage 6 source files, audit gates, instructor clarifications and final disclosure review remain. |
| **Total** | **100** | **50** | |

### Why the score was re-based

Adding a new major empirical objective changes the project denominator. The prior 71/100 was earned under a scorecard that did not include the Phillips-curve data build, design, estimation, inference or review. Retaining 71 as the current total would overstate completion of the expanded problem. The prior score is not deleted; it remains a Stage 5 milestone. The rebased Stage 6 score began at 48/100 and is now 50/100; it will move only when artifacts/tests establish completion.

## 2. Research-question status

| Research question / strand | Status | Defensible current position |
|---|---|---|
| RQ2: How much headline inflation variation is attributable to food? | Substantially complete | Food and Beverages accounts for 90.59% of seasonally adjusted monthly headline CPI-change variance under the covariance-aware decomposition (89.60% raw; 81.06% YoY descriptive). Statistical attribution, not causation. |
| RQ1: Does excluding food strengthen the inflation–unemployment relationship? | New; not estimated | Matched urban quarterly PLFS/CPI design is feasible in principle. The direct paired slope difference is the primary estimand. No Phillips-curve result exists yet. All aggregate UR regression inference remains non-confirmatory under the design-specific null simulations. |
| Supporting: Does food inflation predict later non-food/core inflation? | Substantially developed; not frozen | v3.3 finds no statistically detectable robust positive delayed association, but low power means small associations are not ruled out. Interpret reverse direction as exploratory. |

## 3. Active workstreams and next actions

### Priority A — new Phillips-curve objective

1. (Complete) Transcribe and source all 27 old-design PLFS urban quarterly CWS UR observations (Apr–Jun 2018 to Oct–Dec 2024); check overlaps and run the dedicated data tests.
2. Acquire all-India Urban CPI 2012-base General and six group indices. The official CPI Warehouse route and its expected filter configuration are now documented; the warehouse/API could not be accessed to retrieve the payload in this environment. Preserve the blank input template until an official extract is received. Add raw source, provenance, spot-checks and SHA-256.
3. Construct Urban operational core using groups 2, 3, 4 and 6 with normalised official Urban weights; validate the aggregation and label its item-level caveat.
4. Resolve pandemic-quarter data treatment and freeze quarterly inflation construction.
5. Send the updated Stage 6 package to Claude for a design/data/inference review; reconcile blocking/material findings.
6. Discuss the design and its limitations with both students; version, hash and freeze the specification before running regressions.
7. Estimate headline and core Phillips regressions on the same quarters and test `beta_core - beta_headline` directly. Preserve all failed/alternative specifications in the log.

### Priority B — v3.3 spillover audit remediation

1. Add mutation-protecting tests for the fixed-regressor block-wild bootstrap (restricted null, HAC bandwidth, plus-one p-value, Rademacher multipliers, interval endpoints) and the q=1 COVID horizon / all-zero columns.
2. Add model-specific bootstrap seeds and increase draws for headline p-values; re-check near-threshold results with about 50,000 draws.
3. Show HC3 intervals beside HAC intervals and state the low power / minimum detectable effect limitation.
4. Replace the self-consistent null-size exercise with an independent recursive/GARCH design; keep its results design-specific.
5. Add lagged log relative price to the reverse equation as a labelled post-results sensitivity; keep the reverse relationship exploratory.
6. Remove stray `bench_*` files, regenerate the relevant manifests and verify a clean extraction.
7. Update the verified October-2026 PIB/MoSPI source URL and audit log.

### Priority C — common-driver sensitivity for spillover work

1. Capture the official monthly INR Indian-basket crude series from PPAC or document access limitations.
2. Capture monthly USD/INR from RBI DBIE and determine whether monthly average or end-month is appropriate before estimation.
3. Capture policy-rate timing from official RBI sources and predeclare event/level coding.
4. Align all controls to the CPI sample without interpolating annual data; estimate only as Tier-B sensitivity, not as a replacement for Tier-A.

### Priority D — evidence freeze and report gate

Only after A–C have been assessed: freeze claims, tables, source register and limitations; obtain final student review and instructor clarification; then begin the student-authored report and submission QA.

## 4. Stage 6 current facts and guardrails

- **PLFS sample:** 27 quarterly observations under the old urban CWS design, April–June 2018 to October–December 2024. The Phillips-curve estimand is explicitly Urban India, not a rural-plus-urban national relationship. The source-transcribed CSV has 27 unique ordered quarter IDs, no missing UR values, and 17/17 matching cross-bulletin comparisons across 16 quarters. Official Table 7 source locations have been checked across all quarters; values are retained at published one-decimal precision. This is not a microdata re-estimation.
- **Urban 2012-base weights:** Food 36.29; Pan/Tobacco 1.36; Clothing/Footwear 5.57; Housing 21.67; Fuel/Light 5.58; Miscellaneous 29.53. Four-group core weight sum 58.13. The weight vector is backed by an official MoSPI release table; the six monthly Urban index series are not yet in the package.
- **Urban core caveat:** item indices for the old 2012 base are Combined-only per the warehouse availability description. The Urban group-exclusion core retains items such as vehicle fuel and precious metals within Miscellaneous.
- **PLFS API:** not used for this data file. The series was manually transcribed from official bulletin PDFs; the PLFS API schema was inspected but no authenticated API extract was obtained. Keep the old 2018–2024 observations separate from the redesigned post-Jan-2025 series.
- **Urban CPI acquisition:** the official Warehouse and monthly annexure route is documented in `documentation/stage6_urban_cpi_acquisition_protocol.md`. The Warehouse timed out; current eSankhyiki v2.0.0 catalogue describes a paginated guest-access `getCPIData` endpoint; the separate older API manual/Swagger document token-based `getCPIIndex` routes. These are different API generations and not interchangeable. No successful API payload was obtained. The 156-month template remains blank; the 0.50-point group-composite tolerance is explicitly provisional pending a genuine Urban export. No CPI-based statistics or estimates are permitted until source data arrive.
- **No interpolation:** none for missing PLFS months/quarters or annual crude-to-monthly conversion.
- **No claims about the new relationship:** no regression estimates, correlations or slope comparisons have been run in Stage 6.
- **No report drafting yet:** report remains deferred until the evidence and claims are reviewed and frozen.

## 5. Current deliverable register

| Artifact | Purpose | Status |
|---|---|---|
| `phillips_curve_data_feasibility_stage6.md` | Sources, target sample, CPI Urban weights, construction and acquisition checklist | Updated; PLFS source transcription complete, Urban CPI pending |
| `stage6_urban_cpi_acquisition_protocol.md` | Exact Urban CPI source route, API-version discrepancy, data dictionary and acceptance checks | Created; source route documented, payload still pending |
| `data/raw/plfs_urban_quarterly_ur_2018_2024.csv` | 27-quarter official PLFS urban CWS UR transcription with row-level provenance | Complete; 27 Stage 6 tests pass in total (six PLFS/pair and 21 CPI-validator mutation/structure tests); students should spot-check original bulletins |
| `data/raw/plfs_urban_quarterly_ur_source_reconciliation_stage6.csv` | Per-quarter overlap values and bulletin cross-checks | Complete; 17/17 comparisons match across 16 quarters |
| `tests/test_stage6_plfs_ur_data.py` | Automated source-transcription and structure checks | Complete; 6 tests pass |
| `outputs/tables/stage6_plfs_ur_validation.txt` | Validation result and scope boundary | Generated; explicitly states no CPI construction or estimation |
| `data/raw/cpi_2012_urban_groups_TEMPLATE.csv` | Empty monthly Urban CPI input template, Jan-2013–Dec-2025, with component flags and source metadata | Created; not a data file |
| `src/validate_stage6_urban_cpi.py` and `tests/test_stage6_urban_cpi_validator.py` | Strict intake validation for a future 156-month Urban CPI CSV | Created; 21 dedicated synthetic validator tests; 27 Stage 6 tests pass in total; no real CPI data validated |
| `data/raw/urban_cpi_group_weights_2012.csv` | Official 2012-base Urban CPI group weights and normalised core weights | Source located; arithmetic checked |
| `phillips_curve_preanalysis_plan_stage6.md` | Hypotheses, estimand, primary model, inference proposal and freeze gates | Draft complete; not frozen |
| `CLAUDE_REVIEW_PROMPT_STAGE6_PHILLIPS_DESIGN.md` | Independent pre-estimation review prompt | Ready to send to reviewer |
| `chatgpt_independent_tracker_stage6.md` | Rebased project tracker and ordered workstreams | Current |
| `ai_usage_log_stage6_checkpoint1.md` | AI-assisted research/design activity for this checkpoint | Updated; historical v3.3 `ai_usage_log.md` restored byte-identically |

## 6. Academic integrity and responsibility

ChatGPT and Claude have assisted with research framing, data discovery, code, diagnostics and documentation. These materials are drafts/work products, not student-authored report prose. Both students must review the sources, run and understand the code, challenge the claims and write the final report in their own words. The instructor's exact measurement of the 30% AI-content cap and the handwritten “20–30% of own…” note still require clarification. No student approval is recorded in this tracker.


## 7. Checkpoint 1 update — 18 November 2026

**Revised score: 50/100.** The +2 reflects a reproduced aggregate-UR leverage diagnostic, a revised pre-analysis plan, a stronger CPI intake validator (synthetic tests only), a reproducible null-size simulation, new state-panel feasibility research and an explicit Claude audit reconciliation. It does **not** credit any actual CPI data acquisition or Phillips-curve regression.

### Priority A — checkpoint 1 evidence

| Deliverable | Status | What is still not done |
|---|---|---|
| Claude B1 leverage reproduction | Completed | Independent Claude confirmation pending; this documents weak identification rather than solving it. |
| B2 pandemic and state-CPI gap treatment | Completed in design/templates | Need actual CPI panel and exact sample mask once data arrive. |
| B3 synthetic null-size calibration | Script, CSV and interpretation summary created; 2,000 replications per sample × DGP × method, seed recorded | Claude must independently reproduce and judge realism; no procedure declared confirmatory. |
| B4 q/q SAAR and YoY construction revision | Pre-analysis plan updated | CPI acquisition and seasonal adjustment with pandemic flags must be tested. |
| B5 strict Urban CPI validator and anchors | Code/templates/tests implemented | Only synthetic inputs tested; raw export, real SHA, 8 source anchors and composite residual still absent. |
| B6 decision rule | Explicit sign/influence rule written | Needs Claude challenge; inference cannot be decisive with current design. |
| State-panel candidate | Feasibility established in principle; 21 candidate state/UT units templated | Need complete state UR + RSE transcriptions, state CPI export, state weights, geographic concordance, gap/missingness analysis and small-cluster calibration. RSE examples show state estimates can be imprecise. |
| Claude Checkpoint 1 review | Prompt ready | Send package and obtain independent report before Checkpoint 2. |

### Current critical dependencies

1. Actual All-India Urban CPI 2012-base monthly export and/or state-wise Urban CPI group/general export with metadata and original bytes.
2. State-specific group weights from MoSPI Annexure II for each included panel unit.
3. PLFS state UR and UR-RSE tables across the chosen quarter span, same bulletin vintage.
4. Claude review of whether Candidate B can safely become primary and whether the aggregate should remain descriptive only.

### No-go rule

No headline/core regression or correlation until real CPI data pass the strict validator, the sample and transformation are frozen, and Claude has reviewed the amended design. The state panel must not fill Apr/May 2020 state CPI gaps with All-India imputation or nowcasts. Report drafting remains deferred.
