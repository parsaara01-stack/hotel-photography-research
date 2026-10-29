import argparse
import functools
import http.server
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Build, verify and serve the static protocol/demo.')
parser.add_argument('--port',type=int,default=8769)
args=parser.parse_args()
subprocess.run([sys.executable,str(ROOT/'scripts/verify.py')],check=True)
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'docs'))
server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),handler)
print(f'Protocol/demo: http://127.0.0.1:{args.port}',flush=True)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
