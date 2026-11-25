from pathlib import Path
import shutil
ROOT=Path.cwd()
SRC=ROOT/'work/report_draft'
OUT=ROOT/'outputs/hs455_report'
RESEARCH=ROOT/'outputs/hs455_research/stage7'
OUT.mkdir(exist_ok=True)
for f in ['report.tex','cover_details.tex','make_figures.py','make_tables.py']:
    shutil.copy2(SRC/f,OUT/f)
for dirname in ['assets','tables']:
    (OUT/dirname).mkdir(exist_ok=True)
    for p in (SRC/dirname).iterdir():
        if p.suffix in {'.pdf','.png','.tex'}: shutil.copy2(p,OUT/dirname/p.name)
for name in ['make_figures.py','make_tables.py']:
    p=OUT/name
    p.write_text(p.read_text().replace("DATA=BASE.parents[1]/'outputs/hs455_research/stage7'", "DATA=BASE/'research_data'").replace("'quarterly_core_Dec2024'", "'monthly_core_Dec2024'"))
files=['data/processed/phillips_yoy_log_matched.csv','data/processed/phillips_qoq_saar_matched.csv','data/processed/urban_cpi_levels.csv','data/processed/urban_unemployment.csv',
'results/official_headline_variance_allocations.csv','results/unemployment_leverage.csv','results/phillips_all_specifications.csv','results/spillover_recursive_calibration.csv','results/primary_phillips_comparison.csv','results/primary_food_variance_summary.csv','results/spillover_effect_intervals.csv','results/spillover_high_precision_bootstrap.csv','results/phillips_descriptive_statistics.csv','results/food_variance_block_uncertainty.csv','documentation/source_register.csv','documentation/claim_ledger.csv']
for sector in ['combined','urban']:
    for frequency in ['MoM_raw','YoY_raw']:
        files.append(f'data/processed/{sector}_{frequency}_exact_contributions.csv')
for f in files:
    dest=OUT/'research_data'/f
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(RESEARCH/f,dest)
print('Portable report source prepared:',OUT)
