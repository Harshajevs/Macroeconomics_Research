import sys,unittest,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
ROOT=Path(__file__).resolve().parents[1]

class ActualInputsOutputs(unittest.TestCase):
    def test_exact_source_snapshot_and_bulletin_resolutions(self):
        for line in (ROOT/'data/input_integrity.sha256').read_text().splitlines():
            digest,name=line.split('  ',1)
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest,name)
        d=pd.read_csv(ROOT/'data/processed/plfs_api_bulletin_reconciliation.csv').set_index('quarter_id')
        self.assertEqual((d.loc['2019Q2','selected_ur'],d.loc['2019Q2','ur_api']),(8.8,21.6))
        self.assertEqual((d.loc['2019Q3','selected_ur'],d.loc['2019Q3','ur_api']),(8.3,8.1))
        c=pd.read_csv(ROOT/'data/processed/urban_cpi_levels.csv').set_index('month')
        self.assertEqual(len(c),156)
        self.assertEqual((c.loc['2024-12','headline'],c.loc['2024-12','fuel_light']),(192.,170.5))
        self.assertEqual((c.loc['2020-04','headline'],c.loc['2020-05','headline']),(150.9,150.6))

    def test_actual_common_sample_slopes_against_statsmodels(self):
        outputs=pd.read_csv(ROOT/'results/phillips_all_specifications.csv')
        for freq in ['yoy_log','qoq_saar']:
            d=pd.read_csv(ROOT/f'data/processed/phillips_{freq}_matched.csv',index_col='quarter')
            for sample in ['full27','exclude_three_pandemic']:
                sub=d if sample=='full27' else d.loc[~d.index.isin(['2020Q2','2020Q3','2021Q2'])]
                for trend in [False,True]:
                    X=sub[['unemployment']].copy()
                    if trend:X['time']=sub.calendar_position-sub.calendar_position.mean()
                    X=sm.add_constant(X)
                    for outcome in ['headline','core_food_fuel_excluded','core_food_fuel_excluded_minus_headline']:
                        y=sub.core_food_fuel_excluded-sub.headline if outcome.endswith('minus_headline') else sub[outcome]
                        fit=sm.OLS(y,X).fit().get_robustcov_results(cov_type='HC3')
                        row=outputs[(outputs.frequency==freq)&(outputs['sample']==sample)&(outputs.trend==trend)&(outputs.outcome==outcome)&(outputs.inference_sensitivity=='HC3')].iloc[0]
                        self.assertAlmostEqual(row.slope,fit.params[1],places=10)
                        self.assertAlmostEqual(row.se,fit.bse[1],places=10)

if __name__=='__main__':unittest.main()
