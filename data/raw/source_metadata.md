# Source metadata and reconciliation record

## 1. `cpi_2012_combined_groups_source_export.xlsx` and `_source_export.csv`
- User-supplied MoSPI/eSankhyiki CPI table export, preserved unchanged in `data/raw/`.
- Fields in the original export: base year, year, month code/name, state, sector, group, subgroup, index, inflation, status.
- Selection represented by the relevant records: base year 2012=100, All India, Combined, monthly, January 2013–December 2025.
- It contains overall group series, CPI General, CFPI, and subgroup-level observations. The original workbook is retained as the immutable source record; the CSV is a row-for-row text export for audit/search purposes.

## 2. `cpi_2012_combined_groups.csv` — principal analytical input
- One row per month, January 2013–December 2025 (156 observations).
- Series: All-India Combined CPI, base 2012=100.
- Variables: General/headline index; six CPI groups (Food and Beverages; Pan, Tobacco and Intoxicants; Clothing and Footwear; Housing; Fuel and Light; Miscellaneous); CFPI; and published headline YoY inflation.
- The headline index and published headline YoY series are taken from `cpi_2012_combined_headline_official.csv`. The workbook's General-Overall values were checked against the existing headline file for every month; the index observations match.
- Group and CFPI index observations are taken from their corresponding `*-Overall` rows in the workbook export.
- `cfpi` is retained as a separate alternative food-price measure. It is not interchangeable with the Food and Beverages CPI group.

## 3. Housing-index recovery
- The workbook export has no `index` values for the Combined Housing group in ten months: December 2018 through September 2019. The rest of the Housing series is populated.
- These ten values were recovered from the Housing row in Annexure I of the respective official monthly MoSPI/NSO CPI releases published by the Press Information Bureau (PIB). The selected month values are the final indices reported in the subsequent monthly release.
- Recovered values: 2018-12 146.5; 2019-01 147.7; 2019-02 148.5; 2019-03 149.0; 2019-04 149.7; 2019-05 150.1; 2019-06 149.4; 2019-07 150.6; 2019-08 151.6; 2019-09 152.2.
- Month-by-month release titles, URLs, and selected values are documented in `housing_index_recovery_sources.csv`.
- These are not interpolated values. They are values transcribed from official release tables. The original workbook remains unchanged.

## 4. Pan/Tobacco December 2025 reconciliation
- The supplied workbook export lists the Combined Pan, Tobacco and Intoxicants index for December 2025 as 215.9.
- The official December 2025 CPI release (base 2012=100), and the project's independently prepared official spot-check table, list it as 215.8.
- The analytical input uses 215.8. The discrepancy is explicitly recorded in `source_reconciliation.csv`; the original workbook continues to show the supplied export value of 215.9.

## 5. Official spot checks
- `group_spotcheck_from_dec2025_release.csv` contains official Combined indices for December 2024, November 2025 and December 2025, including CFPI.
- Source: MoSPI/NSO CPI release for December 2025, dated 12 January 2026; Annexures I and II.
- The `spotcheck_groups.py` script compares all seven index series (General, six groups and CFPI) in the analytical input against these official values. This is a targeted check, not proof that every month is error-free.

## 6. Published headline CPI series
- `cpi_2012_combined_headline_official.csv`: All-India General CPI (Combined), base 2012=100, January 2013–December 2025; published YoY inflation January 2014–December 2025.
- Source: MoSPI/NSO press release, "Consumer Price Index numbers on base 2012=100 for rural, urban and combined for the month of December, 2025", dated 12 January 2026; Annexures VI (index) and VII (YoY).
- December 2025 index and inflation are provisional.
- April–May 2020 require special provenance treatment. The source index series in this project reflects MoSPI/NSO's later business-continuity reconstruction, which contains imputed components; it should not be described as an entirely observed-price series. The published headline YoY comparison fields for April and May 2020 remain blank in this project because the original contemporaneous release did not publish a General CPI/YoY inflation rate for those months. See Section 13.

