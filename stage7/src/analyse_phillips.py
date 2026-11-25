"""Simple matched-sample Urban Phillips associations; inference is descriptive."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import skew,kurtosis
from statsmodels.tsa.seasonal import STL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research_math import quarterly_average,slope_fit
from prepare_inputs import ROOT,WEIGHTS

EXCLUDED={'2020Q2','2020Q3','2021Q2'}
OUTCOMES=['headline','core_food_fuel_excluded','nonfood_only','core_no_housing']

def load_indices():
    d=pd.read_csv(ROOT/'data/processed/urban_cpi_levels.csv',index_col='month')
    d.index=pd.PeriodIndex(d.index,freq='M')
    for name,kept in [('core_food_fuel_excluded',['pan_tobacco','clothing','housing','misc']),
                      ('nonfood_only',['pan_tobacco','clothing','housing','fuel_light','misc']),
                      ('core_no_housing',['pan_tobacco','clothing','misc'])]:
        w=pd.Series({k:WEIGHTS[k] for k in kept});d[name]=d[kept].mul(w).sum(axis=1)/w.sum()
    return d

def transform(d,seasonal=13,history_start='2013-01',history_end='2025-12'):
    rawq=quarterly_average(d[OUTCOMES]);yoy=100*np.log(rawq/rawq.shift(4))
    hist=d.loc[history_start:history_end,OUTCOMES]
    sa=hist.apply(lambda s:np.exp(np.log(s)-STL(np.log(s),period=12,seasonal=seasonal,robust=True).fit().seasonal))
    saq=quarterly_average(sa);qoq=400*np.log(saq/saq.shift(1))
    return {'yoy_log':yoy,'qoq_saar':qoq}

def samples(d):
    return {'full27':np.ones(len(d),bool),'exclude_three_pandemic':~d.index.astype(str).isin(EXCLUDED),
            'exclude_2020_2021':~d.index.year.isin([2020,2021])}

def main():
    # Reject any drift in the pre-estimation inputs.
    for line in (ROOT/'documentation/pre_estimation_input_manifest.sha256').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    d=load_indices();transforms=transform(d)
    u=pd.read_csv(ROOT/'data/processed/urban_unemployment.csv',index_col='quarter')
    u.index=pd.PeriodIndex(u.index,freq='Q');u=u.sort_index()
    rows=[];leave=[];stats=[];matched=[]
    for frequency,pi in transforms.items():
        frame=u.join(pi,how='left');assert frame[OUTCOMES].notna().all().all()
        frame['calendar_position']=np.arange(len(frame))
        frame['pandemic_excluded_flag']=frame.index.astype(str).isin(EXCLUDED)
        frame.to_csv(ROOT/f'data/processed/phillips_{frequency}_matched.csv',index_label='quarter')
        for outcome in OUTCOMES[1:]:frame[outcome+'_minus_headline']=frame[outcome]-frame.headline
        allnames=OUTCOMES+[k+'_minus_headline' for k in OUTCOMES[1:]]
        for sample,mask in samples(frame).items():
            sub=frame.loc[mask]
            assert len(sub)=={'full27':27,'exclude_three_pandemic':24,'exclude_2020_2021':19}[sample]
            for var in ['unemployment']+OUTCOMES:
                s=sub[var];stats.append(dict(frequency=frequency,sample=sample,variable=var,n=len(s),mean=s.mean(),median=s.median(),sd=s.std(),minimum=s.min(),maximum=s.max(),skewness=skew(s,bias=False),excess_kurtosis=kurtosis(s,bias=False)))
            for trend in [False,True]:
                for var in allnames:
                    for method,kw in [('HC3',dict(hc3=True)),('calendar_HAC3',dict(hac_lag=3)),('calendar_HAC4',dict(hac_lag=4))]:
                        result=slope_fit(sub[var],sub.unemployment,sub.calendar_position,trend=trend,**kw)
                        rows.append(dict(frequency=frequency,sample=sample,trend=trend,outcome=var,inference_sensitivity=method,**result))
                # algebraic paired identity, including in trend-adjusted models
                results={v:slope_fit(sub[v],sub.unemployment,sub.calendar_position,trend=trend) for v in allnames}
                for var in OUTCOMES[1:]:
                    assert np.isclose(results[var]['slope']-results['headline']['slope'],results[var+'_minus_headline']['slope'],atol=1e-12)
            for quarter in sub.index:
                omit=sub.drop(index=quarter)
                for var in ['headline','core_food_fuel_excluded','core_food_fuel_excluded_minus_headline']:
                    r=slope_fit(omit[var],omit.unemployment,omit.calendar_position,hc3=True)
                    leave.append(dict(frequency=frequency,sample=sample,omitted_quarter=str(quarter),outcome=var,**r))
        matched.append((frequency,frame))
    pd.DataFrame(rows).to_csv(ROOT/'results/phillips_all_specifications.csv',index=False)
    pd.DataFrame(stats).to_csv(ROOT/'results/phillips_descriptive_statistics.csv',index=False)
    pd.DataFrame(leave).to_csv(ROOT/'results/phillips_leave_one_quarter_out.csv',index=False)
    sensitivity=[]
    for seasonal,start,end in [(7,'2013-01','2025-12'),(25,'2013-01','2025-12'),(13,'2014-01','2025-12'),(13,'2013-01','2024-12')]:
        pi=transform(d,seasonal,start,end)['qoq_saar'];frame=u.join(pi)
        for sample,mask in samples(frame).items():
            sub=frame.loc[mask]
            for outcome in ['headline','core_food_fuel_excluded','nonfood_only']:
                targets=[(outcome,sub[outcome])]
                if outcome!='headline':targets.append((outcome+'_minus_headline',sub[outcome]-sub.headline))
                for name,y in targets:
                    r=slope_fit(y,sub.unemployment,sub.index.asi8,hc3=True)
                    sensitivity.append(dict(seasonal_window=seasonal,history_start=start,history_end=end,sample=sample,outcome=name,**r))
    pd.DataFrame(sensitivity).to_csv(ROOT/'results/phillips_seasonal_history_sensitivity.csv',index=False)
    # Leverage is a property of U and the design, independent of inflation outcomes.
    uu=u.unemployment;ss=(uu-uu.mean())**2;leverage=1/len(uu)+ss/ss.sum()
    pd.DataFrame(dict(unemployment=uu,share_of_ur_ss_percent=100*ss/ss.sum(),ols_leverage=leverage)).to_csv(ROOT/'results/unemployment_leverage.csv',index_label='quarter')
    make_figures(matched)
    summary=pd.DataFrame(rows);print(summary[(~summary.trend)&summary.inference_sensitivity.eq('HC3')&summary['sample'].isin(['full27','exclude_three_pandemic'])&summary.outcome.isin(['headline','core_food_fuel_excluded','core_food_fuel_excluded_minus_headline'])][['frequency','sample','outcome','n','slope','ci_low','ci_high','correlation']].to_string(index=False))

def make_figures(matched):
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    colors={'headline':'#237a9b','core_food_fuel_excluded':'#b14c34'}
    for row,(frequency,frame) in enumerate(matched):
        ax=axes[row,0]
        for var in colors:ax.plot(frame.index.to_timestamp(),frame[var],label=var.replace('_',' '),color=colors[var],lw=1.8)
        ax.set(title='Urban inflation: '+frequency.replace('_',' '),ylabel='Percent (log change)')
        ax.axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2021-12-31'),color='grey',alpha=.12)
        ax.legend(fontsize=8,frameon=False)
        ax=axes[row,1]
        for var in colors:
            ax.scatter(frame.unemployment,frame[var],s=28,color=colors[var],alpha=.7,label=var.replace('_',' '))
            xx=np.array([frame.unemployment.min(),frame.unemployment.max()]);b=np.polyfit(frame.unemployment,frame[var],1);ax.plot(xx,b[0]*xx+b[1],color=colors[var])
        for q in ['2020Q2','2020Q3','2021Q2']:
            ax.annotate(q,(frame.loc[q,'unemployment'],frame.loc[q,'headline']),xytext=(3,3),textcoords='offset points',fontsize=8)
        ax.set(xlabel='Urban CWS unemployment, persons 15+ (%)',ylabel='Inflation (%)',title='Identical 27 quarters; simple OLS lines')
        ax.grid(alpha=.15)
    fig.suptitle('Headline versus operational core: descriptive Phillips associations',fontsize=14)
    fig.tight_layout();fig.savefig(ROOT/'figures/phillips_paths_and_scatter.png',dpi=180);plt.close(fig)

if __name__=='__main__':main()
