# Stage 6 — Phillips-curve data feasibility and source protocol

**Prepared:** 17 November 2026  
**Status:** PLFS unemployment input transcribed from official quarterly bulletins and structurally validated; Urban CPI monthly index acquisition remains pending.  
**Scope:** New Phillips-curve objective added to the HS455 project. This note does not revise or replace the v3.3 food-spillover data or specification.

## 1. Decision in brief

A defensible matched-frequency, matched-geography design appears feasible using the pre-redesign Periodic Labour Force Survey (PLFS) quarterly urban estimates and the 2012-base all-India Urban CPI series. **The estimand is an Urban India relationship, not a national rural-plus-urban Phillips Curve.** The all-India label here means all-India coverage of the urban population. Rural unemployment is not available at the same pre-2025 quarterly frequency in this PLFS bulletin series, and an annual national series is too short for a comparable quarterly slope test.

- **Unemployment:** all-India urban unemployment rate, persons aged 15 years and above, Current Weekly Status (CWS), quarterly bulletin series.
- **Inflation geography:** all-India Urban CPI, base 2012=100.
- **Expected primary window:** April–June 2018 to October–December 2024, at most 27 quarters. The first calendar year contributes three quarters (April–June, July–September and October–December); 2019–2024 contribute four quarters each.
- **Post-January-2025 PLFS:** kept separate because the survey design was redesigned. Do not append it to the old quarterly series as if it were the same uninterrupted sample.
- **Core measure:** an explicitly labelled *urban group-exclusion operational core*, constructed from the four non-food, non-fuel CPI groups using the 2012-base Urban weights. It is not an exact item-purged RBI core.

The 27-quarter PLFS CWS unemployment series has now been transcribed from the official bulletin PDFs, source-tagged and validated for calendar completeness. Seventeen overlapping-bulletin comparisons across 16 quarters match at the published one-decimal precision. This is a reproducible transcription of published estimates, not a re-estimation from PLFS microdata. The Urban CPI group-index extract is still outstanding, so no common inflation–unemployment dataset exists and no Phillips-curve estimation is permitted yet.

## 2. PLFS unemployment series

### 2.1 Exact target series

| Dimension | Required selection |
|---|---|
| Indicator | Unemployment rate (UR) |
| Frequency | Quarterly bulletin |
| Geography | All India |
| Sector | Urban |
| Age | 15 years and above |
| Gender | Person (all genders combined) |
| Labour-force status | Current Weekly Status (CWS), as reported in the quarterly bulletin |
| Units | Per cent of the labour force |

The PLFS quarterly bulletin defines CWS unemployment using a seven-day reference period: a person is classified as unemployed if they did not work for at least one hour on any day in the reference week and sought or was available for work for at least one hour on any day in that week. The quarterly estimate therefore represents a short-period measure, not the annual usual-status unemployment rate.

### 2.2 Frequency and method break

The old PLFS design produced quarterly CWS estimates for urban areas only. MoSPI's PLFS documentation describes the revamped design from January 2025, which added monthly all-India rural/urban CWS estimates and extended quarterly coverage to rural areas. The redesigned survey must not be silently concatenated with the previous quarterly urban series.

The official PLFS API documentation identifies quarterly data for 2018–2026 and records that for 2018–2024 the quarterly sector available is Urban; Rural and Rural+Urban quarterly series start in 2025. It identifies the relevant query codes as:

| Filter | Code |
|---|---:|
| `indicator_code` — unemployment rate | `3` |
| `frequency_code` — quarterly bulletin | `2` |
| `state_code` — All India | `99` |
| `gender_code` — Person | `3` |
| `age_code` — 15 years and above | `1` |
| `sector_code` — Urban | `2` |
| `quarter_code` | `2` Jul–Sep; `3` Oct–Dec; `4` Jan–Mar; `5` Apr–Jun |

The PLFS API schema and filters were inspected, but no authenticated API response was obtained. The unemployment values in this package were therefore transcribed directly from the official quarterly bulletin PDFs, not downloaded through the API. The source-coded file `data/raw/plfs_urban_quarterly_ur_2018_2024.csv` records the primary bulletin, Statement 5, printed page, release metadata where available, URL and retrieval date for every quarter. `data/raw/plfs_urban_quarterly_ur_source_reconciliation_stage6.csv` records overlapping-bulletin checks. The transcription is retained at the one-decimal precision published by MoSPI; it should not be interpreted as having greater precision.

