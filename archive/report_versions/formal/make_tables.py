"""Generate numerical tables and audit values from the report data subset."""
from pathlib import Path
import numpy as np
import pandas as pd
import json
BASE=Path(__file__).resolve().parent;DATA=BASE/'research_data';OUT=BASE/'tables';OUT.mkdir(exist_ok=True)
BS=chr(92)*2

def table(name,caption,columns,header,rows,note,label=None):
    text='\\begin{table}[H]\n\\centering\\small\n\\caption{'+caption+'}\n'
    if label:text+='\\label{'+label+'}\n'
    text+='\\begin{tabular'+('x' if 'X' in columns else '')+'}'+('{\\linewidth}' if 'X' in columns else '')+'{'+columns+'}\n\\toprule\n'+header+BS+'\n\\midrule\n'
    for row in rows:text+=' & '.join(map(str,row))+BS+'\n'
    text+='\\bottomrule\n\\end{tabular'+('x' if 'X' in columns else '')+'}\n\\tabnote{'+note+'}\n\\end{table}\n'
    (OUT/(name+'.tex')).write_text(text)

stats=pd.read_csv(DATA/'results/phillips_descriptive_statistics.csv')
choices=[('yoy_log','full27','unemployment','Unemployment'),('yoy_log','full27','headline','Headline: YoY'),('yoy_log','full27','core_food_fuel_excluded','Core: YoY'),('qoq_saar','full27','headline','Headline: q/q SAAR'),('qoq_saar','full27','core_food_fuel_excluded','Core: q/q SAAR'),('yoy_log','exclude_three_pandemic','unemployment','Unemployment: exclusion')]
rows=[]
for f,s,v,label in choices:
 r=stats[stats.frequency.eq(f)&stats['sample'].eq(s)&stats.variable.eq(v)].iloc[0]
 rows.append([label,int(r.n),*[f'{0 if abs(r[k])<.005 else r[k]:.2f}' for k in ['mean','median','sd','skewness','excess_kurtosis']],f'{r.minimum:.2f}--{r.maximum:.2f}'])
table('descriptive','Descriptive statistics on matched quarter samples','lrrrrrrr','Series & $n$ & Mean & Median & SD & Skewness & Excess kurtosis & Min--max',rows,
'All values are percentages or percentage points except skewness and excess kurtosis. SD uses $n-1$; skewness and excess kurtosis use finite-sample bias corrections. The exclusion removes 2020Q2, 2020Q3 and 2021Q2.','tab:descriptive')

d=pd.read_csv(DATA/'results/phillips_all_specifications.csv');d=d[d.inference_sensitivity.eq('HC3')]
def rec(f,s,o,trend=False):return d[d.frequency.eq(f)&d['sample'].eq(s)&d.outcome.eq(o)&d.trend.eq(trend)].iloc[0]
c=pd.read_csv(DATA/'results/primary_phillips_comparison.csv');rows=[]
for f,flab in [('yoy_log','YoY'),('qoq_saar','q/q SAAR')]:
 for s,slab in [('full27','Full'),('exclude_three_pandemic','Exclusion')]:
  r=c[c.frequency.eq(f)&c['sample'].eq(s)].iloc[0];h=rec(f,s,'headline');core=rec(f,s,'core_food_fuel_excluded')
  rows.append([flab,slab,int(r.n),f'{r.headline_slope:.3f}',f'{r.core_slope:.3f}',f'{r.core_minus_headline_slope:.3f}',f'{h.r_squared:.3f}',f'{core.r_squared:.3f}'])
table('regressions','OLS estimates: the same unemployment observations in each comparison','llrrrrrr','Inflation & Sample & $n$ & $\\hat\\beta_H$ & $\\hat\\beta_C$ & $\\hat\\delta$ & $R_H^2$ & $R_C^2$',rows,
'$\\delta=\\beta_C-\\beta_H$. Slopes give inflation percentage points associated with one percentage point of unemployment. Nominal HC3 ranges for $\\delta$ appear in Figure~\\ref{fig:delta}; no significance stars are used.','tab:regression')

rows=[]
checks=[('Full sample','full27',False,'core_food_fuel_excluded'),('Exclude three pandemic quarters','exclude_three_pandemic',False,'core_food_fuel_excluded'),('Exclude all of 2020--2021','exclude_2020_2021',False,'core_food_fuel_excluded'),('Full sample, calendar trend','full27',True,'core_food_fuel_excluded'),('Exclude food only','full27',False,'nonfood_only'),('Core without housing','full27',False,'core_no_housing')]
for label,s,trend,o in checks:
 rows.append([label,*[f'{rec(f,s,outcome,trend).slope:.3f}' for f in ['yoy_log','qoq_saar'] for outcome in ['headline',o]]])
table('robustness','Robustness of unemployment slopes to sample and price-basket choices','Xrrrr','Check & H: YoY & C: YoY & H: q/q & C: q/q',rows,
'H denotes headline; C denotes operational core or the stated alternative. All paired comparisons use identical observations and controls. Food-only exclusion retains fuel/light.','tab:robustness')

v=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv');rows=[]
for sector in ['Combined','Urban']:
 for f,label in [('MoM_raw','Monthly'),('YoY_raw','YoY')]:
  z=v[v.sector.eq(sector)&v.frequency.eq(f)&v['sample'].eq('full_history')].set_index('component').covariance_share_percent
  rows.append([sector,label,f'{z.food_bev:.2f}',f'{z.fuel_light:.2f}',f'{z[["pan_tobacco","clothing","housing","misc"]].sum():.2f}',f'{z.aggregation_residual:.2f}'])
