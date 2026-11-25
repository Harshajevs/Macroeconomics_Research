# Claude Stage 6 adversarial audit — reconciliation log (18 November 2026)

**Source review:** Claude, *HS455 Stage 6 Phillips-Curve Design: Independent Pre-Estimation Audit*, 17 November 2026.  
**Status:** Checkpoint 1 amendments implemented in the working copy; not yet independently re-audited. No Phillips-curve model has been estimated. The Urban CPI source file is still missing. Student review/approval remains pending.

## 1. Blocking findings

| Audit item | Finding | Action in Checkpoint 1 | Status / remaining gate |
|---|---|---|---|
| B1 | Aggregate UR slope dominated by 2020Q2; 3 pandemic quarters explain 75.4% of UR variation; remaining series trends down sharply | Reproduced diagnostic from the project's 27 PLFS values; added per-quarter variation share/leverage and sample summaries. 2020Q2/Q3/2021Q2 contribute 75.43% of full-sample centred SS. After exclusion, the re-centred 24Q SS is 17.39% of full 27Q SS; retained rows measured around the original 27Q mean account for 24.57%; sample variance ratio is 19.66%. Both 27-quarter and 24-quarter samples retained as predeclared co-primary descriptive comparisons. | **Addressed as a design warning**, not solved. Aggregate time-series slope remains weakly identified; no confirmatory claim permitted. |
| B2 | 2021Q2 omitted from pandemic/imputation set; April/May 2020 state CPI values unavailable | All-India Urban CPI template records component-specific Apr/May 2020 macro-imputation flags from the MoSPI technical note. State CPI template labels Apr/May 2020 `not_compiled_by_MoSPI`; state-level panel cannot fill these months from all-India series. YoY 2021Q2 is flagged because 2020Q2 base is absent at state level. | **Addressed in template and design**; full state panel still requires source data and quarter-level missingness audit. |
| B3 | HC3/HAC/wild procedures poorly calibrated at n=24–27, especially with persistent inflation | Added a reproducible fixed-regressor synthetic null-size calibration for OLS, HC3, HAC(3), HAC(4), four outcome processes, both samples, 2,000 replications by default. Results are diagnostic and design-specific. | **Partly addressed.** Claude must independently review DGPs and results; no method is declared reliable. Aggregate analysis remains descriptive/exploratory. |
| B4 | YoY quarter averages overlap MA(3), effective independent windows about 7; proposed lag and block choices mismatched | Revised plan makes SA annualised q/q and quarterly-average YoY co-primary transformations; no lagged YoY inflation. For state panel, q/q/YoY gaps from uncompiled state CPI are explicit. | **Addressed at design level**; q/q seasonal adjustment needs review against missing-value handling before estimation. |
| B5 | Validator missed level/range, composite, jump, identical-column, anchor and source-hash defects | Replaced validator with level range 90–300, group-composite residual check, jump flags/hard fail, identical-column check, eight source anchors, per-row macro-imputation flags, export metadata and raw-file SHA-256 verification. Expanded template to 2013-01–2025-12. | **Code implemented; synthetic tests only.** Real CPI acceptance not achieved until actual Warehouse/official export, anchors and digest are supplied. |
| B6 | Strengthening decision rule ambiguous | Revised plan explicitly requires negative headline/core slopes and negative direct difference across all prespecified samples/transforms to discuss strengthening; point estimate alone is insufficient. | **Addressed conceptually**, but no p-value decision rule will be treated as confirmatory until small-sample calibration is credible. |

## 2. Material findings

| Audit item | Resolution |
|---|---|
| M1 paired-difference algebra | Retained as the correct direct comparison only when the same sample and regressors are used; state and time fixed effects must be identical in both outcome equations. A synthetic unit test verifies the OLS identity to numerical tolerance. |
| M2 PLFS provenance and vintage | Existing all-India 27-quarter input retained with its primary and overlap provenance. New state-level PLFS template requires Table 7 UR and Table 3RSE/UR RSE from the same bulletin vintage. Do not silently mix vintages. Each cell must have source/page/table metadata. |
| M3 27-quarter window and YoY base | The all-India aggregate design retains CPI coverage back to 2013. The state panel template uses monthly CPI from 2013 onward and flags the Apr/May 2020 state gap; no false complete YoY series is assumed. |
| M4 urban operational core | The all-India core weights remain 2.3396, 9.5820, 37.2785, 50.7999. Added a no-Housing sensitivity to the plan. The state panel must use the relevant state's Annexure-II weights, not the national Urban vector. |
| M5 acquisition provenance | The all-India CPI intake requires original export, SHA-256, export/retrieval dates, filter settings, provisional/final status and the eight press-release anchors. State-panel data have separate templates and no fill from imputed national series. |
| M6 timing | Match CPI quarter averages to the same PLFS quarter. Any lagged-U specification is secondary and uses common sample only. |
| M7 tracker | Rebased tracker updated and readiness score not inflated; state panel remains a proposed route under independent review. |

