import os
import sys

os.environ.setdefault("PYTHONUTF8", "1")

if len(sys.argv) > 1:
    os.system(f"twine upload dist/* -u __token__ -p {sys.argv[1]}")
else:
    os.system("twine upload dist/* --config-file pypirc.pypirc")
