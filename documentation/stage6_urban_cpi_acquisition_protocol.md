# Stage 6 — Urban CPI acquisition protocol (2012 base)

**Prepared:** 18 November 2026  
**Status:** Source route established; raw Urban CPI extract not yet acquired.  
**Purpose:** Obtain a source-auditable monthly All-India Urban CPI panel to match the pre-redesign PLFS Urban quarterly CWS unemployment series.

## 1. Exact data required

The required input is **monthly All-India Urban CPI, base 2012=100, Current Series**, with one observation per calendar month for January 2013–December 2025 (156 months). The matched PLFS estimation window remains 2018Q2–2024Q4; the longer CPI history is required for defensible seasonal adjustment and source validation, while the YoY transformation needs CPI data beginning no later than 2017Q2. Pull the six group indices and the official general index:

- General Index (all groups)
- Group 1: Food and Beverages
- Group 2: Pan, Tobacco and Intoxicants
- Group 3: Clothing and Footwear
- Group 4: Housing
- Group 5: Fuel and Light
- Group 6: Miscellaneous

The Urban general index is the headline outcome. The operational core is a fixed-weight index constructed from groups 2, 3, 4 and 6. Do not substitute the Combined sector, a State aggregate with a different definition, the 2024-base CPI, or a third-party calculated inflation rate.

The validator and template now require 156 consecutive month rows, January 2013–December 2025. The January–May 2013 portion needs special scrutiny for the Urban Housing/General series: the current series held them at 100 before full rent sampling, while MoSPI later documented a research back-series. Do not silently substitute or splice that back-series. Keep it separate and consider it only as a clearly labelled STL-history sensitivity after independent review.

## 2. Primary source: MoSPI CPI Warehouse

Official entry point: https://cpi.mospi.gov.in/  
Documented 2012-base current-series page: https://cpi.mospi.gov.in/TimeSeries_2012.aspx

The research pass established from MoSPI's National Metadata Structure for CPI (metadata last updated 13 February 2026) that old 2012-base CPI data run through December 2025 and are available in the CPI Warehouse. The MoSPI metadata also confirms that monthly press releases include Excel annexures. During the current research pass the Warehouse page timed out, so no export was obtained.

The following export configuration is corroborated by a World Bank reproducibility catalogue describing its own download from this same MoSPI Warehouse. Use it as a guide, and verify the actual current UI labels before exporting:

1. Open the CPI Warehouse.
2. Select `Time Series`.
3. Select `Base 2012`.
4. Select `Current Series` (not Back Series).
5. Set the period to January 2013–December 2025.
6. Select All India coverage and all groups/subgroups.
7. Retain the Urban sector series; if the export offers Rural, Urban and Combined together, do not delete the other sectors until the raw file has been archived.
8. Export the source file and preserve it unmodified in `data/raw/source_downloads/` with the original filename.
9. Create a separately cleaned Urban-only input in `data/raw/cpi_2012_urban_groups.csv`; record the exact source-file name, query settings, retrieval date and SHA-256 of both raw and cleaned files.

The World Bank catalogue entry is `https://reproducibility.worldbank.org/index.php/catalog/280`. It documents a workbook called `CPI_R_U_subgroups_Jan11_May24.xlsx`, sourced from the MoSPI CPI Warehouse, with Current Series January 2013–May 2024, All States, all groups/subgroups and Rural/Urban/Combined variables. This confirms a published route and historical coverage but is not permission to replace the primary MoSPI download with a copied workbook. If a team member obtains this workbook as a fallback, it must be retained as a separately sourced secondary copy and spot-checked against MoSPI monthly press-release annexures before use.

## 3. API route: unresolved version discrepancy

The current eSankhyiki CPI API catalogue at https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api describes API v2.0.0, endpoint `GET /api/cpi/getCPIData`, and an open API where the bearer token is optional for guest access, subject to per-IP rate limits. The catalogue says the endpoint is paginated and returns a JSON envelope. Its live catalogue page did not expose the complete machine-readable query schema to this research environment.

There is a separate official MoSPI API user manual at https://www.api.mospi.gov.in/API/CPI%20API%20User%20Manual.pdf. It documents the older `GET /api/getCPIIndex` group/subgroup endpoint and says first-time registration and login provide a 15-minute access token; without that token, the older API returns only the first 10 records. The currently indexed NSO India `esankhyiki-mcp` CPI Swagger file at https://github.com/nso-india/esankhyiki-mcp/blob/main/swagger/swagger_user_cpi.yaml is version 1.0.11 and documents the newer-looking path `GET /api/cpi/getCPIIndex` with the query names `base_year`, `series`, `year`, `month_code`, `state_code`, `group_code`, `subgroup_code`, `sector_code`, `limit`, `page`, and `Format`, and bearer-token security. That schema covers 2012/2010/2024 base years; state and sector filters on the group endpoint; the state code `99` for All India; and 1–3 sector codes. The item endpoint’s state/sector parameters are specified for 2024, consistent with the lack of state-level item detail on the 2012 base.

These documents may describe different API generations and route versions. Do not assume the v1.0.11 query names can be passed to v2.0.0 `getCPIData`. An attempted direct API request did not yield a usable payload, and the local execution environment had no network DNS resolution. Therefore:

