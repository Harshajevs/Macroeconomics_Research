"""Reproduce the secondary extension and strengthen its uncertainty disclosures."""
from pathlib import Path
import sys,json,hashlib,argparse,time
import numpy as np
import pandas as pd
from scipy.stats import chi2,t,norm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'src'))
import estimate_baseline as m
from fast_bootstrap import Design

def wilson(k,n):
    z=norm.ppf(.975);p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-half,center+half

def refresh():
    rows=[];contrasts=[]
    for direction in ['food_to_nonfood','food_to_core']:
        y,X=m.design(q=3,p=1,start='2013-10',direction=direction);res=m.fit_model(y,X)
        terms=['x_l1','x_l2','x_l3'];names=list(X.columns);R=m.restriction_matrix(names,terms)
        seed=45521000+int(hashlib.sha256(direction.encode()).hexdigest()[:6],16)
        engine=Design(X,R);stat=engine.statistics(y)[0][0]
        boot=engine.bootstrap(y,[names.index(k) for k in terms],19999,seed)
        x0R=m.restriction_matrix(names,['x0']);x0engine=Design(X,x0R)
        contemp=x0engine.bootstrap(y,[names.index('x0')],49999,seed+1)
        rows.append(dict(direction=direction,n=len(y),p=1,q=3,joint_stat=stat,joint_reps=19999,joint_seed=seed,joint_bootstrap_tail=boot,joint_mcse=np.sqrt(boot*(1-boot)/20000),contemporaneous_coefficient=res.params['x0'],contemporaneous_reps=49999,contemporaneous_seed=seed+1,contemporaneous_bootstrap_tail=contemp,contemporaneous_mcse=np.sqrt(contemp*(1-contemp)/50000)))
        for label,tt in [('delayed_sum',terms),('current_plus_lags',['x0',*terms])]:
            w=np.array([float(k in tt) for k in names]);theta=float(w@res.params)
            for kind,kw in [('HC3',dict(cov_type='HC3')),('HAC6',dict(cov_type='HAC',maxlags=6,use_correction=True))]:
                cov=res.get_robustcov_results(**kw).cov_params();se=np.sqrt(w@cov@w);crit=t.ppf(.975,res.df_resid)
                contrasts.append(dict(direction=direction,contrast=label,method=kind,n=len(y),estimate=theta,se=se,ci_low=theta-crit*se,ci_high=theta+crit*se))
    pd.DataFrame(rows).to_csv(ROOT/'results/spillover_high_precision_bootstrap.csv',index=False)
    pd.DataFrame(contrasts).to_csv(ROOT/'results/spillover_effect_intervals.csv',index=False)
    print('Updated secondary forward results',pd.DataFrame(rows).to_string(index=False),flush=True)
    refresh_reverse()

def refresh_reverse():
    # Reverse remains exploratory; add the audit-suggested lagged relative price
    # as a post-results sensitivity, without calling it an identified ECM.
    rows=[]
    for ecm in [False,True]:
        # p=0 is the historical STL reverse model's selected order. Match it
        # so adding the relative-price term is the sole specification change.
        y,X=m.design(q=3,p=0,start='2014-01',direction='nonfood_to_food',stl=True)
        if ecm:
            relative=100*np.log(m.D.food/m.D.nonfood).shift(1)
            X['lagged_log_food_nonfood_relative_price']=relative.reindex(X.index)
        r=m.fit_model(y,X);terms=['x_l1','x_l2','x_l3'];R=m.restriction_matrix(list(X.columns),terms)
        engine=Design(X,R);seed=45522000+int(ecm)
        tail=engine.bootstrap(y,[list(X.columns).index(k) for k in terms],49999,seed)
        rows.append(dict(relative_price_added=ecm,own_lag_p=0,n=len(y),joint_block_bootstrap_tail=tail,reps=49999,seed=seed,relative_price_coefficient=r.params.get('lagged_log_food_nonfood_relative_price',np.nan),relative_price_scale='100 ln(raw food/nonfood), lag1; coefficient in monthly-inflation pp per relative-price log percentage point',interpretation='Exploratory post-results STL reverse sensitivity; predictive association, not causal transmission or proof of cointegration'))
    pd.DataFrame(rows).to_csv(ROOT/'results/reverse_relative_price_sensitivity.csv',index=False)

