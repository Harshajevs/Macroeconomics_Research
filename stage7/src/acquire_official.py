"""Archive the documented MoSPI guest API, preserving every response page."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/source_downloads'

def fetch_cpi():
    params = dict(base_year='2012', level='Group', series='Current',
                  year=','.join(map(str, range(2013, 2026))), state_code='99',
                  sector_code='2', group_code='0,1,2,3,4,5,6',
                  subgroup_code='0.99,1.99,2.99,3.99,4.99,5.99,6.99', limit=100)
    url = 'https://api.mospi.gov.in/api/cpi/getCPIData'
    records, log, pages, total = [], [], 1, None
    page = 1
    while page <= pages:
        target = RAW / f'urban_cpi_api_page_{page:02d}.json'
        query = dict(params, page=page)
        if target.exists():
            payload = target.read_bytes()
            request_url = requests.Request('GET', url, params=query).prepare().url
        else:
            response = requests.get(url, params=query, timeout=60)
            response.raise_for_status()
            payload, request_url = response.content, response.url
            target.write_bytes(payload)
            time.sleep(.3)
        obj = json.loads(payload)
        assert obj['statusCode'] is True, obj
        meta = obj['meta_data']
        assert meta['page'] == page
        pages = meta['totalPages']
        if total is None: total = meta['totalRecords']
        assert total == meta['totalRecords'], 'Dataset changed during pagination'
        records.extend(obj['data'])
        log.append(dict(file=target.name, url=request_url,
                        sha256=hashlib.sha256(payload).hexdigest(), metadata=meta))
        print(f'Archived CPI page {page}/{pages}: {len(obj["data"])} records', flush=True)
        page += 1
    assert len(records) == total
    (RAW / 'urban_cpi_records.json').write_text(json.dumps(records, indent=2))
    (RAW / 'urban_cpi_requests.json').write_text(json.dumps(dict(
        retrieval_date='2026-11-21', retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        schema='cpi_api_v2_schema.yaml', pages=log, total_records=total), indent=2))
    return records

if __name__ == '__main__': fetch_cpi()
