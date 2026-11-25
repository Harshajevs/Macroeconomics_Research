# Stage 6 aggregate synthetic null-size simulation — summary

**Purpose:** assess finite-sample rejection rates under selected synthetic null outcome processes using the observed 27-quarter PLFS Urban unemployment regressor as fixed design. This is not an inflation dataset, not a Phillips-curve estimate, and not a proof that any method is valid.

- Seed: `45520261118`
- Replications per sample × outcome process × method: `2,000`
- Nominal two-sided size: `5%`
- Samples: all 27 quarters; and 24 quarters excluding 2020Q2, 2020Q3 and 2021Q2
- Outcome processes: iid q/q-like shocks; four-quarter overlapping MA process; four-quarter MA with AR(0.5) innovations; random walk
- Methods: conventional OLS t, HC3 t, calendar-lag HAC(3) and HAC(4) t

## Selected rejection rates

| Sample | Synthetic process | OLS iid | HC3 | HAC(3) | HAC(4) |
|---|---|---:|---:|---:|---:|
| full27 | iid_qoq | 5.1% | 7.8% | 22.2% | 24.1% |
| full27 | yoy_ma3 | 19.4% | 10.2% | 23.3% | 24.3% |
| full27 | yoy_ma3_ar05 | 28.3% | 10.3% | 26.5% | 27.0% |
| full27 | random_walk | 46.4% | 6.8% | 29.6% | 27.7% |
| drop_2020Q2_2020Q3_2021Q2 | iid_qoq | 4.8% | 3.5% | 10.7% | 12.2% |
| drop_2020Q2_2020Q3_2021Q2 | yoy_ma3 | 30.0% | 28.0% | 20.8% | 21.4% |
| drop_2020Q2_2020Q3_2021Q2 | yoy_ma3_ar05 | 39.6% | 38.0% | 27.4% | 27.4% |
| drop_2020Q2_2020Q3_2021Q2 | random_walk | 68.0% | 65.3% | 56.2% | 55.8% |

## Interpretation and limits

The simulation shows severe over-rejection by HAC(3/4) in many small-sample persistent/overlapping designs. HC3 is closer to nominal in the full sample for some processes but is not uniformly calibrated, especially in the 24-quarter sample with persistent or random-walk outcomes. Conventional OLS behaves reasonably only under the iid q/q-like DGP and fails under overlap/persistence. No method should be described as confirmatory for the aggregate UR design on the strength of this simulation.

Monte Carlo standard errors for individual rates are in `stage6_aggregate_null_size_simulation.csv`; for 2,000 draws and a 5% rate, the approximate MCSE is 0.49 percentage points. Rates far from 5% are not sampling noise around the nominal level.

The DGP family is limited and synthetic. The fixed observed UR regressor is conditioned upon; the exercise does not capture the joint generation of unemployment and inflation, structural breaks, survey measurement uncertainty, estimated seasonal adjustment, or cross-state dependence. Independent Claude review is required before any method is used for inference.