### 2.3 Expected sample calendar

| Calendar year | Quarters expected under old urban quarterly PLFS | Count |
|---|---|---:|
| 2018 | Apr–Jun; Jul–Sep; Oct–Dec | 3 |
| 2019 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| 2020 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| 2021 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| 2022 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| 2023 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| 2024 | Jan–Mar; Apr–Jun; Jul–Sep; Oct–Dec | 4 |
| **Total** | **Apr–Jun 2018 to Oct–Dec 2024** | **27** |

This calendar is now populated in the source-transcribed input. The validation confirms 27 distinct, chronologically ordered quarter IDs from 2018Q2 to 2024Q4 with no missing UR values. The values are rounded to one decimal as in the bulletins. This check establishes completeness of the transcription and consistency of the recorded overlap checks; it does not rule out later official revisions or replace a review against the original PDFs by the students. Do not fill a missing or revised quarter by interpolation.

### 2.4 Completed bulletin transcription and overlap checks

The source-transcribed series is stored in `data/raw/plfs_urban_quarterly_ur_2018_2024.csv`. It contains one row per quarter and records the selected official source bulletin, Statement 5, printed page, release-date metadata (or an explicit note where the exact date was not located), source URL, retrieval date and any second bulletin used for an overlap check. The companion `data/raw/plfs_urban_quarterly_ur_source_reconciliation_stage6.csv` expands each overlap into a separate audit row.

| Quarter | UR (%) | Quarter | UR (%) | Quarter | UR (%) |
|---|---:|---|---:|---|---:|
| 2018Q2 | 9.7 | 2018Q3 | 9.6 | 2018Q4 | 9.7 |
| 2019Q1 | 9.2 | 2019Q2 | 8.8 | 2019Q3 | 8.3 |
| 2019Q4 | 7.8 | 2020Q1 | 9.1 | 2020Q2 | 20.8 |
| 2020Q3 | 13.2 | 2020Q4 | 10.3 | 2021Q1 | 9.3 |
| 2021Q2 | 12.6 | 2021Q3 | 9.8 | 2021Q4 | 8.7 |
| 2022Q1 | 8.2 | 2022Q2 | 7.6 | 2022Q3 | 7.2 |
| 2022Q4 | 7.2 | 2023Q1 | 6.8 | 2023Q2 | 6.6 |
| 2023Q3 | 6.6 | 2023Q4 | 6.5 | 2024Q1 | 6.7 |
| 2024Q2 | 6.6 | 2024Q3 | 6.4 | 2024Q4 | 6.4 |

Seventeen comparisons between overlapping official bulletins across 16 distinct quarters match exactly at the published one-decimal precision. These checks cover the overlapping 2018Q3–2019Q2, 2021Q4–2022Q1, 2022Q2–2022Q4, 2023Q1–2023Q4 and 2024Q1–2024Q3 values. Eleven quarters have only one source bulletin recorded in this reconciliation; their primary source and exact table/page are still preserved in the CSV. The automated test suite checks the 27-quarter calendar, source metadata, values and all 17 overlap comparisons.

**Pandemic-data caution.** The October–December 2020 bulletin explains that PLFS fieldwork was suspended from 18 March 2020 and resumed from 1 June 2020; pending schedules were subsequently collected, with responses linked to the actual reference period. The published urban CWS UR rises to 20.8% in 2020Q2 and remains 13.2% in 2020Q3. These observations are retained in the primary transcription rather than dropped after seeing the values. The pre-analysis plan retains separate, pre-declared pandemic-quarter exclusion sensitivities. This UR collection note must be considered jointly with the separate Urban CPI source/vintage and imputation review once the CPI data are obtained.

The validation output is `outputs/tables/stage6_plfs_ur_validation.txt`; the tests are in `tests/test_stage6_plfs_ur_data.py`. Passing these checks confirms internal consistency and the recorded cross-bulletin matches, not an independent survey re-estimation or full official-methodology audit. The SHA-256 of the PLFS input CSV at this Stage 6 checkpoint is `2ee4d29c50499143084b5262f7c0361d2d2613bf7b4fdd249ed029a1254068e0`; the Stage 6 manifest records hashes for the supporting files as well.

