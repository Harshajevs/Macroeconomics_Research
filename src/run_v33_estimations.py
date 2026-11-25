"""Reproducible v3.3 model runs in restartable batches.

Run from project root:
  python src/run_v33_estimations.py --batch forward
  python src/run_v33_estimations.py --batch core
  python src/run_v33_estimations.py --batch reverse

The batches can be rerun independently. They write postreview_* outputs only.
"""
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import estimate_baseline as m

OUT = m.OUT


def build_comparison():
    rows=[]
    for f in sorted(OUT.glob('postreview_*_model_summary.csv')):
        d=pd.read_csv(f)
        if len(d)!=1: continue
        r=d.iloc[0]
        rows.append({
            'label':r.get('label',f.stem.replace('_model_summary','')),
            'direction':r.get('direction'), 'sample_start':r.get('sample_first_date',r.get('final_start')),
            'sample_end':r.get('sample_last_date'), 'n':r.get('n'), 'p':r.get('final_selected_p'),
            'q':r.get('q'), 'HAC6_joint_chi2_p':r.get('HAC6_joint_chi2_p'),
            'HAC6_joint_F_p':r.get('HAC6_joint_F_p'), 'HC3_joint_chi2_p':r.get('HC3_joint_chi2_p'),
            'HAC12_joint_chi2_p':r.get('HAC12_joint_chi2_p'),
            'block_wild_bootstrap_tail_probability':r.get('wild_block_bootstrap_wald_tail_probability'),
            'bootstrap_reps':r.get('wild_block_bootstrap_reps_successful'),
            'primary_comparable_delayed_sum_definition':r.get('primary_comparable_delayed_sum_definition'),
            'primary_comparable_delayed_sum':r.get('primary_comparable_delayed_sum'),
            'delayed_sum_HAC_CI_low':r.get('primary_comparable_delayed_sum_CI_low'),
            'delayed_sum_HAC_CI_high':r.get('primary_comparable_delayed_sum_CI_high'),
            'delayed_sum_bootstrap_t_CI_low':r.get('delayed_sum_bootstrap_t_CI_low'),
            'delayed_sum_bootstrap_t_CI_high':r.get('delayed_sum_bootstrap_t_CI_high'),
            'interpretation_scope':'Conditional predictive association; not causal identification.'
        })
    pd.DataFrame(rows).to_csv(OUT/'postreview_model_comparison_summary.csv',index=False)
    return len(rows)


def run_forward():
    d, parts = m.estimate('postreview_primary_q3_oct2013',3,'2013-10',
        run_bootstrap=True,bootstrap_interval=True,bootstrap_contemporaneous=True,
        run_stability_bootstrap=True,full_diagnostics=True)
    m.leave_out_checks('postreview_primary_q3_oct2013',*parts,3)
    specs=[('postreview_q3_jan2014',3,'2014-01',{}),
           ('postreview_q1_jan2014',1,'2014-01',{}),
           ('postreview_q6_jan2014',6,'2014-01',{}),
           ('postreview_fit2016_q3',3,'2016-04',{}),
           ('postreview_covid_exclusion_mar2020_dec2021_q3',3,'2013-10',
            {'mask_months':m.COVID_EXCLUSION,'allow_fallback':False,'include_covid_controls':False}),
           ('postreview_covid_exclusion_mar2020_dec2020_q3',3,'2013-10',
            {'mask_months':pd.period_range('2020-03','2020-12',freq='M'),'allow_fallback':False,'include_covid_controls':False}),
           ('postreview_imputed_aprmay2020_exclusion_nonfood_q3',3,'2013-10',
            {'mask_months':pd.period_range('2020-04','2020-05',freq='M'),'allow_fallback':False})]
    for label,q,start,kw in specs:
        m.estimate(label,q,start,run_bootstrap=True,full_diagnostics=False,**kw)
    m.estimate('postreview_stl_adjusted_q3',3,'2013-10',stl=True,
        allow_fallback=False,include_covid_controls=False,run_bootstrap=True,
        bootstrap_interval=True,full_diagnostics=False)
    m.short_run_sum_benchmark()
    print('Forward batch completed; baseline/core not overwritten.')


def run_core():
    specs=[('postreview_core_q3_oct2013',3,'2013-10',True),
           ('postreview_core_q3_jan2014',3,'2014-01',False),
           ('postreview_core_q1_jan2014',1,'2014-01',False),
           ('postreview_core_q6_jan2014',6,'2014-01',False)]
    for label,q,start,primary in specs:
        m.estimate(label,q,start,direction='food_to_core',run_bootstrap=True,
            bootstrap_interval=primary,bootstrap_contemporaneous=primary,
            run_stability_bootstrap=primary,full_diagnostics=primary)
    m.estimate('postreview_core_imputed_aprmay2020_exclusion_q3',3,'2013-10',
        direction='food_to_core',mask_months=pd.period_range('2020-04','2020-05',freq='M'),
        allow_fallback=False,run_bootstrap=True,full_diagnostics=False)
    m.estimate('postreview_core_covid_exclusion_mar2020_dec2021_q3',3,'2013-10',
        direction='food_to_core',mask_months=m.COVID_EXCLUSION,allow_fallback=False,
        include_covid_controls=False,run_bootstrap=True,full_diagnostics=False)
    m.short_run_sum_benchmark()
    print('Core batch completed.')


def run_reverse():
    specs=[('postreview_reverse_nonfood_to_food_q3',None,True),
           ('postreview_reverse_covid_exclusion_mar2020_dec2020_q3',pd.period_range('2020-03','2020-12',freq='M'),False),
           ('postreview_reverse_covid_exclusion_mar2020_dec2021_q3',m.COVID_EXCLUSION,False),
           ('postreview_reverse_imputed_aprmay2020_exclusion_q3',pd.period_range('2020-04','2020-05',freq='M'),True),
           ('postreview_reverse_stl_q3',None,False)]
    for label,mask,controls in specs:
        stl=label.endswith('_stl_q3')
        kw={'direction':'nonfood_to_food','allow_fallback':False,
            'run_bootstrap':True,'full_diagnostics':False,'stl':stl,
            'include_covid_controls':False if stl or mask is not None and len(mask)>=10 else True}
        if mask is not None: kw['mask_months']=mask
        m.estimate(label,3,'2014-01',**kw)
    inter=m.post2021_interaction()
    m.export_bidirectional_summary()
    print('Reverse batch completed. Post-2021 interaction:',inter)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--batch',choices=['forward','core','reverse','all'],required=True)
    args=parser.parse_args()
    if args.batch in ('forward','all'): run_forward()
    if args.batch in ('core','all'): run_core()
    if args.batch in ('reverse','all'): run_reverse()
    n=build_comparison()
    print(f'Comparison summary rebuilt from {n} individual model summaries.')

if __name__=='__main__': main()
