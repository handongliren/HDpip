import os
import subprocess
import sys
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
token_file = root / "GitHub Pages.token"

def load_token() -> str:
    """Read GH_TOKEN from the token file if it is not already set in the environment."""
    token = os.environ.get("GH_TOKEN", "").strip()
    if token:
        return token

    if token_file.exists():
        return token_file.read_text(encoding = "utf-8").strip()

    raise FileNotFoundError(f"Token file not found: {token_file}")

def main() -> int:
    token = load_token()
    os.environ["GH_TOKEN"] = token

    shutil.rmtree(root / "site")
    cmd = [sys.executable, "-m", "mkdocs", "build", "-f", "mkdocs.yml"]
    cmd = [sys.executable, "-m", "mkdocs", "build", "-f", "docs/en/mkdocs.yml"]
    print(f"Using token from {token_file}")
    completed = subprocess.run(cmd, cwd = root, check = False)
    return completed.returncode

if __name__ ==  "__main__":
    raise SystemExit(main())
