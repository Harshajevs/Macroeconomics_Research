"""Conditional-null size experiment for HAC, HC3 and block-wild inference.

This is a design-specific calibration exercise, not a universal guarantee about
finite-sample size. It fixes the observed regressors and imposes the joint
food-lag null using the restricted fitted values and residual magnitudes.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import estimate_baseline as model

N_SIM = 120
BOOT_REPS = 199
SEED = 455202611


def signs_for(n, scheme, rng, block=6):
    if scheme == 'iid_rademacher':
        return rng.choice([-1.0, 1.0], size=n)
    if scheme == 'six_month_block_rademacher':
        out = np.ones(n)
        offset = int(rng.integers(0, block))
        for start in range(-offset, n, block):
            out[max(0,start):min(n,start+block)] = rng.choice([-1.0,1.0])
        return out
    raise ValueError(scheme)


def wilson(k, n, z=1.96):
    phat = k/n
    den = 1 + z*z/n
    center = (phat + z*z/(2*n))/den
    half = z*np.sqrt(phat*(1-phat)/n + z*z/(4*n*n))/den
    return center-half, center+half


def main():
    y, X = model.design(q=3, p=1, start='2013-10')
    terms = ['x_l1','x_l2','x_l3']
    R = model.restriction_matrix(list(X.columns), terms)
    X0 = X.drop(columns=terms)
    restricted = sm.OLS(y, X0).fit()
    fitted0 = np.asarray(restricted.fittedvalues)
    resid0 = np.asarray(restricted.resid)
    n = len(y)
    rng = np.random.default_rng(SEED)
    rows=[]
    for scheme in ('iid_rademacher','six_month_block_rademacher'):
        results={'HAC6_chi2':[],'HC3_chi2':[],'block_wild_bootstrap':[]}
        for i in range(N_SIM):
            ysim = pd.Series(fitted0 + resid0*signs_for(n,scheme,rng), index=y.index)
            fit=sm.OLS(ysim,X).fit()
            hac=fit.get_robustcov_results(cov_type='HAC',maxlags=6,use_correction=True,use_t=False)
            hc3=fit.get_robustcov_results(cov_type='HC3',use_t=False)
            hstat=float(hac.wald_test(R,use_f=False,scalar=True).statistic)
            cstat=float(hc3.wald_test(R,use_f=False,scalar=True).statistic)
            hp=float(chi2.sf(hstat,3)); cp=float(chi2.sf(cstat,3))
            bp=model.wild_block_bootstrap_wald(ysim,X,terms,hstat,reps=BOOT_REPS,
                                               block_length=6,seed=SEED+10000*i+(0 if scheme=='iid_rademacher' else 50000))
            results['HAC6_chi2'].append(hp<0.05)
            results['HC3_chi2'].append(cp<0.05)
            results['block_wild_bootstrap'].append(bp['wild_block_bootstrap_wald_tail_probability']<0.05)
        for method, rejected in results.items():
            k=int(np.sum(rejected)); lo,hi=wilson(k,N_SIM)
            rows.append({'error_scheme':scheme,'method':method,'simulations':N_SIM,
                         'bootstrap_draws_per_test':BOOT_REPS if method=='block_wild_bootstrap' else 0,
                         'nominal_size':0.05,'empirical_rejection_rate':k/N_SIM,
                         'wilson_95_low':lo,'wilson_95_high':hi})
    out=pd.DataFrame(rows)
    path=ROOT/'outputs'/'model_results'/'null_size_simulation.csv'
    out.to_csv(path,index=False)
    print(out.to_string(index=False))
    print('\nDGP: restricted model fitted to observed regressors; residual magnitudes held fixed; signs randomized.')
    print('This is a conditional, design-specific calibration experiment; not a universal size theorem.')

if __name__=='__main__':
    main()
