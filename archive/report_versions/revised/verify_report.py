"""Verify numerical evidence, required structure and portable report build."""
from pathlib import Path
import json,re
import numpy as np
import pandas as pd
from scipy.stats import t
from pypdf import PdfReader
BASE=Path(__file__).resolve().parent;DATA=BASE/'research_data'
tex=(BASE/'report.tex').read_text();main=tex.split('% MAIN_TEXT_START')[1].split('% MAIN_TEXT_END')[0]
checks=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
def close(name,a,b):check(name,bool(np.allclose(a,b,atol=1e-9,rtol=1e-9)))
def words(s):return re.findall(r"\b(?:\d+(?:[.,]\d+)*|[A-Za-z]+(?:[’'-][A-Za-z]+)*)\b",s)
expected=['Background and motivation','Research questions and hypotheses','Data and methodology','Discussion of results','Conclusion and policy implications']
check('Exactly five required main sections, in order',re.findall(r'\\section\{([^}]+)\}',main)==expected)
check('Cover/body use the supplied 10pt A4 class','documentclass[10pt,a4paper]' in tex)
check('Supplied cover margins retained','margin=0.75in,top=0.65in,bottom=0.65in' in tex)
check('Supplied cover title/logo proportions retained','fontsize{20}{26}' in tex and 'width=0.44\\textwidth' in tex)
expanded=re.sub(r'\\input\{([^}]+)\}',lambda m:(BASE/(m[1]+'.tex')).read_text(),main)

stats=pd.read_csv(DATA/'results/phillips_descriptive_statistics.csv')
for freq in ['yoy_log','qoq_saar']:
 d=pd.read_csv(DATA/f'data/processed/phillips_{freq}_matched.csv')
 for sample,dd in [('full27',d),('exclude_three_pandemic',d[~d.quarter.isin(['2020Q2','2020Q3','2021Q2'])])]:
  for col in ['unemployment','headline','core_food_fuel_excluded']:
   x=dd[col];saved=stats[stats.frequency.eq(freq)&stats['sample'].eq(sample)&stats.variable.eq(col)].iloc[0]
   actual=[len(x),x.mean(),x.median(),x.std(),x.min(),x.max(),x.skew(),x.kurt()]
   wanted=saved[['n','mean','median','sd','minimum','maximum','skewness','excess_kurtosis']].to_numpy(dtype=float)
   close(f'{freq}/{sample}/{col}: all eight descriptive statistics',actual,wanted)
 # Check full/exclusion plotted correlations and their link to OLS below.
 check(freq+' contains complete matched quarters',len(d)==27 and d.quarter.nunique()==27)

comparison=pd.read_csv(DATA/'results/primary_phillips_comparison.csv')
allreg=pd.read_csv(DATA/'results/phillips_all_specifications.csv')
allreg=allreg[allreg.inference_sensitivity.eq('HC3')&~allreg.trend]
for r in comparison.itertuples():
 d=pd.read_csv(DATA/f'data/processed/phillips_{r.frequency}_matched.csv')
 if r.sample!='full27':d=d[~d.quarter.isin(['2020Q2','2020Q3','2021Q2'])]
 check(f'{r.frequency}/{r.sample}: regression sample',len(d)==r.n)
 X=np.column_stack([np.ones(len(d)),d.unemployment]);inv=np.linalg.inv(X.T@X)
 fit=lambda y:np.linalg.lstsq(X,y,rcond=None)[0]
 bh=fit(d.headline);bc=fit(d.core_food_fuel_excluded);diff=d.core_food_fuel_excluded-d.headline;bd=fit(diff)
 close(f'{r.frequency}/{r.sample}: paired slopes',[bh[1],bc[1],bd[1]],[r.headline_slope,r.core_slope,r.core_minus_headline_slope])
 close(f'{r.frequency}/{r.sample}: difference identity',bc[1]-bh[1],bd[1])
 e=diff-X@bd;h=np.sum((X@inv)*X,axis=1)
 V=inv@(X.T@(((e/(1-h))**2).to_numpy()[:,None]*X))@inv
 rad=t.ppf(.975,len(d)-2)*np.sqrt(V[1,1])
 close(f'{r.frequency}/{r.sample}: plotted nominal HC3 interval',[bd[1]-rad,bd[1]+rad],[r.nominal_HC3_difference_low,r.nominal_HC3_difference_high])
 for outcome,b in [('headline',bh),('core_food_fuel_excluded',bc)]:
  y=d[outcome];corr=d.unemployment.corr(y);r2=1-np.sum((y-X@b)**2)/np.sum((y-y.mean())**2)
  saved=allreg[allreg.frequency.eq(r.frequency)&allreg['sample'].eq(r.sample)&allreg.outcome.eq(outcome)].iloc[0]
  close(f'{r.frequency}/{r.sample}/{outcome}: intercept, R2, correlation',[b[0],r2,corr],[saved.intercept,saved.r_squared,saved.correlation])
  close(f'{r.frequency}/{r.sample}/{outcome}: beta-correlation identity',b[1],corr*y.std()/d.unemployment.std())
  check(f'{r.frequency}/{r.sample}/{outcome}: slope and fit in main table',f'{b[1]:.3f}' in expanded and f'{r2:.3f}' in expanded)

