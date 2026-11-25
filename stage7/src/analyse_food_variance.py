"""Food covariance allocations to OFFICIAL headline inflation variance."""
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research_math import exact_contributions,covariance_shares
from prepare_inputs import ROOT,WEIGHTS

COMBINED_WEIGHTS=dict(zip(WEIGHTS,[.4586,.0238,.0653,.1007,.0684,.2832]))

def bootstrap_food_share(c,y,block,reps,seed):
    # Non-circular moving blocks, shared rows for all components and headline.
    # Applied to complete-calendar full samples only. Seasonal factors are held
    # fixed; these intervals do not incorporate seasonal-estimation uncertainty.
    n=len(y);rng=np.random.default_rng(seed)
    starts=rng.integers(0,n-block+1,size=(reps,int(np.ceil(n/block))))
    ix=(starts[:,:,None]+np.arange(block)).reshape(reps,-1)[:,:n]
    a=c['food_bev'].to_numpy()[ix];b=y.to_numpy()[ix]
    a=a-a.mean(axis=1,keepdims=True);b=b-b.mean(axis=1,keepdims=True)
    share=100*np.sum(a*b,axis=1)/np.sum(b*b,axis=1)
    return np.quantile(share,[.025,.975])

def main():
    old=pd.read_csv(ROOT.parent/'data/raw/cpi_2012_combined_groups.csv',index_col='date')
    old.index=pd.PeriodIndex(old.index,freq='M')
    new=pd.read_csv(ROOT/'data/processed/urban_cpi_levels.csv',index_col='month')
    new.index=pd.PeriodIndex(new.index,freq='M')
    rows=[];uncertainty=[];validation=[]
    for sector,source,weights in [('Combined',old,COMBINED_WEIGHTS),('Urban',new,WEIGHTS)]:
        groups=source[list(weights)];headline=source.headline
        rebuilt=groups.mul(pd.Series(weights)).sum(axis=1)
        residual=rebuilt-headline
        validation.append(dict(sector=sector,n=len(source),level_residual_mean=residual.mean(),level_residual_max_abs=residual.abs().max()))
        for frequency,lag,sa in [('MoM_raw',1,False),('MoM_STL7',1,True),('YoY_raw',12,False)]:
            if sa:
                levels=source[['headline',*weights]].apply(lambda s:np.exp(np.log(s)-STL(np.log(s),period=12,robust=True).fit().seasonal))
            else:levels=source
            c,y=exact_contributions(levels[list(weights)],levels.headline,weights,lag)
            c.to_csv(ROOT/f'data/processed/{sector.lower()}_{frequency}_exact_contributions.csv',index_label='month')
            for sample in ['full_history','matched_2018Q2_2024Q4','exclude_imputation_exposure','pre2020','post2021']:
                mask=np.ones(len(c),bool)
                if sample=='matched_2018Q2_2024Q4':mask=(c.index>='2018-04')&(c.index<='2024-12')
                if sample=='exclude_imputation_exposure':
                    # Exclude outcomes whose numerator OR denominator uses Apr/May2020.
                    bad={'2020-04','2020-05','2020-06'} if lag==1 else {'2020-04','2020-05','2021-04','2021-05'}
                    mask=~c.index.astype(str).isin(bad)
                if sample=='pre2020':mask=c.index<'2020-01'
                if sample=='post2021':mask=c.index>='2022-01'
                cc,yy=c.loc[mask],y.loc[mask]
                shares=covariance_shares(cc,yy)
                assert np.isclose(shares.sum(),100,atol=1e-9)
                assert np.allclose(cc.sum(axis=1),yy,atol=1e-10)
                for name,value in shares.items():rows.append(dict(sector=sector,frequency=frequency,sample=sample,component=name,n=len(cc),covariance_share_percent=value,mean_contribution_pp=cc[name].mean(),official_headline_variance=yy.var()))
            for block in [6,12]:
                lo,hi=bootstrap_food_share(c,y,block,4999,45520261121+lag+block+(100 if sector=='Urban' else 0)+(1000 if sa else 0))
                uncertainty.append(dict(sector=sector,frequency=frequency,sample='full_history',block_length=block,replications=4999,estimate=covariance_shares(c,y)['food_bev'],ci_low=lo,ci_high=hi,interpretation='Descriptive moving-block interval; seasonal factors fixed; finite-sample calibration not guaranteed'))
    pd.DataFrame(rows).to_csv(ROOT/'results/official_headline_variance_allocations.csv',index=False)
    pd.DataFrame(uncertainty).to_csv(ROOT/'results/food_variance_block_uncertainty.csv',index=False)
    pd.DataFrame(validation).to_csv(ROOT/'results/aggregation_residuals.csv',index=False)
    # Retain a precise bridge to the historical reconstructed-aggregate number.
    legacy=pd.read_csv(ROOT.parent/'outputs/tables/covariance_aware_group_variance_decomposition.csv')
    legacy=legacy[legacy.component.eq('food_bev')&legacy.decomposition.eq('six CPI groups')]
    reproduced=[]
    for frequency,lag,sa,label in [('MoM',1,False,'raw'),('MoM',1,True,'STL-adjusted'),('YoY',12,False,'raw-overlapping-12m-descriptive')]:
        groups=old[list(COMBINED_WEIGHTS)]
        if sa:groups=groups.apply(lambda s:np.exp(np.log(s)-STL(np.log(s),period=12,robust=True).fit().seasonal))
        rebuilt=groups.mul(pd.Series(COMBINED_WEIGHTS)).sum(axis=1)
        cc,yy=exact_contributions(groups,rebuilt,COMBINED_WEIGHTS,lag)
        actual=covariance_shares(cc,yy)['food_bev']
        expected=float(legacy.loc[legacy.frequency.eq(frequency)&legacy.basis.eq(label),'share_of_aggregate_variance_percent'].iloc[0])
        assert np.isclose(actual,expected,atol=1e-7)
        reproduced.append(dict(frequency=frequency,basis=label,legacy_food_share=expected,reproduced_food_share=actual,target='Group-built aggregate, not official headline'))
    pd.DataFrame(reproduced).to_csv(ROOT/'results/legacy_reconstructed_food_shares.csv',index=False)
    result=pd.DataFrame(rows);main=result[result['sample'].eq('full_history')&result.component.eq('food_bev')]
    print(main[['sector','frequency','n','covariance_share_percent']].to_string(index=False))
    fig,axes=plt.subplots(1,2,figsize=(11,4.8))
    for ax,sector in zip(axes,['Combined','Urban']):
        s=main[main.sector.eq(sector)&~main.frequency.eq('MoM_STL7')];ax.bar(['Monthly change','Year-on-year change'],s.covariance_share_percent,color=['#237a9b','#b66e3c'])
        for i,v in enumerate(s.covariance_share_percent):ax.text(i,v+1,f'{v:.1f}%',ha='center')
        ax.set(title=sector+' CPI',ylabel='Food covariance allocation (%)',ylim=(0,110));ax.grid(axis='y',alpha=.15)
    fig.suptitle('Food accounts for most official headline inflation variance\nRaw percentage changes; shares include covariance and are not causal',fontsize=13)
    fig.tight_layout();fig.savefig(ROOT/'figures/official_food_variance_shares.png',dpi=180);plt.close(fig)

if __name__=='__main__':main()
