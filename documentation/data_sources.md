# Data sources and download checklist — updated 14 Nov 2026

| Series | Source | Coverage | Base / definition | Status |
|---|---|---|---|---|
| General CPI Combined index | MoSPI Dec-2025 CPI release, Annexure VI; checked against supplied eSankhyiki workbook | Jan 2013–Dec 2025 | 2012=100 | COMPLETE; exact month-by-month match between headline file and workbook General series |
| Published General CPI YoY | MoSPI Dec-2025 CPI release, Annexure VII | Jan 2014–Dec 2025 | 2012=100 | COMPLETE; Apr–May 2020 not compiled by MoSPI |
| Six Combined CPI group indices | Supplied eSankhyiki workbook export plus official PIB/MoSPI recovery for ten missing Housing observations | Jan 2013–Dec 2025 | 2012=100 | COMPLETE; see raw source export and recovery audit |
| CFPI Combined | Supplied eSankhyiki workbook export; checked at Dec 2024, Nov 2025 and Dec 2025 | Jan 2013–Dec 2025 | 2012=100 | COMPLETE; retained as alternative food measure |
| Group weights | MoSPI Dec-2025 release, Annexure I | 2012 CPI Combined basket | weights sum to 100 | COMPLETE; configured and verified |
| Three-month group spot-check | MoSPI Dec-2025 CPI release, Annexures I-II | Dec 2024, Nov 2025, Dec 2025 | 2012=100 | COMPLETE; all seven indices match |

## Primary sources

- MoSPI CPI warehouse / eSankhyiki: https://cpi.mospi.gov.in/ and https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api
- MoSPI/NSO December 2025 CPI release (12 January 2026), final release of 2012-base series: https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2213736
- Official housing-index recovery sources are listed month-by-month in `data/raw/housing_index_recovery_sources.csv`.

## Data integrity notes

- The original eSankhyiki workbook is preserved unchanged at `data/raw/cpi_2012_combined_groups_source_export.xlsx`; its row-wise CSV export is alongside it.
- The workbook provided all target overall series, but the Housing `index` cell was blank for Dec 2018–Sep 2019. Those ten Combined values were transcribed from the Housing row of official monthly PIB/MoSPI CPI Annexure I releases and are documented in `data/raw/housing_index_recovery_sources.csv`. These are source-recovered observations, not interpolations.
- The supplied workbook lists Pan/Tobacco Dec 2025 as 215.9, while the official December 2025 release and project spot-check show 215.8. The analytic file uses 215.8 and preserves the difference in `data/raw/source_reconciliation.csv`.
- `cpi_2012_combined_groups.csv` contains 156 monthly rows, with 2013 used to calculate the first YoY value in Jan 2014. The main analysis window is Jan 2014–Dec 2025 (144 observations).
- The old 2012-base series ends in Dec 2025. No 2024-base back-series has been appended. This is not a real-time 2026 dataset.
- Group weights: Food and Beverages 45.86%; Pan, Tobacco and Intoxicants 2.38%; Clothing and Footwear 6.53%; Housing 10.07%; Fuel and Light 6.84%; Miscellaneous 28.32%.
- Food and Beverages is the primary food measure. CFPI is retained as a separate alternative measure and is not interchangeable with Food and Beverages.
- Non-food excludes Food and Beverages but includes Fuel and Light. Core excludes Food and Beverages and Fuel and Light.
- April–May 2020 have CPI indices but no published official headline YoY rates because MoSPI did not compile those rates during the COVID collection disruption. Calculated index-based rates are flagged and sensitivity output excluding those months is provided.

## Reproducibility checklist

- [x] Full monthly group dataset acquired and assembled
- [x] Source workbook preserved unchanged
- [x] Housing gaps recovered from official releases and logged
- [x] Dec 2025 Pan/Tobacco discrepancy reconciled and logged
- [x] Headline index matched across workbook and official headline CSV
- [x] Three-month official spot-check passes for headline, six groups and CFPI
- [x] Real-data integration test passes
- [x] Descriptive food/non-food outputs generated
- [ ] Econometric specification frozen and estimated
- [ ] Robustness and diagnostic stage completed
