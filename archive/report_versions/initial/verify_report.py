"""Check report numbers, source completeness, length and compiled-PDF structure."""
from pathlib import Path
import json,re
import numpy as np
import pandas as pd
from scipy.stats import t
from pypdf import PdfReader
BASE=Path(__file__).resolve().parent
DATA=BASE/'research_data'
tex=(BASE/'report.tex').read_text()
main=tex.split('% MAIN_TEXT_START')[1].split('% MAIN_TEXT_END')[0]
checks=[]
def check(label,condition):
    if not condition: raise AssertionError(label)
    checks.append(label)
def close(label,a,b,atol=1e-9):
    check(label,bool(np.allclose(a,b,atol=atol,rtol=1e-9)))

# Refit identical-row regressions, including the HC3 interval of the difference.
comp=pd.read_csv(DATA/'results/primary_phillips_comparison.csv')
for row in comp.itertuples():
    d=pd.read_csv(DATA/f'data/processed/phillips_{row.frequency}_matched.csv')
    if row.sample=='exclude_three_pandemic':
        d=d[~d.quarter.isin(['2020Q2','2020Q3','2021Q2'])]
    check(f'{row.frequency}/{row.sample} row count',len(d)==row.n)
    X=np.column_stack([np.ones(len(d)),d.unemployment]);inv=np.linalg.inv(X.T@X)
    fit=lambda y: np.linalg.lstsq(X,y,rcond=None)[0]
    bh=fit(d.headline.to_numpy());bc=fit(d.core_food_fuel_excluded.to_numpy())
    bd=fit((d.core_food_fuel_excluded-d.headline).to_numpy())
    close(f'{row.frequency}/{row.sample} slopes',[bh[1],bc[1],bd[1]],
        [row.headline_slope,row.core_slope,row.core_minus_headline_slope])
    y=(d.core_food_fuel_excluded-d.headline).to_numpy()
    h=np.sum((X@inv)*X,axis=1);e=y-X@bd
    V=inv@(X.T@(((e/(1-h))**2)[:,None]*X))@inv
    radius=t.ppf(.975,len(d)-2)*np.sqrt(V[1,1])
    close(f'{row.frequency}/{row.sample} HC3 interval',[bd[1]-radius,bd[1]+radius],
        [row.nominal_HC3_difference_low,row.nominal_HC3_difference_high])
    # Verify that the complete formatted row exists in the submitted TeX.
    clean=main.replace('$','')
    numbers=[row.headline_slope,row.core_slope,row.core_minus_headline_slope]
    check(f'{row.frequency}/{row.sample} report slopes',all(f'{n:.3f}' in clean for n in numbers))
    check(f'{row.frequency}/{row.sample} report interval',
        f'{row.nominal_HC3_difference_low:.3f}' in clean and f'{row.nominal_HC3_difference_high:.3f}' in clean)

cpi=pd.read_csv(DATA/'data/processed/urban_cpi_levels.csv',index_col='month')
core=cpi.loc['2024-12',['pan_tobacco','clothing','housing','misc']].to_numpy()@np.array([1.36,5.57,21.67,29.53])/58.13
close('Worked core index',core,183.15047307758473)
check('Worked core index printed',f'{core:.4f}' in main)
cpi.index=pd.to_datetime(cpi.index)
quarterly=cpi.headline.resample('QE').mean()
yoy=100*np.log(quarterly.loc['2024-12-31']/quarterly.loc['2023-12-31'])
check('Worked quarterly annual inflation printed',f'{yoy:.4f}' in main)

