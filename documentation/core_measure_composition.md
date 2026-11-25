# Operational core CPI: definition and composition caveat

**Project definition:** `core` is the weighted CPI aggregate excluding the Food and Beverages and Fuel and Light groups. This follows the conventional group-level definition used in Indian CPI analysis. It is a derived group-weighted index from the 2012-base All-India Combined series.

## Important retained items

The official MoSPI All-India Item Combined Weight table (2012 base) shows that the Miscellaneous group includes the Transport and Communication subgroup and the Personal Care and Effects subgroup. The item weights include vehicle petrol/diesel/lubricants and gold/silver/other ornaments. These remain inside the project's operational core measure because they are within Miscellaneous, which is retained when Food and Beverages and Fuel and Light are excluded.

| Items retained inside operational core | Combined CPI weight (%) |
|---|---:|
| Petrol for vehicle | 2.18697 |
| Diesel for vehicle | 0.14800 |
| Lubricants and other fuels for vehicle | 0.05002 |
| Gold | 1.08035 |
| Silver | 0.11175 |
| Other ornaments | 0.01157 |
| **Total** | **3.58866** |

Vehicle fuel items together have a combined CPI weight of 2.38499%; gold, silver and other ornaments together account for 1.20367%.

## What this project can and cannot do

- It can state accurately that the operational core series excludes the entire Fuel and Light group, but still retains the listed items located within Miscellaneous.
- It cannot create a core-ex-petrol/diesel/gold/silver index from the current dataset because the source workbook provides monthly indices for aggregate subgroups, not the individual item price indices needed to remove those items.
- Do not claim that operational core is entirely insulated from energy or precious-metal price movements.
- Keep core as a pre-declared robustness outcome, with this caveat in the methodology and results sections.

## Sources

MoSPI, All India Item CPI (Combined) Weights (Base Year: 2012): https://www.cpi.mospi.gov.in/Weight_AI_Item_Combined_2012.aspx

RBI Bulletin (2026), Table IV.1.2, All-India CPI Combined weighting structure, 2012=100: https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23800

The original MoSPI item-weight page lists item codes and Combined weights. The accompanying CSV `data/raw/core_retained_item_weights_2012.csv` records the selected items used in this note.
