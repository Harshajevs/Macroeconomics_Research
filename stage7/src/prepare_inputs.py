"""Validate new official Urban CPI and reconcile PLFS before estimation."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent
sys.path.insert(0,str(PROJECT/'src'))
import validate_stage6_urban_cpi as legacy_validator

NAMES=['General','Food and Beverages','Pan, Tobacco and Intoxicants',
       'Clothing and Footwear','Housing','Fuel and Light','Miscellaneous']
SHORT=['headline','food_bev','pan_tobacco','clothing','housing','fuel_light','misc']
WEIGHTS=dict(zip(SHORT[1:],[.3629,.0136,.0557,.2167,.0558,.2953]))

def main():
    raw=ROOT/'data/source_downloads';processed=ROOT/'data/processed'
    records=json.loads((raw/'urban_cpi_records.json').read_text())
    d=pd.DataFrame(records)
    for field,expected in [('baseyear','2012'),('state','All India'),('sector','Urban')]:
        assert d[field].astype(str).eq(expected).all(),(field,expected)
    assert set(d.group)==set(NAMES)
    assert d.subgroup.eq(d.group+'-Overall').all()
    d['month_id']=pd.to_datetime(d.year.astype(str)+'-'+d.month,format='%Y-%B').dt.to_period('M')
    assert not d.duplicated(['month_id','group']).any()
    wide=d.pivot(index='month_id',columns='group',values='index').loc[:,NAMES].astype(float)
    wide.columns=SHORT
    assert wide.index.equals(pd.period_range('2013-01','2025-12',freq='M'))
    assert np.isfinite(wide.to_numpy()).all()
    wide.to_csv(processed/'urban_cpi_levels.csv',index_label='month')

    # Anchor values are extracted from separately published press-release tables,
    # not copied from the API. The raw HTML and original PDF are included.
    anchors=[];requests=json.loads((raw/'anchor_requests.json').read_text())
    for month in ['2017-01','2018-12','2019-12','2021-12','2023-12']:
        table=pd.read_csv(raw/f'anchor_{month}_table.csv',dtype=str)
        col=8 if month in ['2017-01','2019-12'] else 7
        values=[]
        general=table[table.iloc[:,0].str.contains('General Index',na=False)].iloc[0]
        values.append(float(general.iloc[col]))
        for group in range(1,7):
            row=table[table.iloc[:,0].eq(str(group))].iloc[0]
            values.append(float(row.iloc[col]))
        anchors.append(dict(month=month,**dict(zip(legacy_validator.INDEX_FIELDS,values)),
                            source_document=f'Archived PIB release table, {month}',source_url=requests[month]))
    technical='https://www.mospi.gov.in/sites/default/files/press_release/CPI%20Technical%20Note%20on%20Imputation.pdf'
    for month,values in [('2020-04',[150.9,156.1,179.1,150.4,155.6,137.1,142.5]),
                         ('2020-05',[150.6,154.8,183.4,150.8,155.6,136.2,143.0]),
                         ('2024-12',[192.,209.4,212.2,187.8,181.7,170.5,182.])]:
        anchors.append(dict(month=month,**dict(zip(legacy_validator.INDEX_FIELDS,values)),
            source_document='MoSPI technical note Table1' if month.startswith('2020') else 'MoSPI February2025 release AnnexureI December2024 final',
            source_url=technical if month.startswith('2020') else 'https://www.mospi.gov.in/sites/default/files/press_release/CPI_PR_12Feb25.pdf'))
    pd.DataFrame(anchors).to_csv(processed/'urban_cpi_independent_anchors.csv',index=False)
    digest=hashlib.sha256((raw/'urban_cpi_records.json').read_bytes()).hexdigest()
    intake=[]
    for month,row in wide.iterrows():
        metadata=dict(month=str(month),sector='Urban',base_year='2012',series='Current',state_coverage='All India',
            source_document='Archived MoSPI CPI API v2, 11 complete response pages',
            source_url='https://api.mospi.gov.in/api/cpi/getCPIData',retrieval_date='2026-11-21',export_date='2026-11-21',
            filter_settings='base_year=2012;level=Group;series=Current;state_code=99;sector_code=2;years2013-2025',
            month_status='final',raw_source_sha256=digest,
            source_status_codes='|'.join(d.loc[d.month_id==month,'status'].tolist()))
        metadata.update(dict(zip(legacy_validator.INDEX_FIELDS,row.tolist())))
        metadata.update(legacy_validator._expected_imputation_flags(str(month)))
        intake.append(metadata)
    pd.DataFrame(intake).to_csv(processed/'urban_cpi_validated_intake.csv',index=False)
    report=legacy_validator.validate_rows(intake,anchors,expected_raw_sha256=digest)
    report['status_note']='API F/F*/F+ preserved; historical final vintage, with explicit technical-note macro-imputation flags. F+ is not reinterpreted as macro-imputation.'
    report['early_2013_housing_actual_values']=wide.loc['2013-01':'2013-05','housing'].tolist()
    report['early_2013_note']='Observed Current-query source contains 100.3,100.4,100.4,100.5,100.5; inherited statement that every value equals100 is not used. No back-series splice. Shorter STL history sensitivity is required.'
    (ROOT/'results/cpi_validation.json').write_text(json.dumps(report,indent=2))

    pl=pd.DataFrame(json.loads((raw/'plfs_aggregate_api.json').read_text())['data'])
    for field,value in [('state','All India'),('sector','urban'),('gender','person'),('AgeGroup','15 years and above'),('frequency','Quarterly')]:
        assert pl[field].eq(value).all()
    qmap={'Jan-Mar':1,'Apr-Jun':2,'Jul-Sep':3,'Oct-Dec':4}
    pl['quarter_id']=pl.year.astype(str)+'Q'+pl.quarter.map(qmap).astype(str)
    pl['ur_api']=pl.value.astype(float)
    old=pd.read_csv(PROJECT/'data/raw/plfs_urban_quarterly_ur_2018_2024.csv')
    joined=old.merge(pl[['quarter_id','ur_api']],on='quarter_id',validate='one_to_one',how='outer',indicator=True)
    assert joined['_merge'].eq('both').all()
    mismatch=joined.loc[joined.ur_cws_15plus_person_pct!=joined.ur_api]
    # The archived bulletin pages were inspected directly: Statement5, PDF page9
    # in each 2019 bulletin. API discrepancies must never overwrite these values.
    expected={'2019Q2':(8.8,21.6),'2019Q3':(8.3,8.1)}
    assert set(mismatch.quarter_id)==set(expected)
    for _,row in mismatch.iterrows():
        assert (row.ur_cws_15plus_person_pct,row.ur_api)==expected[row.quarter_id]
    joined['selected_ur']=joined.ur_cws_15plus_person_pct
    joined['resolution']=np.where(joined.quarter_id.isin(expected),
        'Use published Statement5 age15+ person value; source PDF page9 directly checked; API discrepancy retained',
        'API agrees exactly with bulletin transcription')
    joined.to_csv(processed/'plfs_api_bulletin_reconciliation.csv',index=False)
    pd.DataFrame({'quarter':joined.quarter_id,'unemployment':joined.selected_ur}).to_csv(processed/'urban_unemployment.csv',index=False)
    # The freeze is made after source validation and before ANY new Phillips regression.
    manifest=[]
    for directory in [raw,processed]:
        for p in sorted(directory.glob('*')):
            if p.is_file():manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT)))
    frozen=ROOT/'documentation/pre_estimation_input_manifest.sha256'
    if frozen.exists():
        # Preserve the original pre-estimation snapshot on offline reproduction.
        for line in frozen.read_text().splitlines():
            expected,name=line.split('  ',1)
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    else:frozen.write_text('\n'.join(manifest)+'\n')
    print(f'PASS: {len(wide)} CPI months; {report["anchor_comparisons"]} anchor cells; maximum composite gap {report["group_composite_max_abs_residual"]:.5f}; 25/27 PLFS API values match and two documented discrepancies resolved from bulletins.')

if __name__=='__main__':main()