variance=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv')
for sector in ['Combined','Urban']:
    for frequency in ['MoM_raw','YoY_raw']:
        d=pd.read_csv(DATA/f'data/processed/{sector.lower()}_{frequency}_exact_contributions.csv').drop(columns='month')
        headline=d.sum(axis=1)
        shares=100*d.apply(lambda c: c.cov(headline))/headline.var()
        saved=variance[variance.sector.eq(sector)&variance.frequency.eq(frequency)&variance['sample'].eq('full_history')].set_index('component')
        close(f'{sector}/{frequency} complete accounting',shares.sum(),100)
        close(f'{sector}/{frequency} allocation recalculation',shares.loc[saved.index],saved.covariance_share_percent)
        check(f'{sector}/{frequency} food share printed',f'{shares.food_bev:.2f}' in main)
        close(f'{sector}/{frequency} official variance',headline.var(),saved.official_headline_variance.iloc[0])

spill=pd.read_csv(DATA/'results/spillover_effect_intervals.csv')
for r in spill[spill.contrast.eq('delayed_sum')&spill.method.eq('HC3')].itertuples():
    check(f'{r.direction} estimate/interval printed',all(f'{v:.4f}' in main for v in [r.estimate,r.ci_low,r.ci_high]))
for r in pd.read_csv(DATA/'results/spillover_high_precision_bootstrap.csv').itertuples():
    check(f'{r.direction} joint bootstrap printed',f'{r.joint_bootstrap_tail:.4f}' in main)

# Strict count: paragraph prose only, with every mathematical expression and
# entire figure/table environment removed. This is a conservative lower bound.
prose=main
for env in ['figure','table','equation']:
    prose=re.sub(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}', '', prose,flags=re.S)
prose=re.sub(r'\\(?:sub)?section\*?\{[^}]*\}','',prose)
prose=re.sub(r'\\(?:cite|label|ref|eqref)\{[^}]*\}','',prose)
prose=re.sub(r'\$[^$]*\$','',prose)
prose=re.sub(r'\\[%&]','',prose)
prose=re.sub(r'\\[a-zA-Z]+(?:\[[^\]]*\])?',' ',prose)
prose=re.sub(r'[{}~]',' ',prose)
prose_words=len(re.findall(r"\b\w+(?:[’'-]\w+)*\b",prose))
check('Main paragraph prose between 3000 and 4000 words',3000<=prose_words<=4000)
reader=PdfReader(BASE/'HS455_Report_Review_Draft.pdf')
texts=[p.extract_text() for p in reader.pages]
refpage=next(i for i,s in enumerate(texts) if '\nReferences\n' in s)
main_pages=refpage-1
check('Main text has 10--12 pages',10<=main_pages<=12)
# Inclusive upper bound counts even running heads, chart labels and mathematics.
pdf_tokens=sum(len(s.split()) for s in texts[1:refpage])
check('Even inclusive main-PDF token count below 4000',pdf_tokens<4000)
for text in ['K Harshavardhan','2023MCB1216','Pasula Kohith','2023EEB1232','Smruti Ranjan Behera','Samaresh Bardhan','Bhavesh Garg']:
    check('Cover detail: '+text,text in texts[0])
check('No unresolved cross-references','??' not in '\n'.join(texts))
log=(BASE/'report.log').read_text()
check('No LaTeX box overflow / undefined references',not re.search(r'Overfull|Undefined|undefined references|Citation .* undefined',log))
for path in re.findall(r'\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',tex):
    candidates=[BASE/path,BASE/(path+'.tex'),BASE/'assets'/path]
    check('Portable dependency: '+path,any(p.exists() for p in candidates))
result={'status':'PASS','checks_passed':len(checks),'paragraph_prose_words':prose_words,
    'inclusive_main_pdf_tokens':pdf_tokens,'main_pages':main_pages,'total_pdf_pages':len(texts),
    'cover_pdf_page':1,'main_pdf_pages':[2,refpage], 'references_pdf_page':refpage+1,
    'appendix_pdf_pages':[refpage+2,len(texts)],'checks':checks,
    'word_count_note':'Paragraph count excludes captions, tables, headings, display and inline math. Inclusive token count includes all main-page content, running heads and page numbers.'}
(BASE/'report_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
