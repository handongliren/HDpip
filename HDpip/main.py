"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是主文件。
"""

from typing import *

import pathlib

if __name__ == "__main__" and __package__ is None:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    __package__ = "HDpip"

import maliang.theme
import maliang.core.configs

from . import core
from . import gui

def needWelcome(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    返回是否需要进行欢迎引导。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否需要
    :rtype: bool
    """

    if not data_manager.isInited():
        return True
    else:
        data_manager.init()
        if not data_manager.setting["license"]:
            return True

@gui.error_catcher.catch
def main(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    主函数。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    maliang.core.configs.Env.system = "Windows11"
    maliang.core.configs.Env.auto_update = True
    gui.upgrade.cleanupCopy(data_manager)
    if needWelcome(data_manager):
        gui.welcome.Welcome(data_manager).mainloop()
        return
    gui.upgrade.checkAndUpdate(data_manager)
    maliang.theme.set_color_mode(data_manager.setting["theme"])
    gui.main.Main().mainloop()

if __name__ == "__main__":
    main()
