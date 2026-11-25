from pathlib import Path
import pandas as pd,numpy as np,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent;DATA=BASE/'research_data';OUT=BASE/'assets'
BLUE='#12647A';RUST='#BB603A';GOLD='#CC9D36';INK='#203743'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'legend.fontsize':8,
'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'savefig.bbox':'tight'})
d=pd.read_csv(DATA/'data/processed/combined_MoM_raw_exact_contributions.csv',index_col='month');d.index=pd.to_datetime(d.index)
x=pd.DataFrame({'food':d.food_bev,'other':d.sum(axis=1)-d.food_bev})
monthly=x.groupby(x.index.month).agg(['mean','count'])
monthly.to_csv(DATA/'results/monthly_contribution_calendar_means.csv')
summary=x.agg(['count','mean','median','std','min','max','skew','kurt']).T
summary.to_csv(DATA/'results/monthly_contribution_summary.csv')
fig,a=plt.subplots(figsize=(6.8,2.45));pos=np.arange(12);w=.35
for dx,col,color,label in [(-w/2,'food',BLUE,'Food'),(w/2,'other',RUST,'All other contributions + residual')]:
 a.bar(pos+dx,monthly[col]['mean'],w,color=color,label=label)
a.axhline(0,color=INK,lw=.8);a.set(xticks=pos,xticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],ylabel='Mean contribution (percentage points)')
a.legend(frameon=False,ncol=2,loc='upper left');a.grid(axis='y',alpha=.15);a.set_axisbelow(True);fig.tight_layout(pad=.6)
for ext in ['pdf','png']:fig.savefig(OUT/f'11_calendar_contributions.{ext}',dpi=240)
plt.close(fig)
h=x.sum(axis=1);var=h.var();own=x.food.var();cross=x.food.cov(x.other)
vals=[100*own/var,100*cross/var,100*(own+cross)/var]
fig,a=plt.subplots(figsize=(6.8,1.9))
a.barh([2,1,0],vals,color=[BLUE,GOLD,RUST],height=.58)
for y,val in zip([2,1,0],vals):a.text(val+1,y,f'{val:.2f}%',va='center',fontsize=10)
a.set(yticks=[2,1,0],yticklabels=['Food own-variance term','Food–other covariance term','Total food allocation'],xlabel='Percentage of official headline variance',xlim=(0,104))
a.grid(axis='x',alpha=.15);a.set_axisbelow(True);fig.tight_layout(pad=.6)
for ext in ['pdf','png']:fig.savefig(OUT/f'12_covariance_calculation.{ext}',dpi=240)
plt.close(fig)
rows=[]
for col,label in [('food','Food contribution'),('other','All other contributions')]:
 r=summary.loc[col];rows.append(label+' & '+' & '.join(f'{r[k]:.3f}' for k in ['mean','median','std','min','max'])+chr(92)*2)
text=r'''\begin{table}[H]
\centering\small
\caption{Monthly Combined CPI contributions: summary statistics}
\label{tab:contributionstats}
\begin{tabular}{lrrrrr}\toprule
Series & Mean & Median & SD & Minimum & Maximum\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}
\tabnote{Percentage points; 155 raw monthly changes. Other contributions include the aggregation residual.}
\end{table}
'''
(BASE/'tables/contribution_statistics.tex').write_text(text)
audit={'n':len(x),'food_variance':own,'headline_variance':var,'food_other_covariance':cross,'food_headline_covariance':x.food.cov(h),'own_share':vals[0],'cross_share':vals[1],'total_share':vals[2]}
(DATA/'results/additional_calculations.json').write_text(json.dumps(audit,indent=2))
print(summary.to_string());print(json.dumps(audit,indent=2))
