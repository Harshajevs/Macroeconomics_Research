"""Inject audit-listed defects into an in-memory legacy module; never edit it."""
from pathlib import Path
import sys,unittest,types,io,json,warnings
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
import test_legacy_inference_protection as tests

def main():
    source=(ROOT.parent/'src/estimate_baseline.py').read_text();original=tests.m
    mutations={
        'null_not_imposed':('restricted_X = X.drop(columns=terms).to_numpy(dtype=float)','restricted_X = X.to_numpy(dtype=float)'),
        'wrong_bootstrap_bandwidth':('stat = hac_wald_statistic(ystar, full_X, R, nlags=block_length)','stat = hac_wald_statistic(ystar, full_X, R, nlags=0)'),
        'plus_one_removed':('(1 + exceed) / (1 + successful) if successful else np.nan','exceed / successful if successful else np.nan'),
        'gaussian_multipliers':('signs[max(0, start):min(n, start + block_length)] = rng.choice([-1.0, 1.0])','signs[max(0, start):min(n, start + block_length)] = rng.normal()'),
        'bootstrap_interval_reversed':("f'{prefix}_bootstrap_t_CI_low': theta - qhi * observed_se,\n        f'{prefix}_bootstrap_t_CI_high': theta - qlo * observed_se,","f'{prefix}_bootstrap_t_CI_low': theta - qlo * observed_se,\n        f'{prefix}_bootstrap_t_CI_high': theta - qhi * observed_se,"),
        'varying_candidate_covid_window':('covid_lag_horizon=max(q, max_initial_p)','covid_lag_horizon=max(q, p)'),
        'zero_column_removal_disabled':('X_out = X_out.drop(columns=zero_cols)','X_out = X_out')}
    rows=[]
    for name,(before,after) in [('baseline',(None,None)),*mutations.items()]:
        if before is not None:assert source.count(before)>=1,name
        code=source if before is None else source.replace(before,after,1)
        mod=types.ModuleType('mutant');mod.__file__=str(ROOT.parent/'src/estimate_baseline.py')
        exec(compile(code,mod.__file__,'exec'),mod.__dict__);tests.m=mod
        stream=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromTestCase(tests.LegacyInferenceProtection)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',FutureWarning)
            result=unittest.TextTestRunner(stream=stream).run(suite)
        killed=not result.wasSuccessful()
        rows.append(dict(mutation=name,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),killed=killed if before else None))
        assert result.wasSuccessful() if name=='baseline' else killed,name
        tests.m=original
    (ROOT/'results/inference_mutation_matrix.json').write_text(json.dumps(rows,indent=2))
    print('Baseline5/5 pass; all7 targeted inference/selection mutants killed. Legacy file unchanged.')

if __name__=='__main__':main()
