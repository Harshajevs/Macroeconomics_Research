"""Protect the legacy inference behaviors identified in the supplied audit."""
import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
import statsmodels.api as sm
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
import estimate_baseline as m

class LegacyInferenceProtection(unittest.TestCase):
    def fixture(self):
        rng=np.random.default_rng(19);x=rng.normal(size=48)
        X=pd.DataFrame({'const':np.ones(48),'x_l1':x,'nuisance':rng.normal(size=48)})
        y=pd.Series(2+3*x+.3*X.nuisance+rng.normal(size=48))
        return y,X

    def test_restricted_null_bandwidth_and_plus_one_tail(self):
        y,X=self.fixture();xr=X.drop(columns='x_l1').to_numpy();fit=xr@np.linalg.lstsq(xr,y,rcond=None)[0];e=np.asarray(y)-fit
        signs=np.resize([-1.,1.],len(y));captured=[];calls=[]
        def statistic(ystar,full,R,nlags):
            captured.append(np.asarray(ystar));calls.append(nlags)
            return 11. if len(captured)<=3 else 9.
        with patch.object(m,'_block_signs',return_value=signs),patch.object(m,'hac_wald_statistic',side_effect=statistic):
            r=m.wild_block_bootstrap_wald(y,X,['x_l1'],10.,reps=99,block_length=6,seed=55)
        np.testing.assert_allclose(captured[0],fit+e*signs,atol=1e-12)
        self.assertEqual(calls,[6]*99)
        self.assertEqual(r['wild_block_bootstrap_wald_tail_probability'],.04)

    def test_block_signs_are_rademacher_on_offset_six_month_grid(self):
        class FixedRng:
            def __init__(self):self.i=0
            def integers(self,a,b):return 2
            def choice(self,choices):
                assert list(choices)==[-1.,1.]
                self.i+=1;return -1. if self.i%2 else 1.
        s=m._block_signs(21,6,FixedRng())
        np.testing.assert_array_equal(s,np.r_[np.repeat(-1.,4),np.repeat(1.,6),np.repeat(-1.,6),np.repeat(1.,5)])

    def test_bootstrap_t_endpoints_against_independent_statsmodels(self):
        y,X=self.fixture();fit=sm.OLS(y,X).fit();w=np.array([0.,1.,0.]);theta=float(w@fit.params)
        se=np.sqrt(w@fit.get_robustcov_results(cov_type='HAC',maxlags=6,use_correction=True).cov_params()@w)
        rng=np.random.default_rng(303);ts=[]
        for _ in range(79):
            # Independent multiplier construction, same documented RNG order.
            offset=int(rng.integers(0,6));s=np.ones(len(y))
            for start in range(-offset,len(y),6):s[max(0,start):min(len(y),start+6)]=rng.choice([-1.,1.])
            b=sm.OLS(fit.fittedvalues+fit.resid*s,X).fit()
            bs=np.sqrt(w@b.get_robustcov_results(cov_type='HAC',maxlags=6,use_correction=True).cov_params()@w)
            ts.append((float(w@b.params)-theta)/bs)
        lo,hi=np.quantile(ts,[.025,.975])
        got=m.wild_block_bootstrap_t_interval(y,X,['x_l1'],[1],reps=79,seed=303)
        self.assertAlmostEqual(got['delayed_sum_bootstrap_t_CI_low'],theta-hi*se,places=10)
        self.assertAlmostEqual(got['delayed_sum_bootstrap_t_CI_high'],theta-lo*se,places=10)
        self.assertLess(got['delayed_sum_bootstrap_t_CI_low'],got['delayed_sum_bootstrap_t_CI_high'])

    def test_estimate_passes_fixed_candidate_covid_horizon(self):
        original=m.design;calls=[]
        def capture(*args,**kwargs):calls.append(kwargs['covid_lag_horizon']);return original(*args,**kwargs)
        with tempfile.TemporaryDirectory() as tmp,patch.object(m,'OUT',Path(tmp)),patch.object(m,'design',side_effect=capture):
            m.estimate('test',1,'2014-01',max_initial_p=3,allow_fallback=False,do_diagnostics=False,run_bootstrap=False)
        self.assertEqual(calls,[3,3,3,3])

    def test_zero_covid_column_removed_after_calendar_mask(self):
        y,X=m.design(q=3,p=1,start='2013-10',mask_months=pd.period_range('2020-03','2021-12',freq='M'))
        self.assertNotIn('covid_affected_window',X.columns)
        self.assertEqual(np.linalg.matrix_rank(X),X.shape[1])

if __name__=='__main__':unittest.main()
