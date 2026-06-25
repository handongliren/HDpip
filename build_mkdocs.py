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

    site_dir = root / "site"
    if site_dir.exists():
        shutil.rmtree(site_dir)

    commands = [
        [sys.executable, "-m", "mkdocs", "build", "-f", "mkdocs.yml"],
        [sys.executable, "-m", "mkdocs", "build", "-f", "docs/en/mkdocs.yml"],
    ]

    print(f"Using token from {token_file}")
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        completed = subprocess.run(cmd, cwd = root, check = False)
        if completed.returncode != 0:
            return completed.returncode

    return 0

if __name__ ==  "__main__":
    raise SystemExit(main())
