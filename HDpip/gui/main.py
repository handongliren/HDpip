"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是主文件。
"""

from typing import *
from typing_extensions import override
import pathlib

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

class AboutCanvas(custom.containers.Canvas):
    """
    关于画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.title.set(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ")")
        self.description.set(self.data_manager.language["main", "description"])

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.image = maliang.Image(self, ss((25, 25)), ss((50, 50)), image = self.winfo_toplevel().icon_)
        self.title = maliang.Text(self, ss((100, 25)), None, anchor = "w", fontsize = ss(32))
        self.version = maliang.Text(self, ss((100, 75)), None, anchor = "w", fontsize = ss(30), text = core.system.getVersion())
        self.version.style.set(fg = custom.color.primary)
        self.description = maliang.Text(self, ss((25, 125)), None, anchor = "w", fontsize = ss(25))

        self.renderLanguage()

class ControlCanvas(custom.containers.Canvas):
    """
    控制画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.install_button.set(self.data_manager.language["main", "install_button"])
        self.uninstall_button.set(self.data_manager.language["main", "uninstall_button"])
        self.upgrade_button.set(self.data_manager.language["main", "upgrade_button"])
        self.setting_button.set(self.data_manager.language["main", "setting_button"])

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.install_button = custom.widgets.Button(self, ss((40, 40)), ss((120, 60)), theme = "outline-success", icon = bi("box-seam"), fontsize = ss(30))
        self.uninstall_button = custom.widgets.Button(self, ss((190, 40)), ss((120, 60)), theme = "outline-danger", icon = bi("trash"), fontsize = ss(30))
        self.upgrade_button = custom.widgets.Button(self, ss((40, 140)), ss((120, 60)), theme = "outline-primary", icon = bi("arrow-up"), fontsize = ss(30))
        self.setting_button = custom.widgets.Button(self, ss((190, 140)), ss((120, 60)), theme = "outline-secondary", icon = bi("gear"), fontsize = ss(30))

        self.renderLanguage()

class MirrorCanvas(custom.containers.Canvas):
    """
    镜像画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.title.set(self.data_manager.language["main", "mirror"])
        self.switch_button.set(self.data_manager.language["main", "switch_button"])
        self.auto_switch_button.set(self.data_manager.language["main", "auto_switch_button"])
        self.view_button.set(self.data_manager.language["main", "view_button"])
        self.copy_button.set(self.data_manager.language["main", "copy_button"])
        self.copy_pip_button.set(self.data_manager.language["main", "copy_pip_button"])

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.create_rectangle(ss((0, 0, 350, 50)), fill = custom.color.primary, outline = "")
        self.title = maliang.Text(self, ss((10, 0)), None, anchor = "nw", fontsize = ss(30))
        self.title.style.set(fg = custom.color.white)
        self.switch_button = custom.widgets.Button(self, ss((340, 25)), ss((80, 30)), anchor = "e", theme = "outline-light", icon = bi("toggles"), fontsize = ss(20))
        self.auto_switch_button = custom.widgets.Button(self, ss((250, 25)), ss((120, 30)), anchor = "e", theme = "outline-light", icon = bi("arrow-repeat"), fontsize = ss(20))

        self.text = maliang.Text(self, ss((20, 65)), None, fontsize = ss(20))
        self.view_button = custom.widgets.Button(self, ss((250, 65)), ss((80, 30)), theme = "outline-default", icon = bi("eye"), fontsize = ss(20))
        self.copy_button = custom.widgets.Button(self, ss((20, 110)), ss((80, 30)), theme = "outline-primary", icon = bi("clipboard"), fontsize = ss(20))
        self.copy_pip_button = custom.widgets.Button(self, ss((130, 110)), ss((200, 30)), theme = "primary", icon = bi("clipboard-data"), fontsize = ss(20))

        self.renderLanguage()

class Main(custom.containers.Tk):
    """
    主窗口。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.wm_title(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ")")

    @override
    def __init__(self, data_manager: core.data.DataManager = core.data.data_manager):
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(ss((1200, 800)), title = "寒冬pip(HDpip)", data_manager = data_manager, icon = str(core.system.getBaseDir() / "assets" / "image" / "icon.png"))
        self.icon_ = maliang.PhotoImage(file = str(core.system.getBaseDir() / "assets" / "image" / "icon.png"))
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True

        self.base_canvas = maliang.Canvas(self, expand = "xy", auto_zoom = True, auto_update = True)
        self.base_canvas.place(x = 0, y = 0, width = ss(1200), height = ss(800))

        self.about_canvas = AboutCanvas(self.base_canvas, data_manager)
        self.about_canvas.place(x = 0, y = 0, width = ss(350), height = ss(150))
        self.about_canvas.create_line(ss((0, 150, 350, 150)), width = 2, fill = custom.color.gray_500)

        self.control_canvas = ControlCanvas(self.base_canvas, data_manager)
        self.control_canvas.place(x = 0, y = ss(150), width = ss(350), height = ss(240))
        self.control_canvas.create_line(ss((0, 240, 350, 240)), width = 2, fill = custom.color.gray_500)

        self.mirror_canvas = MirrorCanvas(self.base_canvas, data_manager)
        self.mirror_canvas.place(x = 0, y = ss(390), width = ss(350), height = ss(160))
        self.mirror_canvas.create_line(ss((0, 159, 350, 159)), width = 2, fill = custom.color.gray_500)

        self.base_canvas.create_line(ss((350, 0, 350, 800)), width = 2, fill = custom.color.gray_500)
        self.base_canvas.create_line(ss((700, 0, 700, 800)), width = 2, fill = custom.color.gray_500)
        self.base_canvas.create_line(ss((0, 540, 350, 540)), width = 2, fill = custom.color.gray_500)
        self.base_canvas.create_line(ss((700, 400, 1200, 400)), width = 2, fill = custom.color.gray_500)
        self.renderLanguage()

if __name__ == "__main__":
    import subprocess
    subprocess.Popen(
        [sys.executable, str(base_dir / "main.py")],
        stdin = subprocess.DEVNULL,
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL,
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
