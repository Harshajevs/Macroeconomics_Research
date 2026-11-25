"""Recompute every historical model's point estimates and add HC3 intervals."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'src'))
import estimate_baseline as m

def main():
    historical=pd.read_csv(ROOT.parent/'outputs/model_results/postreview_model_comparison_summary.csv');rows=[]
    for _,s in historical.iterrows():
        name=s.label;q,p=int(s.q),int(s.p);mask=None;controls=True
        if 'covid_exclusion_mar2020_dec2021' in name:mask=pd.period_range('2020-03','2021-12',freq='M');controls=False
        elif 'covid_exclusion_mar2020_dec2020' in name:mask=pd.period_range('2020-03','2020-12',freq='M');controls=False
        elif 'imputed_aprmay2020_exclusion' in name:mask=pd.period_range('2020-04','2020-05',freq='M')
        stl=('stl' in name)
        if stl:controls=False
        y,X=m.design(q=q,p=p,start=s.sample_start,direction=s.direction,mask_months=mask,include_covid_controls=controls,stl=stl,covid_lag_horizon=max(q,3))
        fit=m.fit_model(y,X);names=list(X.columns);w=np.array([float(k in [f'x_l{i}' for i in range(1,min(q,3)+1)]) for k in names])
        theta=float(w@fit.params)
        assert len(y)==int(s.n),(name,'n')
        assert np.isclose(theta,s.primary_comparable_delayed_sum,atol=1e-9),(name,theta,s.primary_comparable_delayed_sum)
        se=np.sqrt(w@fit.get_robustcov_results(cov_type='HC3').cov_params()@w);crit=t.ppf(.975,fit.df_resid)
        rows.append(dict(label=name,direction=s.direction,n=len(y),p=p,q=q,reproduced_delayed_sum=theta,historical_delayed_sum=s.primary_comparable_delayed_sum,HC3_se=se,HC3_ci_low=theta-crit*se,HC3_ci_high=theta+crit*se,covariance_gap_note='Historical HAC/bootstrap uses compressed outcome rows across removed months; not promoted to calibrated inference' if mask is not None else 'Continuous monthly sample'))
    pd.DataFrame(rows).to_csv(ROOT/'results/all_legacy_variants_reproduced_HC3.csv',index=False)
    print(f'All {len(rows)} historical delayed sums and sample sizes reproduced; HC3 intervals added without altering legacy outputs.')

if __name__=='__main__':main()
