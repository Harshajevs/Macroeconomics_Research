from pathlib import Path
import shutil
base=Path.cwd();src=base/'work/report_revision';out=base/'outputs/hs455_report_revised'
out.mkdir(exist_ok=True)
for name in ['report.tex','make_figures.py','make_tables.py','verify_report.py','numerical_audit.json','report_verification.json','HS455_Report.pdf']:
 shutil.copy2(src/name,out/name)
for folder in ['assets','tables','research_data']:
 shutil.copytree(src/folder,out/folder,dirs_exist_ok=True)
print('Revised report delivery folder prepared.')
