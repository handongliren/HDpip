"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是更新器。
"""

from typing import *
from typing_extensions import override
import pathlib

import maliang.theme
import maliang.core.configs
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

try:
    from .. import core
except ImportError:
    import sys
    sys.path.append(str(base_dir))
    import core

try:
    from . import custom
    from .custom.util import ss
    from .custom.media import bi
except ImportError:
    import custom
    from custom.util import ss
    from custom.media import bi

def checkUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    检查是否有更新。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否有更新
    :rtype: bool
    """

    data_manager.init()
    current_version = core.system.getVersion()
    latest_version = core.pip_api.getLatestVersion("hdpip")

    return current_version < latest_version

class ConfirmCanvas(custom.containers.Canvas):
    """
    确认画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.tip.set(self.data_manager.language["upgrade", "tip"].format(
            current_version = core.system.getVersion(), 
            latest_version = core.pip_api.getLatestVersion("hdpip")
        ))
        self.note_button.set(self.data_manager.language["upgrade", "note_button"])
        self.confirm_button.set(self.data_manager.language["upgrade", "confirm_button"])
        self.delay_next_button.set(self.data_manager.language["upgrade", "delay_next_button"])
        self.delay_week_button.set(self.data_manager.language["upgrade", "delay_week_button"])

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        初始化确认画布。

        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.tip = maliang.Text(self, ss((300, 75)), None, anchor = "center", justify = "center", fontsize = ss(30))
        self.note_button = custom.widgets.Button(self, ss((300, 200)), ss((300, 50)), anchor = "center", theme = "outline-primary")
        self.confirm_button = custom.widgets.Button(self, ss((150, 275)), ss((200, 50)), anchor = "center", theme = "primary")
        self.delay_next_button = custom.widgets.Button(self, ss((450, 275)), ss((200, 50)), anchor = "center", theme = "outline-warning")
        self.delay_week_button = custom.widgets.Button(self, ss((300, 350)), ss((300, 50)), anchor = "center", theme = "outline-danger")

        self.renderLanguage()

class Upgrade(custom.containers.Tk):
    """
    更新窗口。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.quickTitle(self.data_manager.language["upgrade", "title"])

    @override
    def __init__(self, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(ss((600, 400)), data_manager = data_manager, icon = str(base_dir / "assets" / "image" / "icon.png"))
        self.icon_ = maliang.PhotoImage(file = str(base_dir / "assets" / "image" / "icon.png"))
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True

        self.confirm_canvas = ConfirmCanvas(self, data_manager = data_manager)
        self.confirm_canvas.place(width = ss(600), height = ss(400), x = 0, y = 0)

        self.renderLanguage()

if __name__ == "__main__":
    Upgrade().mainloop()