def errors(rng,n,scenario,scale):
    burn=250;N=n+burn;z=rng.normal(size=N) if scenario=='iid_gaussian' else rng.standard_t(4,size=N)/np.sqrt(2) if scenario=='heavy_tail_ar_garch' else rng.normal(size=N)
    eps=np.zeros(N);v=np.ones(N);a=np.zeros(N)
    for j in range(1,N):
        v[j]=.07+.07*eps[j-1]**2+.86*v[j-1] if scenario!='iid_gaussian' else 1.
        eps[j]=np.sqrt(v[j])*z[j]
        a[j]=(.3*a[j-1] if scenario!='iid_gaussian' else 0)+eps[j]
    return scale*a[burn:]

def calibrate(reps=1000,inner=999):
    rows=[];base_seed=45520261122
    for direction in ['food_to_nonfood','food_to_core']:
        y,baseX=m.design(q=3,p=1,start='2013-10',direction=direction);fit=m.fit_model(y,baseX)
        names=list(baseX.columns);terms=['x_l1','x_l2','x_l3'];R=m.restriction_matrix(names,terms);tested=[names.index(k) for k in terms]
        ylag=names.index('y_l1');beta=fit.params.to_numpy().copy();beta[tested]=0
        scale=np.std(fit.resid,ddof=int(len(beta)))
        scenarios=[('iid_gaussian',0.),('ar_garch',0.),('heavy_tail_ar_garch',0.)]
        if direction=='food_to_nonfood':scenarios += [('ar_garch',.048),('ar_garch',.1),('ar_garch',.2),('ar_garch',.4)]
        for scenario,effect in scenarios:
            scenario_seed=base_seed+int(hashlib.sha256((direction+scenario+str(effect)).encode()).hexdigest()[:6],16)
            rng=np.random.default_rng(scenario_seed);counts=dict(HAC6=0,HC3=0,block_wild=0);coverage=dict(HAC6=0,HC3=0)
            for rep in range(reps):
                xx=baseX.to_numpy().copy();b=beta.copy();b[ylag]=.5 if scenario=='heavy_tail_ar_garch' else .3;b[tested]=effect/3
                noise=errors(rng,len(y),scenario,scale);yy=np.empty(len(y));previous=float(baseX.iloc[0,ylag])
                for j in range(len(y)):
                    xx[j,ylag]=previous;yy[j]=xx[j]@b+noise[j];previous=yy[j]
                engine=Design(xx,R)
                for method,kind in [('HAC6','HAC'),('HC3','HC3')]:
                    stat,bhat,cov=engine.statistics(yy,kind)
                    counts[method]+=int(chi2.sf(stat[0],3)<.05)
                    # The sum of the three tested coefficients: coverage and power
                    # differ from the joint restriction test.
                    theta=float((R@bhat).sum());se=np.sqrt(cov[0].sum());crit=t.ppf(.975,len(y)-len(b))
                    coverage[method]+=int(theta-crit*se<=effect<=theta+crit*se)
                bootseed=int(rng.integers(1,2**32-1));tail=engine.bootstrap(yy,tested,inner,bootseed,legacy_rng=False)
                counts['block_wild']+=int(tail<.05)
                if (rep+1)%250==0:print(direction,scenario,effect,rep+1,'/',reps,flush=True)
            for method,k in counts.items():
                lo,hi=wilson(k,reps);rate=k/reps
                rows.append(dict(direction=direction,scenario=scenario,true_delayed_sum=effect,method=method,replications=reps,inner_bootstrap=inner if method=='block_wild' else 0,rejection_rate=rate,monte_carlo_se=np.sqrt(rate*(1-rate)/reps),wilson_low=lo,wilson_high=hi,contrast_95_interval_coverage=coverage.get(method,np.nan)/reps,scenario_seed=scenario_seed,dgp='Own lag regenerated recursively; iid Gaussian or independent AR/GARCH/heavy-tail innovations; actual food/calendar regressors retained'))
            pd.DataFrame(rows).to_csv(ROOT/'results/spillover_recursive_calibration.csv',index=False)
    print('Recursive calibration finished',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['refresh','reverse','calibrate'],default='refresh');p.add_argument('--reps',type=int,default=1000);p.add_argument('--inner',type=int,default=999);a=p.parse_args()
    if a.mode=='refresh':refresh()
    elif a.mode=='reverse':refresh_reverse()
    else:calibrate(a.reps,a.inner)