## 7. Weights and group aggregation
- Combined CPI group weights used in `src/config.py`: Food and Beverages 45.86%; Pan, Tobacco and Intoxicants 2.38%; Clothing and Footwear 6.53%; Housing 10.07%; Fuel and Light 6.84%; Miscellaneous 28.32%. They sum to 100%.
- The weighted group sum is treated as a reconstruction diagnostic, not as a requirement for exact equality with the published headline index. MoSPI's national combined group/headline construction may exhibit small residuals due to the aggregation procedure and rounding.

## 8. Sample and data vintage
- Raw index coverage: January 2013–December 2025. January 2013 is retained to calculate the first year-on-year observation in January 2014.
- Primary analysis sample: January 2014–December 2025 (144 months).
- This is a historical 2012-base dataset ending December 2025. It is not live/current CPI data through 2026. Do not append the 2024-base series without a documented linking and comparability assessment.

## 9. Status flags
- The original workbook's `status` field is retained in the untouched source workbook and its row-wise CSV export. Codes such as `F`, `F*`, and `F+` are preserved as source metadata; no interpretation is assigned here without an authoritative status-code legend.

## 10. Food subgroup indices and weights
- The preserved row-level eSankhyiki export contains all 12 Food and Beverages subgroup indices for all 156 months from January 2013 to December 2025.
- The source selection is 2012 base, All India, Combined. The subgroup names are Cereals and Products; Meat and Fish; Egg; Milk and Products; Oils and Fats; Fruits; Vegetables; Pulses and Products; Sugar and Confectionery; Spices; Non-alcoholic Beverages; and Prepared Meals, Snacks, Sweets etc.
- Official Combined subgroup weights are recorded in `data/raw/food_subgroup_combined_weights_2012.csv`, based on the MoSPI 2012-base press-release Annexure I. They sum to 45.86%, matching the published Food and Beverages group weight. Source: https://www.mospi.gov.in/sites/default/files/press_release/cpi_pr_12apr16t.pdf
- The corrected descriptive script constructs a weighted subgroup-rebuilt food index and compares it with the published Food and Beverages index. The observed mean absolute gap is 0.0333 index points and maximum absolute gap is 0.0934 index points in the current build. This is a validation check, not forced equality.
- The food-ex-vegetables proxy is the fixed-weight aggregate of the other 11 subgroup indices, renormalized to the remaining 39.82% food weight. It is a derived proxy, not an official published MoSPI series.

## 11. Operational core CPI composition caveat
- The project's operational core CPI excludes Food and Beverages and Fuel and Light, while retaining the Miscellaneous group.
- The MoSPI item-level Combined weight table (2012 base) shows that selected vehicle petrol/diesel/lubricant items and gold/silver/other ornaments are located within Miscellaneous subgroups. Their combined weight is 3.58866% of the full CPI basket: 2.38499% vehicle petrol/diesel/lubricants and 1.20367% gold/silver/other ornaments.
- The workbook export does not contain the monthly item-level indices needed to remove these items. Accordingly, the project documents the limitation and does not claim that core is entirely insulated from fuel or precious-metal movements.
- Source: https://www.cpi.mospi.gov.in/Weight_AI_Item_Combined_2012.aspx
- Item weights are transcribed in `data/raw/core_retained_item_weights_2012.csv`.

## 12. Current analysis windows and generated dataset
- The processed analytical dataset now preserves all 156 index observations from January 2013 to December 2025.
- Year-on-year inflation begins in January 2014; month-on-month/log inflation begins in February 2013.
- Seven source event-month flags are created for March–September 2020. The two MoSPI headline YoY collection-gap flags for April and May 2020 remain separate from the April–May imputed-component provenance flag. The econometric model does not enter the seven flags individually; it constructs one pooled affected-window control based on the maximum lag horizon.


