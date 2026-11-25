# Stage 6 Checkpoint 1 — evidence ledger

| Claim / fact | Evidence in package | Status |
|---|---|---|
| All-India Urban PLFS UR spans 27 quarters 2018Q2–2024Q4 | `data/raw/plfs_urban_quarterly_ur_2018_2024.csv` and source reconciliation | Existing project input; source-transcribed, subject to student spot-check |
| Three pandemic quarters account for most UR variance | New outputs `stage6_aggregate_ur_leverage_*` | Recomputed from PLFS values only |
| Aggregate regression inference is unreliable at this size | New synthetic null-size script/CSV | Illustrative design-specific simulation; Claude review pending |
| 2012-base state-wise Urban CPI exists for major states | MoSPI CPI Warehouse metadata | Source availability, not downloaded values |
| State CPI was not compiled Apr/May 2020 | MoSPI technical note | Official source fact; state-panel gap must remain missing |
| PLFS state UR and RSE available in quarterly bulletins | Table 7 and Appendix A Table 3RSE (examples checked in 2019 bulletin) | Source route confirmed; full panel not transcribed |
| State-specific Urban CPI weights available | MoSPI CPI Changes in Revised Series, Annexure II | Source route confirmed; weight template blank |
| All-India Urban CPI General/groups Jan2013–Dec2025 | MoSPI CPI Warehouse metadata | Availability indicated; no actual extract obtained |
| Food accounts for 90.59% of Combined headline monthly variance | v3.3 verified result table | Historical result, unchanged |
| Phillips curve strengthens after food exclusion | No estimates in package | Not established; do not claim |
