"""Regenerate the Stage 6 aggregate PLFS UR figure from the checked input CSV."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/raw/plfs_urban_quarterly_ur_2018_2024.csv')
y=df['ur_cws_15plus_person_pct'].astype(float)
exclude={'2020Q2','2020Q3','2021Q2'}
fig,ax=plt.subplots(figsize=(11,5))
ax.plot(df['quarter_id'],y,marker='o',linewidth=1.6)
for q in exclude:
    r=df.loc[df.quarter_id==q].iloc[0]
    ax.annotate(q,(r['quarter_id'],r['ur_cws_15plus_person_pct']),xytext=(0,10),textcoords='offset points',ha='center')
ax.set_title('All-India Urban PLFS unemployment rate (CWS, age 15+)')
ax.set_ylabel('Unemployment rate (%)'); ax.set_xlabel('Quarter'); ax.tick_params(axis='x',rotation=60)
ax.grid(alpha=.25); fig.tight_layout()
out=ROOT/'outputs/figures/stage6_aggregate_ur_leverage_diagnostics.png'
fig.savefig(out,dpi=180); plt.close(fig)
print(out)
