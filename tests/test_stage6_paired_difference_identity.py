import unittest
import numpy as np

class TestPairedDifferenceIdentity(unittest.TestCase):
    def test_ols_slope_difference_equals_difference_regression(self):
        rng=np.random.default_rng(4552026); n=27; u=rng.normal(size=n)
        h=1.0-0.10*u+rng.normal(size=n)
        c=0.8-0.18*u+0.8*rng.normal(size=n)
        X=np.column_stack([np.ones(n),u]); inv=np.linalg.inv(X.T@X)
        b_h=inv@(X.T@h); b_c=inv@(X.T@c); b_d=inv@(X.T@(c-h))
        self.assertAlmostEqual(float(b_d[1]),float(b_c[1]-b_h[1]),places=12)

if __name__=='__main__': unittest.main()