## 3. Corrections arising from the full MoSPI technical note

The official MoSPI CPI Technical Note says that insufficient price quotations meant **state-level indices and the all-India General CPI could not be compiled contemporaneously in April and May 2020**. The subsequently disseminated all-India group and General indices contain flagged macro-imputed values. For the Urban all-India row, Table 1 marks:

- April 2020: General, Food & Beverages, Pan/Tobacco, Clothing & Footwear, Miscellaneous as imputed; Housing and Fuel & Light are not marked.
- May 2020: General, Food & Beverages, Clothing & Footwear, Miscellaneous as imputed; Pan/Tobacco, Housing and Fuel & Light are not marked.

The `@` flag means imputed. This is recorded separately for each component. It is not correct to apply those all-India flags to the state CPI panel: state indices were not compiled for the two months. A later RBI paper also documents that missing state-wise April/May 2020 data prevent directly deriving state-level YoY for April/May 2021.

## 4. New methodological discovery: state-panel feasibility

The original aggregate UR series is weakly identified because a few quarters account for most of its time-series variation. A state-quarter panel could exploit cross-state differences in Urban unemployment and prices, broadly following the subnational-panel motivation in the RBI 2017 Phillips-curve paper. Official PLFS quarterly bulletins provide state-wise UR Table 7 and separate RSE tables; MoSPI CPI Warehouse documentation says state-wise 2012-base Urban group/general indices are available for major states and state-wise group weights are published in Annexure II.

However, state CPI indices are unavailable for April/May 2020, and state-level CPI series are not a seamless monthly panel through this episode. A state panel is therefore **feasible in principle but not yet validated**. The prepared state templates deliberately exclude Jammu & Kashmir pending an old/new boundary concordance and include 21 candidate units otherwise represented in the PLFS state table. The review prompt asks Claude to challenge:

1. State list, CPI major-state coverage, state/UT and J&K/Ladakh concordance.
2. PLFS UR and RSE extraction, release-vintage consistency, and minimum-RSE rules.
3. State-specific CPI weights and basket construction.
4. State-level April/May 2020 gaps and loss of 2021Q2 YoY inflation.
5. Whether two-way fixed effects identify within-state, within-quarter variation; cluster inference with roughly 21 state/UT units and 27 quarters; and whether a small-cluster wild bootstrap is defensible.
6. Whether the panel should be a candidate primary design, secondary extension or abandoned in favour of a transparent aggregate descriptive comparison.

No primary design change is frozen until this independent review is returned.

## 5. Files and code added

- `src/validate_stage6_urban_cpi.py` — strengthened All-India Urban CPI intake validator.
- `src/stage6_aggregate_null_size_simulation.py` — synthetic null-size diagnostic using observed PLFS UR as fixed regressor.
- `data/raw/cpi_2012_urban_groups_TEMPLATE.csv` — blank all-India Urban 2012-base monthly CPI template, Jan-2013–Dec-2025.
- `data/raw/cpi_2012_urban_anchor_checks_TEMPLATE.csv` — eight-month official press-release anchor template.
- `data/raw/plfs_state_urban_ur_2018_2024_TEMPLATE.csv` — candidate state-quarter UR and RSE template.
- `data/raw/cpi_state_urban_2012_groups_TEMPLATE.csv` — candidate state-level monthly CPI template; Apr/May 2020 explicitly marked not compiled.
- `data/raw/cpi_state_urban_group_weights_TEMPLATE.csv` — state-specific CPI group weight template.
- `outputs/tables/stage6_aggregate_ur_leverage_*` and `outputs/figures/stage6_aggregate_ur_leverage_diagnostics.png` — reproduced leverage diagnostic.

## 6. No-go rules retained

- No Phillips regressions until actual CPI series passes all intake checks, the candidate design is reviewed, and the specification is frozen and hashed.
- No substitution of Combined CPI for Urban CPI.
- No interpolation or imputation of missing state CPI values; no use of RBI nowcasts as observed CPI.
- No separate bootstrap for headline and core.
- No causal interpretation.
- No statement that the Phillips curve strengthens based solely on separate significance levels or a negative point estimate.
- No report drafting or claim freeze before student review and Claude's next audit.