## 3. Urban CPI series and weights

### 3.1 Availability

MoSPI's CPI Warehouse states that 2012-base all-India sub-group, group, General and Consumer Food Price Indices are available separately for Rural, Urban and Combined sectors from January 2013 onwards. It separately states that old-base item-level indices are Combined-only from January 2014 onwards. Thus the group-level Urban series needed for a matched-geography exercise exist in the official data system; the current v3.3 package, however, contains the Combined group data and does not yet contain the required Urban extract.

The 2012-base Urban group series is demonstrably part of the public CPI data system, but acquisition has not yet succeeded in this work session. MoSPI's National Metadata Structure (metadata last updated 13 February 2026) states that the 2012-base CPI series continues through December 2025, that monthly press releases are accompanied by Excel annexures, and that the 2012-base data through December 2025 are available from the CPI Warehouse. The CPI Warehouse page itself timed out from the research environment during this pass, and the eSankhyiki API page rendered its catalogue text but not a machine-readable schema or data payload. No Urban CPI rows have therefore been downloaded or validated.

There is also an API-documentation version discrepancy that must not be glossed over. The current eSankhyiki CPI catalogue describes API v2.0.0, endpoint `getCPIData`, and says a bearer token is optional for guest access subject to rate limits. The publicly indexed NSO India `esankhyiki-mcp` CPI Swagger file is version 1.0.11 and documents the earlier group endpoint `getCPIIndex` with `base_year`, `series`, `year`, `month_code`, `state_code`, `group_code`, `sector_code`, `limit`, `page` and `Format` parameters, under bearer-token security. These may describe different API versions. A direct attempt to fetch the documented endpoint did not return a usable payload in this environment. Treat both as retrieval leads, not proof of an authenticated or successful data extract. The full discrepancy and manual warehouse route are recorded in `documentation/stage6_urban_cpi_acquisition_protocol.md`.

A World Bank reproducibility catalogue documents a MoSPI-derived workbook named `CPI_R_U_subgroups_Jan11_May24.xlsx`, with Urban, Rural and Combined group/subgroup indices downloaded from the MoSPI Warehouse for January 2013–May 2024. This is useful corroboration that the warehouse export contains the required Urban group series and identifies its coverage, but it is a third-party reproducibility-package record—not a substitute for obtaining the source workbook or verifying the data against MoSPI. Do not silently copy another project's values into this package.

The source acquisition target is monthly All-India Urban 2012-base index values for January 2017–December 2024 at minimum, for:

1. General Index (all groups);
2. Food and Beverages (Group 1);
3. Pan, Tobacco and Intoxicants (Group 2);
4. Clothing and Footwear (Group 3);
5. Housing (Group 4);
6. Fuel and Light (Group 5);
7. Miscellaneous (Group 6).

January 2017 is sufficient to form year-on-year rates for every quarter from April–June 2018. A longer pull from January 2013 is preferable for full provenance and descriptive checks.

### 3.2 Official 2012-base Urban weights

The official CPI release table for the old 2012-base basket gives the following all-India Urban group weights:

| Group | Urban weight (%) | Treatment in operational core |
|---|---:|---|
| Food and Beverages | 36.29 | Excluded |
| Pan, Tobacco and Intoxicants | 1.36 | Retained |
| Clothing and Footwear | 5.57 | Retained |
| Housing | 21.67 | Retained |
| Fuel and Light | 5.58 | Excluded |
| Miscellaneous | 29.53 | Retained |
| **Total** | **100.00** | |

The included weights sum to 58.13%. Renormalised weights for the four retained groups are:

| Retained group | Renormalised core weight (%) |
|---|---:|
| Pan, Tobacco and Intoxicants | 2.3396 |
| Clothing and Footwear | 9.5820 |
| Housing | 37.2785 |
| Miscellaneous | 50.7999 |
| **Total** | **100.0000** |

### 3.3 Operational urban core construction

Subject to obtaining and validating all four Urban group indices, construct:

\[
I^{C,U}_t = \frac{1.36 I^{U}_{2,t}+5.57 I^{U}_{3,t}+21.67 I^{U}_{4,t}+29.53 I^{U}_{6,t}}{58.13}.
\]

