import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for args in [['scripts/build.py'],['scripts/check.py'],['-m','unittest','discover','-s','tests','-v']]:
    subprocess.run([sys.executable,*args],cwd=ROOT,check=True)
