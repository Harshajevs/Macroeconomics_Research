"""Small, explicit accounting and regression functions used in Stage 7."""
import numpy as np
import pandas as pd
from scipy.stats import t

def quarterly_average(monthly):
    if not isinstance(monthly.index, pd.PeriodIndex) or monthly.index.freqstr != 'M':
        raise ValueError('Monthly PeriodIndex required')
    if monthly.index.has_duplicates:
        raise ValueError('Duplicate months')
    complete = monthly.reindex(pd.period_range(monthly.index.min(), monthly.index.max(),freq='M'))
    key=complete.index.asfreq('Q')
    means=complete.groupby(key).mean()
    return means.where(complete.groupby(key).count()==3)

def slope_fit(y, u, times, trend=False, hac_lag=None, hc3=False):
    y,u,times = [np.asarray(x,dtype=float) for x in (y,u,times)]
    if not (len(y)==len(u)==len(times)) or not np.isfinite(np.r_[y,u,times]).all():
        raise ValueError('Regressions require explicit finite common rows')
    if len(set(times)) != len(times): raise ValueError('Duplicate calendar positions')
    X=np.column_stack([np.ones(len(u)),u,*([times-times.mean()] if trend else [])])
    n,k=X.shape
    if np.linalg.matrix_rank(X)<k or n<=k: raise ValueError('Insufficient rank or observations')
    bread=np.linalg.inv(X.T@X); beta=np.linalg.lstsq(X,y,rcond=None)[0]
    e=y-X@beta;h=np.sum(X*(X@bread),axis=1)
    if hc3:
        score=X*(e/(1-h))[:,None];cov=bread@(score.T@score)@bread
    elif hac_lag is not None:
        score=X*e[:,None];meat=score.T@score
        for lag in range(1,hac_lag+1):
            for i,ti in enumerate(times):
                js=np.flatnonzero(times==ti+lag)
                if len(js):
                    cross=np.outer(score[i],score[js[0]])
                    meat+=(1-lag/(hac_lag+1))*(cross+cross.T)
        cov=bread@meat@bread*n/(n-k)
    else: cov=bread*(e@e)/(n-k)
    se=float(np.sqrt(max(cov[1,1],0)));crit=t.ppf(.975,n-k)
    stat=beta[1]/se if se>0 else np.nan
    total=np.sum((y-y.mean())**2)
    return dict(n=n,slope=float(beta[1]),intercept=float(beta[0]),se=se,
                ci_low=float(beta[1]-crit*se),ci_high=float(beta[1]+crit*se),
                p_two_sided=float(2*t.sf(abs(stat),n-k)),
                r_squared=float(1-e@e/total) if total>0 else np.nan,
                correlation=float(np.corrcoef(y,u)[0,1]),max_leverage=float(h.max()),
                residual_sd=float(np.sqrt(e@e/(n-k))))

def exact_contributions(groups, headline, weights, lag=1):
    """Exact simple-percent change accounting using an explicit aggregation residual.

    C_g,t = 100 w_g (I_g,t-I_g,t-lag)/H_t-lag.
    Residual contribution = official headline change minus sum(C_g).
    Not a causal decomposition, and not a decomposition of log inflation.
    """
    if set(groups.columns)!=set(weights): raise ValueError('Group-weight mismatch')
    if not np.isclose(sum(weights.values()),1): raise ValueError('Weights must sum to one')
    if not groups.index.equals(headline.index): raise ValueError('Indices not aligned')
    contrib=groups.diff(lag).mul(pd.Series(weights),axis=1).div(headline.shift(lag),axis=0)*100
    total=100*(headline/headline.shift(lag)-1)
    contrib['aggregation_residual']=total-contrib.sum(axis=1,min_count=len(weights))
    mask=contrib.notna().all(axis=1)&total.notna()
    return contrib.loc[mask],total.loc[mask]

def covariance_shares(contributions,total):
    if not contributions.index.equals(total.index): raise ValueError('Non-paired accounting sample')
    if not np.isfinite(contributions.to_numpy()).all(): raise ValueError('Missing contributions')
    return contributions.apply(lambda c:100*c.cov(total)/total.var(ddof=1))
