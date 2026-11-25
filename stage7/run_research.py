"""Offline reproduction from archived official sources; never writes a report."""
from pathlib import Path
import subprocess,sys,argparse
ROOT=Path(__file__).resolve().parents[1]

def run(args):
    print('RUN',*args,flush=True)
    subprocess.run([sys.executable,*args],cwd=ROOT,check=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--full',action='store_true',help='Also redo high-draw bootstrap and recursive calibration (several minutes)');a=p.parse_args()
    run(['stage7/src/prepare_inputs.py'])
    run(['-m','unittest','discover','-s','stage7/tests','-v'])
    for script in ['analyse_phillips.py','analyse_food_variance.py','audit_legacy_variants.py','audit_mutations.py','state_feasibility.py']:
        run(['stage7/src/'+script])
    if a.full:
        run(['stage7/src/audit_spillover.py','--mode','refresh'])
        run(['stage7/src/audit_spillover.py','--mode','calibrate','--reps','1000','--inner','999'])
        run(['src/stage6_aggregate_null_size_simulation.py','--reps','2000','--seed','45520261118','--output','stage7/results/phillips_design_null_calibration_reproduced.csv'])
    run(['stage7/src/build_checkpoint.py'])
    print('Offline reproduction finished. No report or LaTeX draft created.')

if __name__=='__main__':main()
