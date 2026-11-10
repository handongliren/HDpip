"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是包执行入口。
"""

import sys

from . import gui
from .main import main

if __name__ == "__main__":
    if "--updater" in sys.argv:
        gui.upgrade.runUpdater("--silent" in sys.argv)
    else:
        main()
