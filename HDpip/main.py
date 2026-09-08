"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是主文件。
"""

from typing import *

import maliang.theme
import maliang.core.configs

try:
    from . import core
    from . import gui
except ImportError:
    import core
    import gui

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
    if needWelcome(data_manager):
        gui.welcome.Welcome(data_manager).mainloop()
    else:
        maliang.theme.set_color_mode(data_manager.setting["theme"])
        gui.main.Main().mainloop()

if __name__ == "__main__":
    main()