## June 2013 Housing index discontinuity
The supplied All-India Combined 2012-base Housing index rises from 100.5 in May 2013 to 106.6 in June 2013. The cause has not been established from the source material reviewed. The observation is preserved unchanged. The v3.2 post-results specification retains October 2013 for q=3 configurations with maximum lag no greater than three. Any configuration with p or q above three is programmatically required to start in January 2014 or later, preventing June 2013 from entering through longer lags. January 2014 is always reported alongside the October 2013 baseline. Do not attribute a cause without locating and citing the relevant MoSPI methodology note.

## 13. April–May 2020 reduced-basket release and later imputed series
- The contemporaneous MoSPI/NSO release for April 2020 (PIB release dated 12 May 2020) explains that personal price collection was suspended from 19 March 2020 and April prices were largely obtained by telephone, supplemented by limited neighbourhood purchases. Prices were compiled only for items meeting the adequacy criteria (reported from at least 25% of markets and representing more than 70% of the relevant subgroup/group weight). The initial April release did not compile Meat and Fish or Prepared Meals, Snacks, Sweets etc. under Food & Beverages; Pan, Tobacco and Intoxicants; Clothing and Footwear; most Miscellaneous subgroups; or General CPI. It did publish a partial Food & Beverages group measure excluding Meat and Fish and Prepared Meals, and a CFPI excluding Meat and Fish.
- MoSPI/NSO subsequently issued the *CPI Technical Note on Imputation*. It explains that only 13 of 23 subgroups in April and 15 of 23 in May had initially been compiled/disseminated. To produce a continuous full index series, the NSO imputed missing food subgroups using the Food & Beverages group index and missing non-food subgroups using the General CPI calculated from observed-price subgroups. The note then recalculated the General CPI for all 23 subgroups. Its Table 1 marks April–May imputed indices with `@` and explicitly warns that the reconstructed April–May series is a business-continuity estimate, with a significant share of price data not captured.
- The values in `cpi_2012_combined_groups.csv` and the row-level source export for April–May 2020 match the later MoSPI imputed table for the corresponding All-India Combined index series (including General CPI, Food & Beverages, Pan/Tobacco, Clothing/Footwear, Housing, Fuel & Light, Miscellaneous and CFPI). This is distinct from the smaller set of partial indices in the first April press release. At the subgroup level, availability/imputation differs by cell; do not claim every series component was imputed.
- A direct value check against the later technical-note Table 1 gives the following All-India Combined matches (index points):

  | Series | April 2020 | May 2020 |
  |---|---:|---:|
  | General CPI | 151.4 | 150.9 |
  | Food & Beverages | 154.0 | 152.7 |
  | Pan, Tobacco and Intoxicants | 173.2 | 174.4 |
  | Clothing and Footwear | 152.0 | 152.3 |
  | Housing | 155.6 | 155.6 |
  | Fuel and Light | 144.1 | 142.5 |
  | Miscellaneous | 145.5 | 146.2 |
  | CFPI | 153.4 | 151.8 |

  The technical note marks individual imputed entries with `@`; imputation is component-specific, not a claim that every item/group in both months was imputed. The row-level source export's F/F*/F+ status codes are retained without assigning them a broader meaning than the official note supports.
- `flag_covid_imputed_series_month` in the processed dataset marks April and May 2020 as months containing one or more components from the later reconstructed/imputed series. It is a month-level provenance flag, not a claim that every index in those months is imputed. The separate `flag_collection_gap` marks the two months for which published headline YoY rates are not available.
- The regressions use a horizon-aware pooled COVID-affected-window control. Separate sensitivities exclude April–May 2020 and, more broadly, March 2020–December 2021. Results involving April–May 2020 should be interpreted with this data-vintage caveat.
- Official sources: MoSPI/NSO, *Price Movement of Selected Sub-Groups/Groups of Consumer Price Index ... for April 2020*, PIB Release ID 1623298, 12 May 2020, https://www.pib.gov.in/PressReleasePage.aspx?PRID=1623298&lang=2&reg=48; MoSPI/NSO, *Compilation of Consumer Price Index: A Technical Note* (imputation methodology and April–May 2020 reconstructed tables), https://www.mospi.gov.in/sites/default/files/press_release/CPI%20Technical%20Note%20on%20Imputation.pdf.
