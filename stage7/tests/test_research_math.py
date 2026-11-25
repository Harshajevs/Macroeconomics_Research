import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from research_math import quarterly_average, slope_fit, exact_contributions, covariance_shares

class ResearchMath(unittest.TestCase):
    def test_quarter_requires_three_actual_months(self):
        x = pd.DataFrame({'a': [100., np.nan, 102., 103., 104., 105.]},
                         index=pd.period_range('2020-01', periods=6, freq='M'))
        q = quarterly_average(x)
        self.assertTrue(np.isnan(q.iloc[0, 0]))
        self.assertAlmostEqual(q.iloc[1, 0], 104.)
        self.assertTrue(np.isnan(q.diff().iloc[1, 0]))

    def test_paired_slope_identity_with_trend_and_common_rows(self):
        rng = np.random.default_rng(15)
        u = rng.normal(size=30); time = np.arange(30)
        a = 3 - .7*u + .03*time + rng.normal(size=30)
        b = 2 - 1.2*u + .01*time + rng.normal(size=30)
        h, c, d = [slope_fit(y, u, time, trend=True) for y in (a, b, b-a)]
        self.assertAlmostEqual(c['slope']-h['slope'], d['slope'], places=12)

    def test_calendar_hac_does_not_bridge_excluded_quarters(self):
        time = np.array([0, 1, 4, 5, 6, 9, 10, 11])
        u = np.array([2., 1, 4, 3, 2, 1, 2, 3])
        y = np.array([1., 2, 2, 4, 1, 3, 2, 1])
        r = slope_fit(y, u, time, hac_lag=1)
        X = np.column_stack([np.ones(len(u)),u]); inv=np.linalg.inv(X.T@X)
        e=y-X@np.linalg.lstsq(X,y,rcond=None)[0]; scores=X*e[:,None]
        meat=scores.T@scores
        for i in range(len(time)):
            for j in range(i+1,len(time)):
                if time[j]-time[i]==1:
                    cross=np.outer(scores[i],scores[j]); meat += .5*(cross+cross.T)
        expected=inv@meat@inv*len(u)/(len(u)-2)
        self.assertAlmostEqual(r['se'],np.sqrt(expected[1,1]),places=12)

    def test_hc3_matches_statsmodels(self):
        rng=np.random.default_rng(5);u=rng.normal(size=27);y=rng.normal(size=27)
        r=slope_fit(y,u,np.arange(27),hc3=True)
        expected=sm.OLS(y,sm.add_constant(u)).fit().get_robustcov_results(cov_type='HC3')
        self.assertAlmostEqual(r['se'],expected.bse[1],places=12)

    def test_official_headline_exact_accounting_has_residual(self):
        groups=pd.DataFrame({'food':[100.,110.,108.,120.], 'other':[100.,102.,105.,107.]})
        h=pd.Series([100.,107.,107.,115.])
        c,total=exact_contributions(groups,h,{'food':.4,'other':.6},lag=1)
        np.testing.assert_allclose(c.sum(axis=1),total)
        self.assertGreater(np.abs(c['aggregation_residual']).max(),.1)
        self.assertAlmostEqual(covariance_shares(c,total).sum(),100.,places=10)

    def test_no_silent_missing_input_in_regression(self):
        with self.assertRaises(ValueError):
            slope_fit([1.,np.nan,3.],[2.,1.,4.],[0,1,2])

if __name__=='__main__': unittest.main()
