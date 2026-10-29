"""Meaningful release and data-integrity checks, with no external dependencies."""
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/evidence.json').read_text())
assert len(rows)==6 and len({r['id'] for r in rows})==6
assert sum(r['access_depth']=='full_text' for r in rows)==3
assert sum(r['access_depth']=='abstract' for r in rows)==3
assert all(r['sample_n'] is None or (type(r['sample_n']) is int and r['sample_n']>0) for r in rows)
assert all(r['url'].startswith('https://') and r['source_locator'] and r['retrieved_at_utc'] for r in rows)
manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
assert {r['id'] for r in manifest}=={r['id'] for r in rows}
for r in manifest:
    assert r['sha256'] is None or re.fullmatch('[a-f0-9]{64}',r['sha256'])
assert json.loads((ROOT/'data/release.json').read_text())['status']=='demo_only'
for asset in json.loads((ROOT/'data/image_inventory.json').read_text()):
    assert asset['research_ready'] is False
    if asset['asset']: assert hashlib.sha256((ROOT/asset['asset']).read_bytes()).hexdigest()==asset['sha256']
for p in (ROOT/'data').iterdir():
    if p.suffix in ['.json','.csv']: assert p.read_bytes()==(ROOT/'docs/data'/p.name).read_bytes(),p
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
p=Links();p.feed((ROOT/'docs/index.html').read_text())
assert len(set(p.ids))==len(p.ids),'Duplicate HTML IDs'
for ref in p.refs:
    if ref.startswith('#'):assert ref=='#' or ref[1:] in p.ids,ref
    elif not ref.startswith(('https:','mailto:','data:')):assert (ROOT/'docs'/ref.split('#')[0]).exists(),ref
js=(ROOT/'docs/app.js').read_text()
for forbidden in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','document.cookie','data_kind:\'observed\'']:
    assert forbidden not in js,forbidden
assert "data_kind:'demo'" in js and "environment:'public_demo'" in js
assert all((ROOT/'docs'/name).exists() for name in ['index.html','styles.css','app.js','evidence.js'])
print('PASS: evidence access/missingness, mirrors, rights/hash gate, release lock, local links and no demo transport/storage.')