loo=pd.read_csv(DATA/'results/phillips_leave_one_quarter_out.csv');loo=loo[loo['sample'].eq('full27')]
for f in ['yoy_log','qoq_saar']:
 d=pd.read_csv(DATA/f'data/processed/phillips_{f}_matched.csv').set_index('quarter')
 for outcome in ['headline','core_food_fuel_excluded']:
  rows=loo[loo.frequency.eq(f)&loo.outcome.eq(outcome)]
  vals=[]
  for r in rows.itertuples():
   x=d.drop(index=r.omitted_quarter);vals.append(np.polyfit(x.unemployment,x[outcome],1)[0])
  close(f'{f}/{outcome}: all 27 plotted leave-one-out fits',vals,rows.slope)
  if outcome=='core_food_fuel_excluded':check(f'{f}: all leave-one-out core slopes positive',min(vals)>0)
check('Leave-one-out plot fixes its base sample explicitly',"loo=loo[loo['sample'].eq('full27')]" in (BASE/'make_figures.py').read_text())

y=pd.read_csv(DATA/'data/processed/phillips_yoy_log_matched.csv').set_index('quarter');u=y.unemployment
close('Worked unemployment sum',u.sum(),239.7)
close('Worked centred sum of squares',np.sum((u-u.mean())**2),231.56666666666672)
close('Worked headline cross product',np.sum((u-u.mean())*(y.headline-y.headline.mean())),21.844330288689505)
close('Worked median',u.median(),8.3)
check('PLFS bulletin correction 2019Q2',u.loc['2019Q2']==8.8)
check('PLFS bulletin correction 2019Q3',u.loc['2019Q3']==8.3)
ss=(u-u.mean())**2
check('Pandemic leverage percentages printed',f'{100*ss.loc["2020Q2"]/ss.sum():.2f}' in main and f'{100*ss.loc[["2020Q2","2020Q3","2021Q2"]].sum()/ss.sum():.2f}' in main)
levels=pd.read_csv(DATA/'data/processed/urban_cpi_levels.csv',index_col='month')
core=levels.loc['2024-12',['pan_tobacco','clothing','housing','misc']].to_numpy()@np.array([1.36,5.57,21.67,29.53])/58.13
check('Worked core level printed',f'{core:.4f}' in main)
levels.index=pd.to_datetime(levels.index);q=levels.headline.resample('QE').mean()
check('Worked quarterly inflation printed',f'{100*np.log(q.loc["2024-12-31"]/q.loc["2023-12-31"]):.4f}' in main)

v=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv')
for sector in ['Combined','Urban']:
 for freq in ['MoM_raw','YoY_raw']:
  d=pd.read_csv(DATA/f'data/processed/{sector.lower()}_{freq}_exact_contributions.csv').drop(columns='month')
  headline=d.sum(axis=1);shares=100*d.apply(lambda c:c.cov(headline))/headline.var()
  saved=v[v.sector.eq(sector)&v.frequency.eq(freq)&v['sample'].eq('full_history')].set_index('component')
  close(f'{sector}/{freq}: every component variance allocation',shares.loc[saved.index],saved.covariance_share_percent)
  close(f'{sector}/{freq}: allocations sum exactly to 100',shares.sum(),100)
  check(f'{sector}/{freq}: primary food share printed',f'{shares.food_bev:.2f}' in expanded)
  close(f'{sector}/{freq}: official variance',headline.var(),saved.official_headline_variance.iloc[0])
