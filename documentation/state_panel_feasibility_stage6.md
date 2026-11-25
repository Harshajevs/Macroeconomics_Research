# Stage 6 — State-level Phillips-curve panel: feasibility and unresolved gates

**Prepared:** 18 November 2026. This is a source-based feasibility note, not a dataset or a frozen design.

## 1. Why examine a panel?

The all-India Urban PLFS unemployment time series has only 27 quarterly observations. A three-quarter pandemic set accounts for roughly three-quarters of its total variation. Dropping those quarters leaves 24 observations with a strong downward trend. This makes an aggregate time-series Phillips slope fragile.

The RBI's 2017 paper, Behera, Wahi and Kapur, explicitly motivates subnational inflation Phillips-curve panels because state data provide more observations and greater dispersion in regional inflation and demand indicators. It studies state-level CPI and output-gap data, not our exact PLFS Urban unemployment design, so it is a methodological precedent rather than a directly comparable result.

## 2. Official data evidence

### PLFS state-quarter unemployment

- The January–March 2019 PLFS quarterly bulletin (Table 7, page A-12) reports state-wise Urban UR under Current Weekly Status for age 15 years and above, with a Person column. The October–December 2024 bulletin (Table 7, pages A-35–A-36 depending on rendered pagination; use the PDF's printed page labels during extraction) has a separately labelled 15+ Urban table and a separate all-age table.
- Table 7 reports state-wise UR by gender and quarter; it contains a `person` category and, in the early bulletin, age-group 15 years and above.
- Appendix A has separate RSE tables, including Table 3RSE for unemployment rate. RSE should be collected alongside the state estimate, since state-quarter UR is not equally precise.
- The January–March 2019 bulletin's Table 7 explicitly labels the state-wise Urban UR series as age 15 years and above, with a Person column covering April–June 2018 through January–March 2019. The October–December 2024 bulletin also contains a separate Table 7 for age 15 years and above (October–December 2023 through October–December 2024); it separately publishes an all-age table, so extraction must select the correctly labelled 15+ table rather than infer from table number alone.
- The October–December 2024 bulletin also contains a separate Table 3RSE for UR, age 15 years and above, Urban. The 2019 bulletin's RSE appendix contains a Table 3RSE as well. This confirms a source route for matching UR and RSE, although full quarter-by-quarter transcription and definition checks remain to be completed.
- The Oct–Dec 2024 bulletin includes separate 15+ and all-age state-wise UR tables; extract the explicitly labelled 15+ table only. The matching 15+ Urban Table 3RSE must be paired with it. As a warning about precision, the Oct–Dec 2024 bulletin reports Delhi Person UR RSE of 27.3% for Oct–Dec 2023 and 26.5% for Jul–Sep 2024. These examples make it unsafe to assume every state-quarter estimate is equally reliable; do not apply a post-result RSE cutoff without predeclaring it.

### State-level Urban CPI and weights

- MoSPI CPI Warehouse availability notes for the 2012=100 revision say state-wise sub-group/group/general indices for Rural, Urban and Combined are available from Jan 2013 onwards for major states (population over 50 lakh under Census 2011); minor states have state-wise group/general data.
- MoSPI's `CPI: Changes in the Revised Series`, Annexure II, provides State/UT-wise subgroup and group weight diagrams for CPI (Urban). State-specific core weights must be computed from each state's own weights. The national Urban group weights are not a substitute.
- The state candidate list is the 21 state/UT units appearing in Table 7 other than Jammu & Kashmir: Andhra Pradesh, Assam, Bihar, Chhattisgarh, Delhi, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Odisha, Punjab, Rajasthan, Tamil Nadu, Telangana, Uttarakhand, Uttar Pradesh and West Bengal. This is a **candidate intersection**, not proof that all 21 pass every coverage/weight/RSE gate. J&K is held out until old/new boundary and Ladakh concordance are checked. Chandigarh is also omitted because it is not in the relevant PLFS state table.

## 3. Pandemic break in state CPI

MoSPI's CPI Technical Note on Imputation (July 2020) states that insufficient price quotations meant State-level CPI indices could not be computed for April and May 2020. MoSPI later released an all-India imputed General/group series, but those are not state observations. The RBI's November 2026 paper on filling state-wise CPI-U gaps also notes the absence of state CPI in Apr/May 2020 and consequent inability to derive direct state-wise YoY inflation for Apr/May 2021.

Therefore:
- never copy All-India Urban imputed values into individual state series;
- never fill these state gaps with RBI nowcasts or interpolation in the primary observed-data panel;
- state quarterly average CPI in 2020Q2 is incomplete;
- a quarterly q/q change in 2020Q3 cannot be formed from a complete 2020Q2 base average;
- 2021Q2 state YoY inflation lacks the 2020Q2 comparison base;
- produce an explicit state × month/quarter missingness map and common sample before estimation.

This loss of observations overlaps the high-unemployment pandemic quarters, so the panel is not a simple fix for aggregate leverage.

## 4. Candidate panel specification for reviewer challenge

For state `i`, quarter `q`, outcome `m` (headline or state-specific group-based core):

`pi_m,i,q = state_FE_i + quarter_FE_q + beta_m * U_i,q + e_m,i,q`.

Direct comparison:

`(pi_core - pi_headline)_i,q = state_FE_i + quarter_FE_q + delta_beta * U_i,q + v_i,q`.

With identical sample and regressors, the direct difference coefficient equals the core-minus-headline slope. Interpretation is a within-state, within-quarter association. It is not a national aggregate Phillips curve and not causal.

Potential inference issues: only about 21 state/UT clusters and 27 quarters; serial dependence within state, common shocks across states, spatial dependence, measurement uncertainty of the PLFS state estimates, and unbalanced CPI coverage. Ask Claude whether CR2/Satterthwaite or a state-cluster wild bootstrap is defensible; consider two-way cluster dependence and a null simulation using the actual panel matrix before freezing.

## 5. Data templates created

- `plfs_state_urban_ur_2018_2024_TEMPLATE.csv`: 21 candidate state/UT units × 27 quarters, with separate UR and RSE fields and source metadata.
- `cpi_state_urban_2012_groups_TEMPLATE.csv`: 21 candidate state/UT units × Jan 2013–Dec 2025, with group/general indices and source provenance; Apr/May 2020 are explicitly `not_compiled_by_MoSPI`.
- `cpi_state_urban_group_weights_TEMPLATE.csv`: one row per candidate state/group; blank until each state's Annexure-II weights are transcribed.

All three are blank templates, not observations. A state must not enter the eventual estimation merely because it appears in the template.

## 6. Recommendation pending independent review

Keep the existing all-India Urban 27-quarter series as the transparent aggregate descriptive comparison. Evaluate the state panel as a possible main empirical design or secondary extension because it provides cross-sectional variation, but do not promote it until state CPI/PLFS/RSE data coverage, J&K/Ladakh treatment, pandemic missingness and small-cluster inference have been independently checked. If data quality and inference cannot be justified, do not use it as a stronger proof simply because it has a larger row count.

## 7. Sources

- MoSPI PLFS Jan–Mar 2019 Quarterly Bulletin: https://mospi.gov.in/sites/default/files/publication_reports/PLFS_QB_Jan-March-2019.pdf (Table 7, Table 3RSE).
- MoSPI PLFS Oct–Dec 2024 Quarterly Bulletin: https://mospi.gov.in/sites/default/files/publication_reports/PLFS_Quarterly_Bulletin_Oct-Dec24.pdf (Table 7).
- MoSPI CPI Warehouse: https://cpi.mospi.gov.in/ (2012-base state Urban index coverage).
- MoSPI, `CPI: Changes in the Revised Series`, Annexure II: https://cpi.mospi.gov.in/PDFile/CPI-Changes_in_the_Revised_Series.pdf (state Urban group weights).
- MoSPI CPI Technical Note on Imputation: https://mospi.gov.in/sites/default/files/press_release/CPI%20Technical%20Note%20on%20Imputation.pdf.
- RBI WPS (DEPR) 08/2017, `Phillips Curve Relationship in India: Evidence from State-Level Analysis`: https://rbi.org.in/Scripts/PublicationsView.aspx?id=17752.
- RBI November 2026 paper discussing absent state CPI for Apr/May 2020 and YoY base gap in Apr/May 2021: https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=24096.
