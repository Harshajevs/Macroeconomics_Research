import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
import estimate_baseline as m
from fast_bootstrap import Design

class FastBootstrap(unittest.TestCase):
    def test_exact_legacy_wald_and_rng_tail(self):
        y,X=m.design(q=3,p=1,start='2013-10')
        terms=['x_l1','x_l2','x_l3'];R=m.restriction_matrix(list(X.columns),terms)
        engine=Design(X,R);stat=engine.statistics(y)[0][0]
        self.assertAlmostEqual(stat,m.hac_wald_statistic(y,X,R),places=9)
        a=engine.bootstrap(y,[list(X.columns).index(k) for k in terms],reps=199,seed=22)
        b=m.wild_block_bootstrap_wald(y,X,terms,stat,reps=199,seed=22)['wild_block_bootstrap_wald_tail_probability']
        self.assertEqual(a,b)
        hc3=m.fit_model(y,X).get_robustcov_results(cov_type='HC3')
        self.assertAlmostEqual(engine.statistics(y,kind='HC3')[0][0],float(hc3.wald_test(R,use_f=False,scalar=True).statistic),places=9)

if __name__=='__main__':unittest.main()
