# ChatGPT-led Stage 3 change log — 14 November 2026

## Data and sample
- Processed dataset expanded from 144 to 156 rows, preserving Jan-2013 raw series and deriving MoM from Feb-2013.
- Added four separate March–June 2020 pulse indicators and retained the two April–May collection-gap flags.
- Added official 2012-base food subgroup Combined weights and subgroup-level analytical outputs.

## Corrected inference
- Archived the old YoY correlation/lead-lag and circular YoY bootstrap outputs as legacy.
- Replaced the original descriptive script with a corrected pipeline: YoY moments explicitly descriptive-only; STL applied to log index levels before differencing for MoM.
- Added a paired stationary bootstrap, automated Politis–White/Patton–Politis–White block-length selection, 6/12/24 sensitivity and explicit Monte Carlo resolution.
- H2 retired as confirmatory; MoM shape statistics are exploratory only.

## Additional analysis
- Added food subgroup stylised facts and weighted food-ex-vegetables proxy (derived, not official).
- Added individual non-food group volatility comparison.
- Added covariance-aware group contribution-to-variance decomposition.
- Added core composition caveat and retained item weights.

## Econometric specification
- Dated v3.0 pre-estimation specification: group-built non-food primary outcome, food lags 0–3, own lags p=0–3 selected by BIC, month indicators, four COVID pulses, delayed-lag joint test and cumulative delayed effect.
- No formal spillover regression estimated yet.

## Validation status
- Updated real-data integration test for 156-row processed data and 155-row MoM window.
- Added Stage-3 output/schema tests.
- Fresh-extraction smoke test remains to be run after final packaging.

## Final execution record — 14 Nov 2026
- Executed compileall, synthetic test, real-data integration test, official group spot-check, headline analysis, RBI descriptive comparison, full dataset build, corrected descriptive analysis and Stage-3 econometric/design tests.
- All executed commands passed. The synthetic test is explicitly software-only; real-data test covers the authentic CPI source.
- Formal distributed-lag spillover regression remains deliberately unestimated pending student sign-off and the next modelling milestone.
