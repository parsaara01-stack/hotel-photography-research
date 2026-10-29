"""Bounded structural checks, not scientific or privacy certification."""
import csv
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/evidence.json').read_text())
assert rows and len({r['id'] for r in rows})==len(rows)
assert all(r['access_depth'] in ['full_text','abstract'] for r in rows)
assert all(r['sample_n'] is None or (type(r['sample_n']) is int and r['sample_n']>0) for r in rows)
assert all(r['url'].startswith('https://') and r['source_locator'] and r['retrieved_at_utc'] for r in rows)
with (ROOT/'data/evidence.csv').open() as f:csvrows=list(csv.DictReader(f))
assert [r['id'] for r in rows]==[r['id'] for r in csvrows]
manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
assert {r['id'] for r in manifest}=={r['id'] for r in rows}
assert all(r['sha256'] is None or re.fullmatch('[a-f0-9]{64}',r['sha256']) for r in manifest)
with (ROOT/'data/study_matrix.csv').open() as f:studies=list(csv.DictReader(f))
assert studies and len({r['study_id'] for r in studies})==len(studies)
assert all(r['publication_id'] in {p['id'] for p in rows} for r in studies)
assert all(r['appraisal'] and r['extraction_review'] for r in studies)
assert json.loads((ROOT/'data/search_log.json').read_text())['queries']
release=json.loads((ROOT/'data/release.json').read_text())
assert release['status']=='demo_only' and release['protocol_version']=='0.2' and release['schema_version']==2
for asset in json.loads((ROOT/'data/image_inventory.json').read_text()):
    assert asset['research_ready'] is False
    if asset['asset']:assert hashlib.sha256((ROOT/asset['asset']).read_bytes()).hexdigest()==asset['sha256']
for p in (ROOT/'data').iterdir():
    if p.suffix in ['.json','.csv']:assert p.read_bytes()==(ROOT/'docs/data'/p.name).read_bytes(),p
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
p=Links();html=(ROOT/'docs/index.html').read_text();p.feed(html)
assert len(set(p.ids))==len(p.ids)
for ref in p.refs:
    if ref.startswith('#'):assert ref=='#' or ref[1:] in p.ids,ref
    elif not ref.startswith(('https:','mailto:','data:')):assert (ROOT/'docs'/ref.split('#')[0]).exists(),ref
js=(ROOT/'docs/app.js').read_text()
for forbidden in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','document.cookie']:
    assert forbidden not in js,forbidden
assert "data_kind:'demo'" in js and "environment:'public_demo'" in js
assert "protocol_version:'0.2'" in js and 'name="atmosphere"' not in html
assert 'What Can Room Photos Tell Us?' in html and "connect-src 'none'" in html
assert 'AI-GENERATED EDITORIAL IMAGE' in html
assert 'not a study property or experimental stimulus' in html
assert 'room-cover.jpg' not in js and 'room-detail.jpg' not in js, 'Editorial illustrations must not enter demo stimuli'
print('PASS: data structure/mirrors, demo release lock, local references, asset digest and limited transport/storage string checks. Not research/privacy certification.')