Use the official MoSPI Urban General Index as the headline measure rather than a reconstructed six-group index. As a data-quality check, independently reconstruct a six-group index using the same weights and compare it with the official General Index; document the size and time pattern of the residual rather than assuming exact additivity.

Call this measure **Urban operational core (excluding Food and Beverages and Fuel and Light groups)**. Since 2012-base Urban item indices are not publicly listed in the warehouse availability statement, this group-level index cannot remove petrol/diesel and precious-metal items separately when they sit inside Miscellaneous. Do not describe it as the exact RBI item-purged core. The earlier Combined operational core definition and results remain unchanged.

## 4. Frequency alignment and candidate inflation series

The unemployment target is quarterly. Convert each monthly CPI index series to a quarterly mean index using the three calendar months belonging to the quarter. The primary inflation definition proposed for review is the year-on-year log change in quarterly-average index:

\[
\pi^{j}_q = 100\left[\ln(\bar I^{j}_q)-\ln(\bar I^{j}_{q-4})\right],\qquad j\in\{H,C\},
\]

where \(\bar I_q\) is the arithmetic mean of the three monthly index levels in quarter \(q\), \(H\) is the official Urban General Index, and \(C\) is the constructed Urban operational core index. The rate is in approximate percentage points per year.

A sensitivity series can be formed by averaging the three monthly year-on-year log inflation rates within each quarter. The primary transformation should be finalised before looking at its regression relationship with unemployment. Do not mix 2012-base historical CPI with the 2024-base series beginning in 2025.

## 5. Data-acquisition checklist

| Task | Status | Acceptance condition |
|---|---|---|
| Obtain PLFS age-15+, person, urban, all-India, quarterly CWS UR series | Complete — bulletin transcription | 27 unique quarter rows; every row source-tagged; 17 overlap comparisons across 16 quarters match; automated tests pass |
| Obtain Urban 2012-base CPI monthly General and six group indices | Pending | At least Jan-2017–Dec-2024, complete month calendar, correct sector and base verified |
| Obtain/verify official Urban group weights | Source located; arithmetic checked | Weight vector sums to 100; retained four-group core weight sum is 58.13 |
| Construct the Urban operational core | Blocked on CPI extract | Formula and weights documented; reproduce exactly from raw groups |
| Verify quarterly CPI/unemployment alignment | Pending | Matching quarter keys, no duplicate or missing quarters; all transformations reproducible |
| Audit pandemic-period source treatment | Partial | PLFS 2020 fieldwork note and UR shock recorded; Urban CPI Apr–May 2020 vintage/imputation still needs verification |
| Store source register and checksums | Partial | PLFS row-level URLs, pages and retrieval date recorded; add file hash/manifest; CPI source payload and full request/retrieval log pending |

## 6. Explicit no-go rules

- No interpolation of monthly unemployment, no interpolation of missing quarters, and no blending of annual usual-status UR with quarterly CWS UR.
- No use of Combined CPI as the primary inflation series against Urban unemployment.
- No use of the 2024-base CPI as a seamless continuation of the 2012-base series.
- No claim of exact RBI-style core if petrol/diesel cannot be removed at item level from the Urban series.
- No estimation until the raw data are complete, validated and the pre-analysis plan has received the intended independent review and team discussion.

## 7. Official source register

