from pathlib import Path
import pandas as pd
import json,re
BASE=Path(__file__).resolve().parent
DATA=BASE/'research_data'
OUT=BASE/'tables';OUT.mkdir(exist_ok=True)

d=pd.read_csv(DATA/'results/phillips_all_specifications.csv')
d=d[d.inference_sensitivity.eq('HC3')]
def slope(freq,sample,trend,outcome):
 return float(d.loc[d.frequency.eq(freq)&d['sample'].eq(sample)&d.trend.eq(trend)&d.outcome.eq(outcome),'slope'].iloc[0])
checks=[('Full sample','full27',False,'core_food_fuel_excluded'),
 ('Exclude three pandemic quarters','exclude_three_pandemic',False,'core_food_fuel_excluded'),
 ('Exclude all of 2020--2021','exclude_2020_2021',False,'core_food_fuel_excluded'),
 ('Full sample, calendar trend','full27',True,'core_food_fuel_excluded'),
 ('Full sample, exclude food only','full27',False,'nonfood_only'),
 ('Full sample, core without housing','full27',False,'core_no_housing')]
text=r'''\begin{table}[htbp]
\centering\small
\caption{Selected slope checks: headline and alternative inflation}
\begin{tabularx}{\linewidth}{Xrrrr}
\toprule
&\multicolumn{2}{c}{YoY log}&\multicolumn{2}{c}{q/q SAAR}\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Check &Headline&Alternative&Headline&Alternative\\
\midrule
'''
for label,sample,trend,alt in checks:
 vals=[slope(f,sample,trend,o) for f in ['yoy_log','qoq_saar'] for o in ['headline',alt]]
 text+=label+' & '+' & '.join(f'{v:.3f}' for v in vals)+chr(92)*2+'\n'
text+=r'''\bottomrule
\end{tabularx}
\tabnote{Alternative means operational core unless stated otherwise. Food-only exclusion retains fuel/light; core without housing excludes food, fuel/light and housing. All comparisons within a row use identical samples and controls.}
\end{table}
'''
(OUT/'robustness.tex').write_text(text)

v=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv');v=v[v['sample'].eq('full_history')&~v.frequency.eq('MoM_STL7')]
text=r'''\begin{table}[htbp]
\centering\small
\caption{Complete covariance allocation to raw official headline variance (\%)}
\begin{tabular}{llrrrr}
\toprule
Basket &Change&Food&Fuel/light&Other four groups&Residual\\
\midrule
'''
for sector in ['Combined','Urban']:
 for frequency,label in [('MoM_raw','Monthly'),('YoY_raw','YoY')]:
  s=v[v.sector.eq(sector)&v.frequency.eq(frequency)].set_index('component').covariance_share_percent
  other=s[['pan_tobacco','clothing','housing','misc']].sum()
  text+=f'{sector} & {label} & {s.food_bev:.2f} & {s.fuel_light:.2f} & {other:.2f} & {s.aggregation_residual:.2f}'+chr(92)*2+'\n'
text+=r'''\bottomrule
\end{tabular}
\tabnote{Each row sums to 100\% before rounding. ``Residual'' closes the difference between official headline and weighted-group percentage changes. A negative residual allocation is permitted. The method allocates cross-covariances; it does not assume components are independent.}
\end{table}
'''
(OUT/'accounting.tex').write_text(text)

c=pd.read_csv(DATA/'results/spillover_recursive_calibration.csv')
text=r'''\begin{table}[htbp]
\centering\small
\caption{Recursive monthly-model calibration: rejection rates under a true zero delayed effect (\%)}
\begin{tabularx}{\linewidth}{lXrrr}
\toprule
Outcome &Error process&HAC(6)&HC3&Block-wild\\
\midrule
'''
scenarios={'iid_gaussian':'Independent Gaussian','ar_garch':'AR/GARCH Gaussian','heavy_tail_ar_garch':'AR/GARCH, heavy tails'}
for direction,outcome in [('food_to_nonfood','Non-food'),('food_to_core','Core')]:
 for scenario,label in scenarios.items():
  sub=c[c.direction.eq(direction)&c.scenario.eq(scenario)&c.true_delayed_sum.eq(0)].set_index('method').rejection_rate
  text+=f'{outcome} & {label} & {100*sub.HAC6:.1f} & {100*sub.HC3:.1f} & {100*sub.block_wild:.1f}'+chr(92)*2+'\n'
text+=r'''\bottomrule
\end{tabularx}
\tabnote{Nominal rejection rate is 5\%. Each cell uses 1,000 datasets; block-wild tests use 999 inner draws. Approximate Monte Carlo standard errors near 5\% are 0.7 percentage points. Core block-wild rejection reaches 7.1\% in one design; a bootstrap is not presumed exact.}
\end{table}

\begin{table}[htbp]
\centering\small
\caption{Illustrative power for the non-food equation under AR/GARCH errors}
\begin{tabular}{rrrr}
\toprule
True delayed sum&HAC(6) rejection (\%)&HC3 rejection (\%)&Block-wild rejection (\%)\\
\midrule
'''
for effect in [.048,.1,.2]:
 sub=c[c.direction.eq('food_to_nonfood')&c.scenario.eq('ar_garch')&c.true_delayed_sum.eq(effect)].set_index('method').rejection_rate
 text+=f'{effect:.3f} & {100*sub.HAC6:.1f} & {100*sub.HC3:.1f} & {100*sub.block_wild:.1f}'+chr(92)*2+'\n'
text+=r'''\bottomrule
\end{tabular}
\tabnote{The effect is distributed equally over three delayed coefficients. These results concern a specified synthetic process, not the true unknown data-generating process. On this grid, 80\% bootstrap power is reached between sums 0.100 and 0.200; an exact minimum detectable effect is not estimated. HAC rejection also reflects its oversized null behaviour.}
\end{table}
'''
(OUT/'calibration.tex').write_text(text)

# Source-backed numbers retained for a mechanical audit of the main report.
audit={'monthly_core_Dec2024':183.15047307758473,'headline_YoY_2024Q4':4.903203138551001,
 'data_source_root':'research_data','primary_comparison':pd.read_csv(DATA/'results/primary_phillips_comparison.csv').to_dict('records'),
 'food_variance':pd.read_csv(DATA/'results/primary_food_variance_summary.csv').to_dict('records')}
(BASE/'numerical_audit.json').write_text(json.dumps(audit,indent=2))
print('Three appendix table files generated from verified CSV results.')
