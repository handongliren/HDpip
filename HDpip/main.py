"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是主文件。
"""

from typing import *
from typing_extensions import override


import maliang.theme
import maliang.core.configs
import maliang.core.virtual

try:
    from . import core
    from . import gui
    from .gui.custom.util import ss
    from .gui.custom.media import bi
except ImportError:
    import core
    import gui
    from gui.custom.util import ss
    from gui.custom.media import bi

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

class AboutCanvas(gui.custom.containers.Canvas):
    """
    关于画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.title.set(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ")")
        self.description.set(self.data_manager.language["main"]["description"])

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
        self.version.style.set(fg = gui.custom.color.primary)
        self.description = maliang.Text(self, ss((25, 125)), None, anchor = "w", fontsize = ss(25))

        self.renderLanguage()

class ControlCanvas(gui.custom.containers.Canvas):
    """
    控制画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.install_button = gui.custom.widgets.Button(self, ss((40, 40)), ss((120, 60)), theme = "outline-success", text = self.data_manager.language["main"]["install_button"], icon = bi("box-seam"), fontsize = ss(30))
        self.uninstall_button = gui.custom.widgets.Button(self, ss((190, 40)), ss((120, 60)), theme = "outline-danger", text = self.data_manager.language["main"]["uninstall_button"], icon = bi("trash"), fontsize = ss(30))
        self.upgrade_button = gui.custom.widgets.Button(self, ss((40, 140)), ss((120, 60)), theme = "outline-primary", text = self.data_manager.language["main"]["upgrade_button"], icon = bi("arrow-up"), fontsize = ss(30))
        self.setting_button = gui.custom.widgets.Button(self, ss((190, 140)), ss((120, 60)), theme = "outline-secondary", text = self.data_manager.language["main"]["setting_button"], icon = bi("gear"), fontsize = ss(30))

        self.renderLanguage()

class Main(gui.custom.containers.Tk):
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
        self.about_canvas.create_line(ss((0, 149, 350, 149)), width = 1, fill = gui.custom.color.gray_500)

        self.control_canvas = ControlCanvas(self.base_canvas, data_manager)
        self.control_canvas.place(x = 0, y = ss(150), width = ss(350), height = ss(240))
        self.control_canvas.create_line(ss((0, 240, 350, 240)), width = 1, fill = gui.custom.color.gray_500)
        self.base_canvas.create_line(ss((0, 390, 350, 390)), width = 1, fill = gui.custom.color.gray_500)

        self.base_canvas.create_line(ss((350, 0, 350, 800)), width = 1, fill = gui.custom.color.gray_500)
        self.base_canvas.create_line(ss((700, 0, 700, 800)), width = 1, fill = gui.custom.color.gray_500)
        self.base_canvas.create_line(ss((0, 540, 350, 540)), width = 1, fill = gui.custom.color.gray_500)
        self.base_canvas.create_line(ss((700, 400, 1200, 400)), width = 1, fill = gui.custom.color.gray_500)
        self.renderLanguage()

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
        Main().mainloop()

if __name__ == "__main__":
    main()