1. MoSPI, CPI Warehouse, current series page: https://cpi.mospi.gov.in/ . The Time Series route is described as `https://cpi.mospi.gov.in/TimeSeries_2012.aspx`; the page did not load in this research environment.
2. MoSPI, National Metadata Structure for CPI, updated 13 February 2026: https://mospi.gov.in/sites/default/files/CPI/National_Metadata_Structure_for_CPI.pdf . It records the old 2012-base series through December 2025, monthly Excel annexures, and the CPI Warehouse as the old-series source.
3. MoSPI, CPI Press Release, Annexure I (base 2012=100), April 2018: https://www.mospi.gov.in/sites/default/files/press_release/CPI_PR_12apr18th.pdf . It gives Urban weights and Urban group indices, including the weights used above.
3. MoSPI, PLFS Quarterly Bulletin, April–June 2022: https://mospi.gov.in/sites/default/files/publication_reports/Quarterly%20Bulletin%20PLFS%20April%20June%202022_0.pdf .
4. MoSPI, PLFS Quarterly Bulletin, October–December 2022: https://mospi.gov.in/sites/default/files/publication_reports/QuarterlyBulletinPLFSOctoberDecember2022.pdf .
5. MoSPI, PLFS Quarterly Bulletin, April–June 2023: https://www.mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_April%20_June_2023.pdf .
6. MoSPI, PLFS Quarterly Bulletin, July–September 2024: https://www.mospi.gov.in/sites/default/files/publication_reports/QuarterlyBulletinPLFS_July_September_2024.pdf .
7. MoSPI PLFS Quarterly Bulletin, April–June 2019: https://www.mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_April_June_2019_M_0.pdf .
8. MoSPI PLFS Quarterly Bulletin, July–September 2019: https://mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_July_September_2019_M.pdf .
9. MoSPI PLFS Quarterly Bulletin, October–December 2020: https://mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_October_December_2020L2.pdf .
10. MoSPI PLFS Quarterly Bulletin, January–March 2022: https://mospi.gov.in/sites/default/files/publication_reports/Quarterly%20Bulletin%20PLFS%20January%20-%20March%202022_m1655370580105.pdf .
11. MoSPI PLFS Quarterly Bulletin, October–December 2022: https://www.mospi.gov.in/sites/default/files/publication_reports/QuarterlyBulletinPLFSOctoberDecember2022.pdf?download=1 .
12. MoSPI PLFS Quarterly Bulletin, April–June 2023: https://www.mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_April%20_June_2023.pdf .
13. MoSPI PLFS Quarterly Bulletin, October–December 2023: https://www.mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_October-December_2023.pdf .
14. MoSPI PLFS Quarterly Bulletin, July–September 2024: https://mospi.gov.in/sites/default/files/publication_reports/QuarterlyBulletinPLFS_July_September_2024.pdf .
15. MoSPI PLFS Quarterly Bulletin, October–December 2024: https://mospi.gov.in/sites/default/files/publication_reports/PLFS_Quarterly_Bulletin_Oct-Dec24.pdf .
16. MoSPI eSankhyiki Data Catalogue: https://esankhyiki.mospi.gov.in/catalogue-main/catalogue?page=0&product=PLFS .
17. Official NSO India PLFS API specification (filters, coverage and authentication): https://raw.githubusercontent.com/nso-india/esankhyiki-mcp/main/swagger/swagger_user_plfs.yaml .
18. Official NSO India CPI API specification repository (Swagger file currently indexed as v1.0.11; older `getCPIIndex` route and bearerAuth requirement): https://github.com/nso-india/esankhyiki-mcp/blob/main/swagger/swagger_user_cpi.yaml .
19. Current eSankhyiki CPI API catalogue (v2.0.0; `getCPIData`, token described as optional): https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api . The documented route is `https://api.mospi.gov.in/api/cpi/getCPIData`; its current machine-readable parameter schema and a successful 2012 Urban response were not obtained during this pass.
20. World Bank, Reproducibility Package for India: Trends in Poverty, 2011–12 to 2022–23, data catalogue: https://reproducibility.worldbank.org/index.php/catalog/280 . The metadata describes the MoSPI Warehouse-derived workbook `CPI_R_U_subgroups_Jan11_May24.xlsx`, downloaded for January 2013–May 2024 with Rural, Urban and Combined group/subgroup indices. Use as a source-discovery corroboration only, not as the primary CPI input.
21. RBI, Handbook of Statistics, Table 163: Consumer Price Index — Monthly, dated 31 July 2026: https://www.rbi.org.in/SCRIPTs/PublicationsView.aspx?id=23988 . It corroborates the availability of Urban General CPI on the old 2012 base through December 2025, but the version inspected does not provide the required historical Urban group panel.

**Review note:** The PLFS quarterly values in this package were transcribed from the official bulletin PDFs and overlap-checked as described above; the API was not used to download them. The CPI warehouse/API descriptions identify availability and candidate retrieval routes but do not replace the actual Urban index payload. Keep the Urban CPI evidence status as `source located` until monthly values are captured and validated.
