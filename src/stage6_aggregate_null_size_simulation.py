"""Synthetic null-size diagnostics for the 27-quarter aggregate UR design.

The regressors are the observed PLFS unemployment values. Inflation outcomes are
synthetic and independent of unemployment. This tests nominal rejection rates of
simple slope procedures under several stylised error processes; it does not
estimate the Phillips curve, identify the real DGP, or guarantee size in the data.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

EXCLUDED = {"2020Q2", "2020Q3", "2021Q2"}

def ols_stats(y, x, times, hac_lag=None, hc3=False):
    n=len(y); X=np.column_stack([np.ones(n),x]); bread=np.linalg.inv(X.T@X)
    b=bread@(X.T@y); e=y-X@b; h=np.sum((X@bread)*X,axis=1)
    if hc3:
        adj=e/np.maximum(1-h,1e-12)
        meat=X.T@((adj**2)[:,None]*X)
    elif hac_lag is None:
        # Conventional homoskedastic OLS covariance, not HC0.
        s2=float(e@e)/(n-2)
        cov=s2*bread
        se=np.sqrt(max(cov[1,1],0))
        stat=b[1]/se if se>0 else np.nan
        p=2*student_t.sf(abs(stat),df=n-2) if np.isfinite(stat) else np.nan
        return float(b[1]),float(se),float(p)
    else:
        score=X*e[:,None]
        meat=score.T@score
        # Use calendar quarter distance, not compressed row distance.
        time_to_pos={int(t):i for i,t in enumerate(times)}
        for lag in range(1,hac_lag+1):
            left=[]; right=[]
            for i,t in enumerate(times):
                j=time_to_pos.get(int(t)+lag)
                if j is not None:
                    left.append(i); right.append(j)
            if left:
                cross=score[np.asarray(left)].T @ score[np.asarray(right)]
                meat += (1-lag/(hac_lag+1))*(cross+cross.T)
        meat *= n/(n-2)
    cov=bread@meat@bread
    se=np.sqrt(max(cov[1,1],0))
    stat=b[1]/se if se>0 else np.nan
    p=2*student_t.sf(abs(stat),df=n-2) if np.isfinite(stat) else np.nan
    return float(b[1]),float(se),float(p)

def make_process(name, n, rng):
    if name=='iid_qoq': return rng.normal(size=n)
    if name=='yoy_ma3':
        e=rng.normal(size=n+3)
        return np.array([e[i:i+4].sum() for i in range(n)])
    if name=='yoy_ma3_ar05':
        e=rng.normal(size=n+3); v=np.zeros(n+3)
        for i in range(1,n+3): v[i]=0.5*v[i-1]+e[i]
        return np.array([v[i:i+4].sum() for i in range(n)])
    if name=='random_walk': return np.cumsum(rng.normal(size=n))
    raise ValueError(name)

def run(input_csv, reps=2000, seed=45520261118):
    df=pd.read_csv(input_csv); xall=df['ur_cws_15plus_person_pct'].astype(float).to_numpy()
    qids=df['quarter_id'].astype(str).to_numpy(); times=np.arange(len(df))
    processes=['iid_qoq','yoy_ma3','yoy_ma3_ar05','random_walk']
    outputs=[]; rng=np.random.default_rng(seed)
    for sample_name,mask in [('full27',np.ones(len(df),dtype=bool)),('drop_2020Q2_2020Q3_2021Q2',~np.isin(qids,list(EXCLUDED)))]:
        x=xall[mask]; tm=times[mask]; n=len(x)
        for proc in processes:
            reject={m:0 for m in ['OLS_iid','HC3','HAC3','HAC4']}; valid={m:0 for m in reject}
            for r in range(reps):
                y=make_process(proc,len(df),rng)[mask]
                for name,kw in [('OLS_iid',{'hac_lag':None,'hc3':False}),('HC3',{'hc3':True}),('HAC3',{'hac_lag':3}),('HAC4',{'hac_lag':4})]:
                    _,_,p=ols_stats(y,x,tm,**kw)
                    if np.isfinite(p):
                        valid[name]+=1
                        if p<0.05: reject[name]+=1
            for method in reject:
                rate=reject[method]/valid[method] if valid[method] else np.nan
                outputs.append({'sample':sample_name,'n':n,'process':proc,'method':method,
                  'replications':valid[method],'rejection_rate':rate,'monte_carlo_se':(rate*(1-rate)/valid[method])**0.5,
                  'nominal_size':0.05,'seed':seed})
    return pd.DataFrame(outputs)

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',default='data/raw/plfs_urban_quarterly_ur_2018_2024.csv')
    p.add_argument('--reps',type=int,default=2000); p.add_argument('--seed',type=int,default=45520261118)
    p.add_argument('--output',default='outputs/tables/stage6_aggregate_null_size_simulation.csv')
    a=p.parse_args(); out=run(a.input,a.reps,a.seed); Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,index=False)
    print(out.to_string(index=False)); print('\nSynthetic null calibration only; no actual inflation outcomes used.')
if __name__=='__main__': main()
