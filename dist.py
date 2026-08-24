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

base_dir = pathlib.Path(__file__).parent.resolve()

def clean() -> None:
    """
    清理旧的构建产物。
    """

    for name in ["build", "dist", "hdpip.egg-info"]:
        shutil.rmtree(base_dir / name, ignore_errors = True)

def copy() -> None:
    for name in ["README.md", "LICENSE.txt"]:
        if (base_dir / name).is_file():
            shutil.copy2(base_dir / name, base_dir / "HDpip" / name)

def main() -> int:
    """
    清理并构建 sdist 与 wheel。

    :return: 运行状态
    :rtype: int
    """

    clean()
    copy()
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation"]
    )
    return completed.returncode

if __name__ == "__main__":
    raise SystemExit(main())
