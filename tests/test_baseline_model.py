"""Structural smoke tests for active post-results v3.3 estimates."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'/'model_results'

def main():
    summary=pd.read_csv(OUT/'postreview_model_comparison_summary.csv')
    assert len(summary)==20
    assert summary['block_wild_bootstrap_tail_probability'].between(0,1).all()
    core=pd.read_csv(OUT/'postreview_core_q3_oct2013_model_summary.csv').iloc[0]
    assert int(core['q'])==3 and int(core['n'])==147
    assert 0 <= core['wild_block_bootstrap_wald_tail_probability'] <= 1
    assert core['primary_comparable_delayed_sum_CI_low'] <= core['primary_comparable_delayed_sum'] <= core['primary_comparable_delayed_sum_CI_high']
    base=pd.read_csv(OUT/'postreview_primary_q3_oct2013_model_summary.csv').iloc[0]
    assert int(base['q'])==3 and int(base['final_selected_p']) in range(7)
    assert int(base['n'])==147
    assert 0 <= base['HAC6_joint_chi2_p'] <= 1
    assert base['primary_comparable_delayed_sum_CI_low'] <= base['primary_comparable_delayed_sum'] <= base['primary_comparable_delayed_sum_CI_high']
    coef=pd.read_csv(OUT/'postreview_primary_q3_oct2013_coefficients.csv')
    assert {'x0','x_l1','x_l2','x_l3'}.issubset(set(coef.term))
    assert (OUT/'postreview_primary_q3_oct2013_initial_bic_candidates.csv').exists()
    assert (OUT/'postreview_primary_q3_oct2013_recursive_coefficients.csv').exists()
    assert (OUT/'postreview_primary_q3_oct2013_influence.csv').exists()
    assert (OUT/'postreview_primary_q3_oct2013_leave_out_checks.csv').exists()
    assert (OUT/'bidirectional_granger_style_summary.csv').exists()
    print('ALL POST-REVIEW BASELINE OUTPUT TESTS PASSED')
    print('These tests validate output structure and software behaviour, not causal identification.')
if __name__=='__main__': main()
