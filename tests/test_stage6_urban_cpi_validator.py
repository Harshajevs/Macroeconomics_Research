from __future__ import annotations
import sys, unittest, tempfile, hashlib
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_ROOT/'src'))
from validate_stage6_urban_cpi import (validate_rows,CPIValidationError,EXPECTED_MONTHS,INDEX_FIELDS,GROUP_FIELDS,FLAG_FIELDS,ANCHOR_MONTHS)

def fixtures():
    digest='a'*64; rows=[]
    for i,m in enumerate(EXPECTED_MONTHS):
        # Smooth synthetic indices with different group trajectories; synthetic only.
        groups={
          'food_beverages_group1_index':100+i*0.65,
          'pan_tobacco_group2_index':100+i*0.30,
          'clothing_footwear_group3_index':100+i*0.35,
          'housing_group4_index':100+i*0.25,
          'fuel_light_group5_index':100+i*0.55,
          'miscellaneous_group6_index':100+i*0.40,
        }
        weights={'food_beverages_group1_index':36.29,'pan_tobacco_group2_index':1.36,'clothing_footwear_group3_index':5.57,'housing_group4_index':21.67,'fuel_light_group5_index':5.58,'miscellaneous_group6_index':29.53}
        vals={**groups,'urban_general_index':sum(groups[k]*v for k,v in weights.items())/100.0}
        row={'month':m,**{k:str(v) for k,v in vals.items()},'sector':'Urban','base_year':'2012','series':'Current','state_coverage':'All India',
             'source_document':'synthetic-source.xlsx','source_url':'https://example.invalid','retrieval_date':'2026-11-18','export_date':'2026-11-18',
             'filter_settings':'base_year=2012;sector=Urban;state=All India;series=Current','month_status':'final','raw_source_sha256':digest}
        flags={f:'false' for f in FLAG_FIELDS}
        if m=='2020-04':
            for f in ['flag_general_macro_imputed','flag_food_group1_macro_imputed','flag_pan_group2_macro_imputed','flag_clothing_group3_macro_imputed','flag_miscellaneous_group6_macro_imputed']: flags[f]='true'
        if m=='2020-05':
            for f in ['flag_general_macro_imputed','flag_food_group1_macro_imputed','flag_clothing_group3_macro_imputed','flag_miscellaneous_group6_macro_imputed']: flags[f]='true'
        row.update(flags); rows.append(row)
    anchors=[]
    monthmap={r['month']:r for r in rows}
    for m in ANCHOR_MONTHS:
        a={'month':m,'source_document':'synthetic-anchor','source_url':'https://example.invalid/anchor'}
        a.update({k:monthmap[m][k] for k in INDEX_FIELDS}); anchors.append(a)
    return rows,anchors

class TestStage6UrbanCPIValidatorV2(unittest.TestCase):
    def test_valid_long_156_month_panel(self):
        r,a=fixtures(); out=validate_rows(r,a,expected_raw_sha256='a'*64)
        self.assertEqual(out['rows'],156); self.assertEqual(out['first_month'],'2013-01'); self.assertEqual(out['last_month'],'2025-12')
        self.assertEqual(out['anchor_comparisons'],len(ANCHOR_MONTHS)*len(INDEX_FIELDS))
    def test_rates_in_place_of_levels_fail(self):
        r,a=fixtures(); r[5]['urban_general_index']='4.5'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_general_three_times_weighted_groups_fail(self):
        r,a=fixtures(); r[20]['urban_general_index']=str(float(r[20]['urban_general_index'])*3)
        # Update anchor if this is an anchor month; month 2014-09 is not an anchor.
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_tenfold_housing_spike_fail(self):
        r,a=fixtures(); j=100; r[j]['housing_group4_index']=str(float(r[j]['housing_group4_index'])*10)
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_food_copied_to_fuel_fail(self):
        r,a=fixtures()
        for row in r: row['fuel_light_group5_index']=row['food_beverages_group1_index']
        for ar in a:
            matching=next(x for x in r if x['month']==ar['month']); ar['fuel_light_group5_index']=matching['fuel_light_group5_index']
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_missing_anchor_fails(self):
        r,a=fixtures(); a=a[:-1]
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_anchor_mismatch_fails(self):
        r,a=fixtures(); a[0]['urban_general_index']=str(float(a[0]['urban_general_index'])+2)
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_raw_hash_mismatch_fails(self):
        r,a=fixtures()
        with self.assertRaises(CPIValidationError): validate_rows(r,a,expected_raw_sha256='b'*64)
    def test_duplicate_anchor_month_fails(self):
        r,a=fixtures(); a.append(a[0].copy())
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_wrong_sector_fails(self):
        r,a=fixtures(); r[0]['sector']='Combined'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_wrong_base_year_fails(self):
        r,a=fixtures(); r[0]['base_year']='2024'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_composite_residual_threshold_fails(self):
        r,a=fixtures(); r[20]['urban_general_index']=str(float(r[20]['urban_general_index'])*1.02)
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_moderate_monthly_jump_is_reported_not_repaired(self):
        r,a=fixtures(); r[50]['housing_group4_index']=str(float(r[50]['housing_group4_index'])*1.15)
        weights={'food_beverages_group1_index':36.29,'pan_tobacco_group2_index':1.36,'clothing_footwear_group3_index':5.57,'housing_group4_index':21.67,'fuel_light_group5_index':5.58,'miscellaneous_group6_index':29.53}
        r[50]['urban_general_index']=str(sum(float(r[50][k])*v for k,v in weights.items())/100.0)
        out=validate_rows(r,a)
        self.assertGreater(out['jump_warning_count'],0)
    def test_april_flag_false_fails(self):
        r,a=fixtures(); row=next(x for x in r if x['month']=='2020-04'); row['flag_pan_group2_macro_imputed']='false'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_may_pan_not_imputed(self):
        r,a=fixtures(); row=next(x for x in r if x['month']=='2020-05'); row['flag_pan_group2_macro_imputed']='true'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_bad_date_fails(self):
        r,a=fixtures(); r[0]['retrieval_date']='18/11/2026'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_mixed_raw_hashes_fail(self):
        r,a=fixtures(); r[1]['raw_source_sha256']='b'*64
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_wrong_month_order_fails(self):
        r,a=fixtures(); r[0],r[1]=r[1],r[0]
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_wrong_vintage_fails(self):
        r,a=fixtures(); r[0]['series']='Back Series'
        with self.assertRaises(CPIValidationError): validate_rows(r,a)
    def test_weighted_group_residuals_reported(self):
        r,a=fixtures(); out=validate_rows(r,a)
        self.assertEqual(len(out['residual_summary_by_subperiod']),3)

if __name__=='__main__': unittest.main()
