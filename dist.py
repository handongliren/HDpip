"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

构建分发包脚本。
"""

import pathlib
import shutil
import subprocess
import sys

def clean() -> None:
    """清理旧的构建产物。"""

    for name in ["build", "dist", "hdpip.egg-info"]:
        shutil.rmtree(name, ignore_errors = True)

def main() -> int:
    """清理并构建 sdist 与 wheel。"""

    clean()
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation"]
    )
    return completed.returncode

if __name__ == "__main__":
    raise SystemExit(main())
