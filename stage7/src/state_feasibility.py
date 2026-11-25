"""Offline source-feasibility assessment; does not estimate a state panel."""
from pathlib import Path
import re,json,logging
import pandas as pd
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=ROOT/'data/source_downloads';logging.getLogger('pypdf').setLevel(logging.ERROR)
    reader=PdfReader(raw/'plfs_old_design_2024.pdf')
    text=reader.pages[58].extract_text(extraction_mode='layout')
    assert '3RSE' in text and 'age group: 15 years and above' in text and 'urban' in text
    rows=[]
    for line in text.splitlines():
        match=re.match(r'^([A-Za-z &-]+?)\s{2,}([0-9].*)$',line.strip())
        if not match:continue
        nums=re.findall(r'\d+\.\d+',match[2])
        if len(nums)!=15:continue
        for i,q in enumerate(['2023Q4','2024Q1','2024Q2','2024Q3','2024Q4']):
            rows.append(dict(state=match[1].strip(),quarter=q,ur_person_rse_pct=float(nums[3*i+2]),source='PLFS Oct-Dec2024 Table3RSE age15+ Urban; PDFpage59 printedB-8'))
    d=pd.DataFrame(rows);d.to_csv(ROOT/'data/processed/state_rse_2023Q4_2024Q4_feasibility.csv',index=False)
    s=d[~d.state.isin(['all-India','Jammu & Kashmir'])].ur_person_rse_pct
    assert len(s)==105
    summary=dict(candidate_states=21,cells=len(s),median=float(s.median()),max=float(s.max()),min=float(s.min()),above20=int((s>20).sum()),at_or_above25=int((s>=25).sum()),scope='Five-quarter feasibility slice only; not full27quarter RSE coverage')
    (ROOT/'results/state_panel_feasibility_rse.json').write_text(json.dumps(summary,indent=2))
    records=json.loads((raw/'plfs_states_records.json').read_text());pl=pd.DataFrame(records)
    assert len(pl)==621
    pl.to_csv(ROOT/'data/processed/plfs_state_ur_api_feasibility_UNVALIDATED.csv',index=False)
    print('State panel retained as future extension; 621 API records archived; 105 candidate state-quarter RSE cells inspected. No panel estimates or validated full panel claimed.')

if __name__=='__main__':main()
