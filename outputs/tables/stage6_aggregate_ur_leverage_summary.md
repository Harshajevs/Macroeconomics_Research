# Stage 6 aggregate unemployment leverage diagnostic

- **sample_definition:** All-India Urban PLFS CWS unemployment rate, persons 15+, 2018Q2–2024Q4
- **n_full:** 27
- **mean_full_pct:** 8.877777777777778
- **sd_full_pct:** 2.984360946067057
- **high_leverage_observations:** [{"quarter_id": "2020Q2", "ur_pct": 20.8, "variation_share_pct": 61.38162489537183, "leverage": 0.6508532859907554}, {"quarter_id": "2020Q3", "ur_pct": 13.2, "variation_share_pct": 8.06748449903768, "leverage": 0.11771188202741384}, {"quarter_id": "2021Q2", "ur_pct": 12.6, "variation_share_pct": 5.983131540926268, "leverage": 0.09686835244629972}]
- **three_quarter_variation_share_pct:** 75.43224093533578
- **n_after_exclusion:** 24
- **sd_after_exclusion_pct:** 1.3233617161925375
- **remaining_within_sample_ss_share_of_full_ss_pct:** 17.39437886857636
- **retained_original_mean_ss_share_pct:** 24.567759064664205
- **sample_variance_ratio_after_vs_full_pct:** 19.66321089491241
- **corr_ur_with_compressed_row_order_after_exclusion:** -0.869557742881649
- **corr_ur_with_original_calendar_time_after_exclusion:** -0.8457532908081311
- **interpretation:** These are leverage/variation diagnostics from unemployment alone. They are not Phillips-curve estimates. The 17.39% figure uses the remaining 24 observations re-centred on their own mean; 24.57% uses the same remaining values measured around the original 27-quarter mean. These are different sums of squares, not contradictory estimates.

This diagnostic is calculated from the 27 PLFS unemployment observations only. No CPI data, correlation, or Phillips-curve estimate is used.