table('variance','Complete allocation of official headline-inflation variance (\\%)','llrrrr','Basket & Change & Food & Fuel/light & Other four groups & Residual',rows,
'Each row sums to 100\\% before rounding. Monthly changes: February 2013--December 2025, $n=155$; YoY: January 2014--December 2025, $n=144$. These are covariance allocations, not causal effects.','tab:variance')
rows=[]
for s,label in [('full_history','Full history'),('matched_2018Q2_2024Q4','April 2018--December 2024'),('exclude_imputation_exposure','Exclude imputation-exposed changes'),('pre2020','February 2013--December 2019'),('post2021','January 2022--December 2025')]:
 r=v[v.sector.eq('Combined')&v.frequency.eq('MoM_raw')&v.component.eq('food_bev')&v['sample'].eq(s)].iloc[0]
 rows.append([label,int(r.n),f'{r.covariance_share_percent:.2f}'])
table('variance_sensitivity','Combined CPI: sensitivity of the monthly food allocation','Xrr','Sample & $n$ & Food share (\\%)',rows,
'Imputation exposure removes changes using April or May 2020 in either the numerator or denominator: April--June 2020. All calculations use the official raw headline target.','tab:variancechecks')

s=pd.read_csv(DATA/'results/spillover_effect_intervals.csv');b=pd.read_csv(DATA/'results/spillover_high_precision_bootstrap.csv');rows=[]
for direction,label in [('food_to_nonfood','Non-food'),('food_to_core','Core')]:
 r=s[s.direction.eq(direction)&s.contrast.eq('delayed_sum')&s.method.eq('HC3')].iloc[0];br=b[b.direction.eq(direction)].iloc[0]
 rows.append([label,f'{r.estimate:.4f}',f'$[{r.ci_low:.4f},\\ {r.ci_high:.4f}]$',f'{br.joint_bootstrap_tail:.4f}'])
table('spillover','Monthly extension: delayed food-inflation association','lrrr','Outcome & Sum of lags 1--3 & Nominal HC3 range & Joint bootstrap tail',rows,
'$n=147$, October 2013--December 2025. The joint test concerns all three delayed coefficients, not their sum alone. Restricted-null block-wild calculation: 19,999 draws, six-month blocks.','tab:spillover')

rows=[]
for f,flab in [('yoy_log','YoY'),('qoq_saar','q/q')]:
 for sam,slab in [('full27','Full'),('exclude_three_pandemic','Exclusion')]:
  for o,olab in [('headline','Headline'),('core_food_fuel_excluded','Core')]:
   r=rec(f,sam,o);rows.append([flab,slab,olab,f'{r.intercept:.3f}',f'{r.slope:.3f}',f'{r.se:.3f}',f'$[{r.ci_low:.3f},\\ {r.ci_high:.3f}]$'])
table('regression_details','Individual regression coefficients and nominal HC3 uncertainty','lllrrrr','Inflation & Sample & Outcome & Intercept & Slope & HC3 SE & Slope range',rows,
'Nominal 95\\% t-based ranges. They are descriptive sensitivity summaries in this short, dependent sample. Full and exclusion sample sizes are 27 and 24.','tab:regdetail')

sim=pd.read_csv(DATA/'results/spillover_recursive_calibration.csv');rows=[]
for dr,lab in [('food_to_nonfood','Non-food'),('food_to_core','Core')]:
 for scenario,scenlab in [('iid_gaussian','Independent Gaussian'),('ar_garch','AR/GARCH Gaussian'),('heavy_tail_ar_garch','AR/GARCH, heavy tails')]:
  r=sim[sim.direction.eq(dr)&sim.scenario.eq(scenario)&sim.true_delayed_sum.eq(0)].set_index('method').rejection_rate
  rows.append([lab,scenlab,*[f'{100*r[k]:.1f}' for k in ['HAC6','HC3','block_wild']]])
table('calibration','Null rejection rates in recursive monthly-model simulations (\\%)','lXrrr','Outcome & Error process & HAC(6) & HC3 & Block wild',rows,
'Nominal rate: 5\\%. Each cell uses 1,000 datasets; bootstrap tests use 999 inner draws. The Monte Carlo SE near 5\\% is about 0.7 percentage points.','tab:calibration')

# Transparent calculation register for the prose and verification script.
y=pd.read_csv(DATA/'data/processed/phillips_yoy_log_matched.csv');u=y.unemployment;h=y.headline
moments={}
for f in ['yoy_log','qoq_saar']:
 x=pd.read_csv(DATA/f'data/processed/phillips_{f}_matched.csv')
 for label,xx in [('full',x),('exclusion',x[~x.quarter.isin(['2020Q2','2020Q3','2021Q2'])])]:
  moments[f+'_'+label]=xx[['unemployment','headline','core_food_fuel_excluded']].corr().to_dict()
reg={'unemployment_sum':float(u.sum()),'unemployment_mean':float(u.mean()),'unemployment_median':float(u.median()),'Sxx':float(((u-u.mean())**2).sum()),'Sxy_headline':float(((u-u.mean())*(h-h.mean())).sum()),'correlations':moments}
(BASE/'numerical_audit.json').write_text(json.dumps(reg,indent=2))
print('Eight numerical table files and calculation register generated.')