food=v[v.sector.eq('Combined')&v.frequency.eq('MoM_raw')&v.component.eq('food_bev')]
for r in food.itertuples():check('Combined monthly sensitivity printed: '+r.sample,f'{r.covariance_share_percent:.2f}' in expanded)
check('Imputation exclusion rounds consistently to 88.61','gives 88.61\\%' in main)

spill=pd.read_csv(DATA/'results/spillover_effect_intervals.csv')
for r in spill[spill.contrast.eq('delayed_sum')&spill.method.eq('HC3')].itertuples():
 check(r.direction+': estimate and interval in main table',all(f'{n:.4f}' in expanded for n in [r.estimate,r.ci_low,r.ci_high]))
for r in pd.read_csv(DATA/'results/spillover_high_precision_bootstrap.csv').itertuples():check(r.direction+': joint bootstrap tail printed',f'{r.joint_bootstrap_tail:.4f}' in expanded)

# Transparent text count: body, headings, captions, source lines and table text.
# Formula expressions and axis labels are not counted as running text.
counttext=expanded
counttext=re.sub(r'\\fig\{[^}]*\}\{([^}]*)\}\{[^}]*\}\{([^}]*)\}',lambda m:m[1]+' '+m[2],counttext)
counttext=re.sub(r'\\begin\{tabularx\}\{\\linewidth\}\{[^}]*\}', '',counttext)
counttext=re.sub(r'\\begin\{tabular\}\{[^}]*\}', '',counttext)
counttext=re.sub(r'\\begin\{equation\}.*?\\end\{equation\}','',counttext,flags=re.S)
counttext=re.sub(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}','',counttext)
counttext=re.sub(r'\\(?:cite|label|ref|eqref|begin|end)\*?(?:\[[^\]]*\])?\{[^}]*\}','',counttext)
counttext=re.sub(r'\$[^$]*\$','',counttext)
counttext=re.sub(r'\\[a-zA-Z]+(?:\[[^\]]*\])?',' ',counttext)
counttext=re.sub(r'[{}&~\\]',' ',counttext)
wordcount=len(words(counttext));check('Main text within 3000--4000 words',3000<=wordcount<=4000)
reader=PdfReader(BASE/'HS455_Report.pdf');texts=[p.extract_text() for p in reader.pages]
ref=next(i for i,s in enumerate(texts) if '\nReferences\n' in s)
check('Main text has 10--12 pages',10<=ref-1<=12)
check('No nearly empty main pages',min(len(s.split()) for s in texts[1:ref])>=250)
check('No unresolved references','??' not in '\n'.join(texts))
check('Requested draft labels absent',not re.search(r'AI.assisted|review draft|Student review and revision|before submission', '\n'.join(texts),re.I))
for name in ['K Harshavardhan','2023MCB1216','Pasula Kohith','2023EEB1232','Smruti Ranjan Behera','Samaresh Bardhan','Bhavesh Garg']:check('Cover: '+name,name in texts[0])
log=(BASE/'report.log').read_text();check('No overflowing boxes or unresolved citations',not re.search(r'Overfull|undefined references|Citation .* undefined',log))
figures=re.findall(r'\\fig\{([^}]+)\}',tex);check('Ten vector figures embedded',len(figures)==10 and all((BASE/'assets'/f).is_file() for f in figures))
check('Nine main/appendix tables',tex.count('\\begin{table}')+sum((BASE/(p+'.tex')).read_text().count('\\begin{table}') for p in re.findall(r'\\input\{([^}]+)\}',tex))==9)
for path in re.findall(r'\\input\{([^}]+)\}',tex):check('Portable table: '+path,(BASE/(path+'.tex')).exists())
result={'status':'PASS','checks_passed':len(checks),'main_text_words':wordcount,
'word_count_scope':'Main narrative, headings, captions, source lines and table text, with each decimal number counted as one token; excludes equations, inline mathematics, plot-axis labels, references and appendices.',
'main_pages':ref-1,'total_pdf_pages':len(texts),'main_pdf_pages':[2,ref],
'references_pdf_page':ref+1,'appendix_pdf_pages':[ref+2,len(texts)],
'figures':10,'plot_panels':18,'tables':9,'checks':checks}
(BASE/'report_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
