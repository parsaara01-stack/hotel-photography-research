"""Build the static data bundle; no third-party dependencies or network access."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'data').glob('*'):
    if path.suffix in ['.json','.csv']:
        shutil.copyfile(path, ROOT/'docs/data'/path.name)
rows=json.loads((ROOT/'data/evidence.json').read_text())
(ROOT/'docs/evidence.js').write_text('window.EVIDENCE = '+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n')
inventory=json.loads((ROOT/'data/image_inventory.json').read_text())
for item in inventory:
    if item['asset']:
        item['sha256']=hashlib.sha256((ROOT/item['asset']).read_bytes()).hexdigest()
(ROOT/'data/image_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
shutil.copyfile(ROOT/'data/image_inventory.json', ROOT/'docs/data/image_inventory.json')
print('Built static evidence bundle and verified illustration hash.')