- Do not treat the old v1.0.11 schema as authoritative for the current v2 endpoint without confirmation.
- Do not claim that the new v2 endpoint has been successfully accessed.
- Do not insert any values returned by an undocumented or unverified query.
- If using the API later, save the precise endpoint, query parameters, request timestamp, response headers/metadata, pagination, and untouched JSON/CSV payload before transformation.

## 4. Secondary official verification: monthly CPI press-release annexures

MoSPI publishes a monthly CPI press note with an Excel annexure. The National Metadata Structure describes this dissemination process. The annexure contains Rural, Urban and Combined columns, with Urban weights and indices at group level. An April 2018 example is available at:

https://www.mospi.gov.in/sites/default/files/press_release/CPI_PR_12apr18th.pdf

Use the monthly annexures as a spot-check source for selected months across the sample (at minimum: first month, last month, one pre-pandemic month, April–May 2020 and one month per year). The PDF table is an audit cross-check, not an efficient primary method for transcribing all 156 months if the Warehouse export is available. When comparing a Warehouse time series with press-release values, note that the press release includes a provisional latest month and final previous month; the vintage can matter for early pandemic months.

## 5. Data dictionary and acceptance checks

The cleaned file should match the blank structure in `data/raw/cpi_2012_urban_groups_TEMPLATE.csv` and contain:

| Field | Required meaning |
|---|---|
| `month` | Unique `YYYY-MM` calendar month |
| `urban_general_index` | All-India Urban general index, 2012=100 |
| `food_beverages_group1_index` | Group 1 Urban index |
| `pan_tobacco_group2_index` | Group 2 Urban index |
| `clothing_footwear_group3_index` | Group 3 Urban index |
| `housing_group4_index` | Group 4 Urban index |
| `fuel_light_group5_index` | Group 5 Urban index |
| `miscellaneous_group6_index` | Group 6 Urban index |
| source metadata | Original filename/URL, release metadata, retrieval date, provisional/final status if provided, and notes |

Acceptance conditions before any inflation construction:

1. Exactly one unique observation per calendar month; full 156-month sequence from 2013-01 through 2025-12 with no missing group/general values.
2. Confirm 2012 base, Current Series, All India and Urban sector from export metadata, not filename inference.
3. Confirm values are CPI index levels, not inflation rates; never mix levels and YoY rates.
4. Cross-check the six group indices and General Index against official monthly annexures at selected dates; include a pandemic-vintage check for April and May 2020.
5. Verify the six Urban weights sum to 100.00 and reproduce the fixed operational-core weights in `urban_cpi_group_weights_2012.csv`.
6. Independently calculate a fixed-weight six-group composite for comparison with the official General Index; report the residual rather than assume exact aggregation identity.
7. Build the four-group operational core only after validating all retained group indices. Name it `urban_operational_core_food_fuel_groups_excluded` in the processed dataset and clearly explain that it is not the exact item-purged RBI measure.
8. SHA-256 the untouched download and cleaned file; add both to the input manifest. Keep the download immutable.
9. Run the CPI data tests before creating the quarterly dataset. No regression or correlation work is allowed before these checks pass and the pre-analysis plan is reviewed/frozen.

## 6. Current status and no-go rule

The 27-quarter PLFS unemployment input is complete as a source-tagged bulletin transcription, with 17 matching overlap comparisons across 16 quarters. The Stage 6 suite has 27 passing tests, including synthetic CPI-validator mutations and PLFS/pair-difference checks. **The CPI side is not complete.** The template is intentionally blank; it is not data. The current work session has established source availability and a reproducible acquisition path, but has not acquired the CPI panel. No Phillips-curve correlations, regressions or slope comparisons have been run.

If the CPI Warehouse remains inaccessible to the team, obtain the export directly from the official MoSPI portal using a browser session, or request the historical Urban group-index extract from MoSPI's Price Statistics Division. Do not bypass the blocker by using Combined CPI, interpolating, or constructing an urban series from unrelated sources.

## 7. Sources

- MoSPI, National Metadata Structure for CPI (13 February 2026): https://mospi.gov.in/sites/default/files/CPI/National_Metadata_Structure_for_CPI.pdf
- MoSPI CPI Warehouse: https://cpi.mospi.gov.in/
- MoSPI 2012-base Current Series page: https://cpi.mospi.gov.in/TimeSeries_2012.aspx
- MoSPI CPI monthly release, April 2018, Annexure I: https://www.mospi.gov.in/sites/default/files/press_release/CPI_PR_12apr18th.pdf
- Current eSankhyiki CPI API catalogue (v2.0.0): https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api
- Official MoSPI CPI API User Manual (older API workflow): https://www.api.mospi.gov.in/API/CPI%20API%20User%20Manual.pdf
- NSO India CPI API Swagger repository (version 1.0.11): https://github.com/nso-india/esankhyiki-mcp/blob/main/swagger/swagger_user_cpi.yaml
- World Bank reproducibility catalogue for the 2025 India poverty trends package: https://reproducibility.worldbank.org/index.php/catalog/280
- RBI, Handbook of Statistics, Table 163 (31 July 2026): https://www.rbi.org.in/SCRIPTs/PublicationsView.aspx?id=23988
