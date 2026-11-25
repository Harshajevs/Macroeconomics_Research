"""Generate the report's figures from the verified, portable CSV subset."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
BASE=Path(__file__).resolve().parent
DATA=BASE/'research_data'; OUT=BASE/'assets';OUT.mkdir(exist_ok=True)
BLUE='#12647A';RUST='#BB603A';GOLD='#CC9D36';GREY='#B9C8D0';INK='#203743'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,'axes.titlesize':10,
'axes.labelsize':9,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,
'axes.labelcolor':INK,'text.color':INK,'xtick.color':INK,'ytick.color':INK,
'pdf.fonttype':42,'savefig.bbox':'tight','axes.titlepad':9})
bad=['2020Q2','2020Q3','2021Q2']
yoy=pd.read_csv(DATA/'data/processed/phillips_yoy_log_matched.csv',index_col='quarter')
qoq=pd.read_csv(DATA/'data/processed/phillips_qoq_saar_matched.csv',index_col='quarter')
keep=~yoy.index.isin(bad)
def save(fig,name):
 fig.savefig(OUT/(name+'.pdf'));fig.savefig(OUT/(name+'.png'),dpi=240);plt.close(fig)
def grid(ax):ax.grid(axis='y',alpha=.17);ax.set_axisbelow(True)
# 1: matched time paths.
dates=pd.PeriodIndex(yoy.index,freq='Q').to_timestamp()
fig,ax=plt.subplots(2,1,figsize=(6.8,3.65),sharex=True,gridspec_kw={'height_ratios':[.8,1]})
ax[0].plot(dates,yoy.unemployment,color=BLUE,marker='o',ms=2.5,lw=1.6)
ax[0].set(ylabel='Unemployment (%)',ylim=(4.5,23))
ax[0].annotate('20.8% in 2020Q2',(dates[8],20.8),xytext=(dates[12],21.4),fontsize=8,
 arrowprops={'arrowstyle':'-','color':INK})
for v,c,label in [('headline',BLUE,'Headline'),('core_food_fuel_excluded',RUST,'Core')]:ax[1].plot(dates,yoy[v],color=c,label=label,lw=1.6)
ax[1].set(ylabel='YoY log inflation (%)',ylim=(2.6,7.5));ax[1].legend(frameon=False,ncol=2,loc='upper right')
for a in ax:a.axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2021-12-31'),color='#ECF0F2',zorder=0);grid(a)
fig.tight_layout(pad=.7,h_pad=.5);save(fig,'01_time_paths')
# 2: empirical distribution, exact observed points and moments in the table.
fig,ax=plt.subplots(1,2,figsize=(6.8,2.55),gridspec_kw={'width_ratios':[1,1.05]})
u=yoy.unemployment
ax[0].hist(u,bins=np.arange(6,23,1),color=BLUE,alpha=.85,edgecolor='white')
ax[0].axvline(u.mean(),c=RUST,lw=1.2,label=f'Mean {u.mean():.2f}')
ax[0].axvline(u.median(),c=GOLD,lw=1.2,ls='--',label=f'Median {u.median():.2f}')
ax[0].set(title='A. Unemployment is right-skewed',xlabel='Unemployment (%)',ylabel='Number of quarters',ylim=(0,11))
ax[0].legend(frameon=False,fontsize=7.5,loc='upper right');grid(ax[0])
series=[yoy.headline,yoy.core_food_fuel_excluded,qoq.headline,qoq.core_food_fuel_excluded]
bp=ax[1].boxplot(series,patch_artist=True,widths=.52,showfliers=False,
 medianprops={'color':'white','lw':1.5},whiskerprops={'color':INK},capprops={'color':INK})
for i,patch in enumerate(bp['boxes']):patch.set_facecolor([BLUE,RUST][i%2]);patch.set_alpha(.85)
for i,arr in enumerate(series):ax[1].scatter(np.full(len(arr),i+1)+np.linspace(-.12,.12,len(arr)),arr,s=6,c=INK,alpha=.36,zorder=3)
ax[1].set(title='B. Short-run core is less dispersed',xticks=[1,2,3,4],xticklabels=['H: YoY','C: YoY','H: q/q','C: q/q'],ylabel='Inflation (%)');ax[1].tick_params(axis='x',labelsize=8);grid(ax[1])
fig.tight_layout(pad=.7,w_pad=1.3);save(fig,'02_distributions')
# 3: sample-specific correlations; same variables, rows, ordering and scale.
fig,ax=plt.subplots(1,2,figsize=(6.8,2.4))
cols=['unemployment','headline','core_food_fuel_excluded'];names=['Unemployment','Headline','Core']
for a,d,title in zip(ax,[yoy,yoy.loc[keep]],['All 27 quarters','Exclude three quarters (n = 24)']):
 corr=d[cols].corr();im=a.imshow(corr,vmin=-1,vmax=1,cmap='RdBu_r')
 a.set(xticks=np.arange(3),yticks=np.arange(3),xticklabels=['U','Headline','Core'],yticklabels=['U','Headline','Core'],title=title)
 a.tick_params(axis='x',labelsize=8);a.tick_params(axis='y',labelsize=8)
 for i in range(3):
  for j in range(3):a.text(j,i,f'{corr.iloc[i,j]:.3f}',ha='center',va='center',color='white' if abs(corr.iloc[i,j])>.6 else INK,fontsize=10)
 for spine in a.spines.values():spine.set_visible(False)
fig.subplots_adjust(wspace=.5,left=.14,right=.88,bottom=.16,top=.84)
cax=fig.add_axes([.91,.18,.018,.64]);fig.colorbar(im,cax=cax,ticks=[-1,0,1]);save(fig,'03_correlations')
# 4: four actual scatter plots with fitted lines. Exclusion fits shown only over observed support.
fig,ax=plt.subplots(2,2,figsize=(6.8,4.5),sharex=True,sharey='row')
for row,(d,frequency) in enumerate([(yoy,'YoY log'),(qoq,'q/q SAAR')]):
 for col,(v,label) in enumerate([('headline','Headline'),('core_food_fuel_excluded','Core')]):
  a=ax[row,col];k=~d.index.isin(bad)
  a.scatter(d.loc[k,'unemployment'],d.loc[k,v],s=18,c=BLUE,alpha=.85,zorder=3)
  a.scatter(d.loc[~k,'unemployment'],d.loc[~k,v],s=26,c=RUST,marker='D',zorder=4)
  for mask,color,ls,lab in [(np.ones(len(d),bool),BLUE,'-','Full'),(k,RUST,'--','Exclusion')]:
   b=np.polyfit(d.loc[mask,'unemployment'],d.loc[mask,v],1)
   xx=np.linspace(d.loc[mask,'unemployment'].min(),d.loc[mask,'unemployment'].max(),80)
   a.plot(xx,np.polyval(b,xx),color=color,ls=ls,lw=1.25,label=lab)
  a.set(title=f'{chr(65+row*2+col)}. {label}: {frequency}')
  if col==0:a.set_ylabel('Inflation (%)')
  if row==1:a.set_xlabel('Urban unemployment (%)')
  a.grid(alpha=.15)
ax[0,0].legend(frameon=False,ncol=2,fontsize=7.5,loc='upper left')
fig.tight_layout(pad=.65,h_pad=1.2,w_pad=1);save(fig,'04_phillips_scatter')
# 5: direct slope difference and nominal HC3 ranges.
c=pd.read_csv(DATA/'results/primary_phillips_comparison.csv')
fig,a=plt.subplots(figsize=(6.8,1.75))
for i,(f,s,label) in enumerate([('yoy_log','full27','YoY: full'),('yoy_log','exclude_three_pandemic','YoY: exclusion'),('qoq_saar','full27','q/q: full'),('qoq_saar','exclude_three_pandemic','q/q: exclusion')]):
 r=c[c.frequency.eq(f)&c['sample'].eq(s)].iloc[0];val=r.core_minus_headline_slope
 a.errorbar(val,3-i,xerr=[[val-r.nominal_HC3_difference_low],[r.nominal_HC3_difference_high-val]],fmt='o',c=BLUE if s=='full27' else RUST,capsize=3,ms=5,lw=1.5)
 a.text(1.28,3-i,f'{val:+.3f}',va='center',fontsize=9)
a.axvline(0,c=INK,lw=1,ls=':');a.set(yticks=[3,2,1,0],yticklabels=['YoY: full','YoY: exclusion','q/q: full','q/q: exclusion'],xlabel='Core slope minus headline slope (percentage points)',xlim=(-.48,1.48),ylim=(-.65,3.65));a.spines['left'].set_visible(False);grid(a)
fig.tight_layout(pad=.6);save(fig,'05_slope_difference')
# 6: influence and leave-one-out distributions.
lev=pd.read_csv(DATA/'results/unemployment_leverage.csv')
loo=pd.read_csv(DATA/'results/phillips_leave_one_quarter_out.csv')
loo=loo[loo['sample'].eq('full27')]
fig,ax=plt.subplots(1,2,figsize=(6.8,2.25),gridspec_kw={'width_ratios':[1.1,1]})
ax[0].bar(np.arange(len(lev)),lev.share_of_ur_ss_percent,color=[RUST if q in bad else GREY for q in lev.quarter])
ax[0].set(title='A. Unemployment variation',ylabel='Share of centred sum of squares (%)',ylim=(0,72),xticks=[0,8,16,24],xticklabels=['2018Q2','2020Q2','2022Q2','2024Q2'])
ax[0].tick_params(axis='x',labelsize=7.5);ax[0].annotate('61.4%',(8,61.38),xytext=(12,64),fontsize=9,arrowprops={'arrowstyle':'-','color':RUST});grid(ax[0])
for j,(f,label) in enumerate([('yoy_log','YoY'),('qoq_saar','q/q')]):
 for o,dx,color in [('headline',-.12,BLUE),('core_food_fuel_excluded',.12,RUST)]:
  vals=loo[loo.frequency.eq(f)&loo.outcome.eq(o)].slope
  ax[1].scatter(j+dx+np.linspace(-.045,.045,len(vals)),vals,s=10,c=color,alpha=.65,label='Headline' if j==0 and o=='headline' else 'Core' if j==0 else None)
ax[1].axhline(0,c=INK,ls=':',lw=1);ax[1].set(title='B. Full-sample leave-one-out',xticks=[0,1],xticklabels=['YoY','q/q'],ylabel='Unemployment slope');ax[1].legend(frameon=False,ncol=2,fontsize=7.5,loc='upper left');grid(ax[1]);fig.tight_layout(pad=.65,w_pad=1);save(fig,'06_influence')
# 7: contribution shares plus descriptive 12-month moving-block ranges.
v=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv')
b=pd.read_csv(DATA/'results/food_variance_block_uncertainty.csv')
fig,a=plt.subplots(figsize=(6.8,1.85));positions=np.arange(2);w=.30
for dx,sector,color in [(-w/2,'Combined',BLUE),(w/2,'Urban',RUST)]:
 vals=[];lo=[];hi=[]
 for f in ['MoM_raw','YoY_raw']:
  r=b[b.sector.eq(sector)&b.frequency.eq(f)&b.block_length.eq(12)].iloc[0]
  vals.append(r.estimate);lo.append(r.estimate-r.ci_low);hi.append(r.ci_high-r.estimate)
 bars=a.bar(positions+dx,vals,w,color=color,label=sector)
 a.errorbar(positions+dx,vals,yerr=[lo,hi],fmt='none',ecolor=INK,capsize=3,lw=1)
 for bar,val in zip(bars,vals):a.text(bar.get_x()+bar.get_width()/2,4,f'{val:.2f}%',ha='center',va='bottom',color='white',weight='bold',fontsize=9)
a.set(xticks=positions,xticklabels=['Monthly changes','Year-on-year changes'],ylabel='Food share (%)',ylim=(0,122));a.yaxis.set_major_locator(MultipleLocator(25));a.legend(frameon=False,ncol=2,loc='upper right');grid(a);fig.tight_layout(pad=.6);save(fig,'07_food_variance')
# 8: raw monthly official inflation and component contributions in two baskets.
fig,ax=plt.subplots(2,1,figsize=(6.8,3.8),sharex=True)
for a,sector in zip(ax,['combined','urban']):
 d=pd.read_csv(DATA/f'data/processed/{sector}_MoM_raw_exact_contributions.csv',index_col='month');d.index=pd.to_datetime(d.index)
 h=d.sum(axis=1);other=h-d.food_bev
 a.plot(d.index,h,c=INK,lw=1.05,label='Official headline')
 a.plot(d.index,d.food_bev,c=BLUE,lw=1.1,label='Food contribution')
 a.fill_between(d.index,0,other,color=GOLD,alpha=.34,label='All other contributions + residual')
 a.axhline(0,color=GREY,lw=.7);a.set(title=sector.title()+' CPI',ylabel='Percentage points');grid(a)
ax[0].legend(frameon=False,ncol=3,fontsize=7.2,loc='upper left');fig.tight_layout(pad=.6,h_pad=.9);save(fig,'08_monthly_contributions')
# 9: delayed sum vs current-plus-lags, different estimands clearly separated.
s=pd.read_csv(DATA/'results/spillover_effect_intervals.csv');fig,a=plt.subplots(figsize=(6.8,1.8))
for i,(direction,contrast,label) in enumerate([('food_to_nonfood','delayed_sum','Non-food: delayed 1–3'),('food_to_core','delayed_sum','Core: delayed 1–3'),('food_to_nonfood','current_plus_lags','Non-food: current + 1–3'),('food_to_core','current_plus_lags','Core: current + 1–3')]):
 r=s[s.direction.eq(direction)&s.contrast.eq(contrast)&s.method.eq('HC3')].iloc[0]
 a.errorbar(r.estimate,3-i,xerr=[[r.estimate-r.ci_low],[r.ci_high-r.estimate]],fmt='o',c=BLUE if contrast=='delayed_sum' else RUST,capsize=3,ms=5)
 a.text(.115,3-i,f'{r.estimate:+.4f}',va='center',fontsize=9)
a.axvline(0,c=INK,lw=1,ls=':');a.axhline(1.5,c=GREY,lw=.7)
a.set(yticks=[3,2,1,0],yticklabels=['Non-food: delayed 1–3','Core: delayed 1–3','Non-food: current + 1–3','Core: current + 1–3'],xlabel='Sum of food-inflation coefficients',xlim=(-.09,.155),ylim=(-.65,3.65));a.spines['left'].set_visible(False);grid(a);fig.tight_layout(pad=.6);save(fig,'09_spillover')
# 10 (appendix): power is design-specific, not a claim of exact inference.
sim=pd.read_csv(DATA/'results/spillover_recursive_calibration.csv');fig,a=plt.subplots(figsize=(6.8,2.4))
for method,color,label in [('HAC6',GOLD,'HAC(6)'),('HC3',RUST,'HC3'),('block_wild',BLUE,'Block wild')]:
 d=sim[sim.direction.eq('food_to_nonfood')&sim.scenario.eq('ar_garch')&sim.method.eq(method)].sort_values('true_delayed_sum')
 a.plot(d.true_delayed_sum,100*d.rejection_rate,c=color,label=label,marker='o',ms=4)
a.axhline(80,c=GREY,ls='--',lw=1);a.axhline(5,c=GREY,ls=':',lw=1)
a.set(xlabel='True sum across three delayed coefficients',ylabel='Rejection rate (%)',ylim=(0,105),xlim=(-.005,.207));a.legend(frameon=False,ncol=3,loc='upper left');grid(a);fig.tight_layout(pad=.6);save(fig,'10_power')
print('10 vector figures generated (18 panels in total).')
