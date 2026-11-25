from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

BASE=Path(__file__).resolve().parent
DATA=BASE/'research_data'
ASSETS=BASE/'assets'
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,
 'axes.labelsize':9,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,
 'pdf.fonttype':42,'savefig.bbox':'tight'})
BLUE='#166781';RUST='#b35d3d';GREY='#c3cdd3'
bad=['2020Q2','2020Q3','2021Q2']
d=pd.read_csv(DATA/'data/processed/phillips_yoy_log_matched.csv',index_col='quarter')
dates=pd.PeriodIndex(d.index,freq='Q').to_timestamp()
fig,axes=plt.subplots(2,1,figsize=(6.7,3.9),sharex=True,gridspec_kw={'height_ratios':[.85,1]})
axes[0].plot(dates,d.unemployment,color=BLUE,lw=1.6,marker='o',ms=2.7)
axes[0].set(ylabel='Unemployment (%)',ylim=(4,23))
axes[0].annotate('2020Q2: 20.8%',xy=(dates[d.index.get_loc('2020Q2')],20.8),xytext=(dates[12],21.5),
 arrowprops={'arrowstyle':'-','color':'#4c6270'},fontsize=8)
axes[1].plot(dates,d.headline,color=BLUE,lw=1.6,label='Headline')
axes[1].plot(dates,d.core_food_fuel_excluded,color=RUST,lw=1.6,label='Operational core')
axes[1].set(ylabel='YoY log inflation (%)',ylim=(2.5,7.5))
axes[1].legend(frameon=False,ncol=2,loc='upper right')
for ax in axes:
 ax.axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2021-12-31'),color='#e9edf0',zorder=0)
 ax.grid(axis='y',alpha=.18)
fig.tight_layout(pad=.6,h_pad=.7)
fig.savefig(ASSETS/'time_paths.pdf');fig.savefig(ASSETS/'time_paths.png',dpi=220);plt.close(fig)

for freq,name in [('yoy_log','scatter_yoy'),('qoq_saar','scatter_qoq')]:
 x=pd.read_csv(DATA/f'data/processed/phillips_{freq}_matched.csv',index_col='quarter')
 keep=~x.index.isin(bad)
 fig,axes=plt.subplots(1,2,figsize=(6.7,2.8),sharex=True,sharey=True)
 for ax,var,title in zip(axes,['headline','core_food_fuel_excluded'],['Headline inflation','Operational core inflation']):
  ax.scatter(x.loc[keep,'unemployment'],x.loc[keep,var],s=19,color=BLUE,alpha=.85,zorder=3)
  ax.scatter(x.loc[~keep,'unemployment'],x.loc[~keep,var],s=29,color=RUST,marker='D',zorder=4)
  xx=np.linspace(x.unemployment.min(),x.unemployment.max(),100)
  for mask,ls,color,label in [(np.ones(len(x),bool),'-',BLUE,'Full sample'),(keep,'--',RUST,'Exclude 3 quarters')]:
   b=np.polyfit(x.loc[mask,'unemployment'],x.loc[mask,var],1)
   ax.plot(xx,b[0]*xx+b[1],ls,color=color,lw=1.1,label=label)
  ax.set(title=title,xlabel='Urban unemployment (%)')
  ax.grid(alpha=.15)
 axes[0].set_ylabel('YoY log inflation (%)' if freq=='yoy_log' else 'q/q SAAR log inflation (%)')
 axes[0].legend(frameon=False,loc='lower right',fontsize=7)
 fig.tight_layout(pad=.5,w_pad=1)
 fig.savefig(ASSETS/(name+'.pdf'));fig.savefig(ASSETS/(name+'.png'),dpi=220);plt.close(fig)

v=pd.read_csv(DATA/'results/official_headline_variance_allocations.csv')
v=v[v['sample'].eq('full_history')&v.component.eq('food_bev')&~v.frequency.eq('MoM_STL7')]
fig,ax=plt.subplots(figsize=(6.7,2.55));pos=np.arange(2);width=.32
for dx,sector,color in [(-width/2,'Combined',BLUE),(width/2,'Urban',RUST)]:
 vals=[v.loc[v.sector.eq(sector)&v.frequency.eq(f),'covariance_share_percent'].iloc[0] for f in ['MoM_raw','YoY_raw']]
 bars=ax.bar(pos+dx,vals,width,color=color,label=sector)
 for bar,val in zip(bars,vals):ax.annotate(f'{val:.1f}%',(bar.get_x()+bar.get_width()/2,val),xytext=(0,4),textcoords='offset points',ha='center',fontsize=9)
ax.set(xticks=pos,xticklabels=['Monthly change','Year-on-year change'],ylabel='Food covariance allocation (%)',ylim=(0,105))
ax.yaxis.set_major_locator(MultipleLocator(20));ax.legend(frameon=False,ncol=2,loc='upper right');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.tight_layout(pad=.5);fig.savefig(ASSETS/'food_variance.pdf');fig.savefig(ASSETS/'food_variance.png',dpi=220);plt.close(fig)

lev=pd.read_csv(DATA/'results/unemployment_leverage.csv')
fig,ax=plt.subplots(figsize=(6.7,2.5));colors=[RUST if q in bad else GREY for q in lev.quarter]
ax.bar(np.arange(len(lev)),lev.share_of_ur_ss_percent,color=colors,width=.8)
ax.set(ylabel='Share of unemployment\nvariation (%)',ylim=(0,70),xticks=np.arange(0,27,4),xticklabels=lev.quarter.iloc[::4])
ax.annotate('2020Q2: 61.4%',(8,61.38),xytext=(11,59),arrowprops={'arrowstyle':'-','color':RUST},fontsize=9)
ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);fig.tight_layout(pad=.5)
fig.savefig(ASSETS/'leverage.pdf');fig.savefig(ASSETS/'leverage.png',dpi=220);plt.close(fig)
print('Five publication figures generated as vector PDF and PNG.')
