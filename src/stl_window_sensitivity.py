"""STL seasonal smoother-window sensitivity for raw CPI log levels."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'processed'/'inflation_dataset.csv'
OUT=ROOT/'outputs'/'tables'
OUT.mkdir(parents=True,exist_ok=True)
D=pd.read_csv(DATA)
D['date']=pd.PeriodIndex(D.date,freq='M')
D=D.set_index('date')

SPEC=[
    ('robust_s7_baseline',7,True,'Robust STL; seasonal window 7 (baseline)'),
    ('robust_s13',13,True,'Robust STL; seasonal window 13'),
    ('robust_s25',25,True,'Robust STL; seasonal window 25'),
    ('near_periodic_s99_approx',99,True,'Near-periodic finite-window approximation; robust seasonal window 99'),
    ('nonrobust_s7',7,False,'Non-robust STL; seasonal window 7'),
]


def main():
    rows=[]
    for label,window,robust,note in SPEC:
        for series,col in [('Food and Beverages','food'),('Non-food','nonfood')]:
            level=pd.to_numeric(D[col],errors='coerce').astype(float)
            if level.isna().any() or (level<=0).any():
                raise ValueError(f'Invalid CPI level in {col}')
            fit=STL(np.log(level),period=12,seasonal=window,robust=robust).fit()
            sa=np.log(level)-fit.seasonal
            mom=100*sa.diff().dropna()
            rows.append({
                'specification':label,'seasonal_window':window,'robust':robust,
                'series':series,'n':int(mom.size),'mean':float(mom.mean()),
                'variance':float(mom.var(ddof=1)),'sd':float(mom.std(ddof=1)),
                'skewness':float(stats.skew(mom,bias=False)),
                'excess_kurtosis':float(stats.kurtosis(mom,fisher=True,bias=False)),
                'acf1':float(mom.autocorr(1)),'method_note':note,
                'inference_note':'Descriptive sensitivity only; no iid inference.'
            })
    result=pd.DataFrame(rows)
    baseline=result[result.specification=='robust_s7_baseline'][['series','sd']].rename(columns={'sd':'baseline_s7_sd'})
    result=result.merge(baseline,on='series',how='left')
    result['sd_difference_vs_robust_s7']=result.sd-result.baseline_s7_sd
    result['sd_ratio_vs_robust_s7']=result.sd/result.baseline_s7_sd
    result.to_csv(OUT/'stl_seasonal_window_sensitivity.csv',index=False,float_format='%.8f')
    print(result[['specification','series','n','sd','sd_difference_vs_robust_s7','sd_ratio_vs_robust_s7']].to_string(index=False))

if __name__=='__main__': main()
