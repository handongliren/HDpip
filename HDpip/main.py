"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是主文件。
"""

from typing import *


import maliang.theme
import maliang.core.configs
import maliang.animation
import maliang.core.virtual

try:
    from . import core
    from . import gui
    from .gui.base import ss
except ImportError:
    import core
    import gui
    from gui.base import ss

def needWelcome(data_manager: core.base.DataManager = core.base.DataManager()) -> bool:
    """
    返回是否需要进行欢迎引导。

    :param data_manager: 数据管理器
    :type data_manager: core.base.DataManager
    :return: 是否需要
    :rtype: bool
    """

    if not data_manager.isInited():
        return True
    else:
        data_manager.init()
        if not data_manager.setting["license"]:
            return True

class AboutCanvas(maliang.Canvas):
    """
    关于画布。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `AboutCanvas`类
        """

        self.title.set(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ")")
        self.description.set(self.data_manager.language["main"]["description"])

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `AboutCanvas`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `AboutCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def __init__(self, master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.data_manager = data_manager
        self.data_manager.language.registerEvent(self.onLanguageChange)

        self.image = maliang.Image(self, (ss(25), ss(25)), (ss(50), ss(50)), image = self.winfo_toplevel().icon_)
        self.title = maliang.Text(self, (ss(100), ss(25)), None, anchor = "w", fontsize = ss(32))
        self.version = maliang.Text(self, (ss(100), ss(75)), None, anchor = "w", fontsize = ss(30), text = core.base.getVersion())
        self.version.style.set(fg = gui.base.primary)
        self.description = maliang.Text(self, (ss(25), ss(125)), None, anchor = "w", fontsize = ss(22))

        self.renderLanguage()

class ControlCanvas(maliang.Canvas):
    """
    控制画布。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `ControlCanvas`类
        """

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `ControlCanvas`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `ControlCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def __init__(self, master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.data_manager = data_manager
        self.data_manager.language.registerEvent(self.onLanguageChange)

        self.install_button = gui.base.Button(self, ss((40, 40)), ss((120, 60)), theme = "outline-success", text = self.data_manager.language["main"]["install_button"], fontsize = ss(30))
        self.uninstall_button = gui.base.Button(self, ss((190, 40)), ss((120, 60)), theme = "outline-danger", text = self.data_manager.language["main"]["uninstall_button"], fontsize = ss(30))
        self.upgrade_button = gui.base.Button(self, ss((40, 140)), ss((120, 60)), theme = "outline-primary", text = self.data_manager.language["main"]["upgrade_button"], fontsize = ss(30))
        self.setting_button = gui.base.Button(self, ss((190, 140)), ss((120, 60)), theme = "outline-secondary", text = self.data_manager.language["main"]["setting_button"], fontsize = ss(30))

        self.renderLanguage()

class Main(maliang.Tk):
    """
    主窗口。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `Welcome`类
        """

        self.wm_title(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ") - " + self.data_manager.language["welcome", "title"])

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `Welcome`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `Welcome`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        gui.base.WindowFadeOut(self, 250, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()

    def __init__(self, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__((ss(1200), ss(800)), title = "寒冬pip(HDpip)")
        gui.base.WindowFadeIn(self, 250, controller = maliang.animation.smooth, fps = 60).start()
        self.icon_ = maliang.PhotoImage(file = str(core.base.getBaseDir() / "asset" / "image" / "icon.png"))
        self.iconphoto(True, self.icon_)
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True
        self.center()
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        self.data_manager.language.registerEvent(self.onLanguageChange)

        self.base_canvas = maliang.Canvas(self, expand = "xy", auto_zoom = True, auto_update = True)
        self.base_canvas.place(x = 0, y = 0, width = ss(1200), height = ss(800))
        self.about_canvas = AboutCanvas(self.base_canvas, data_manager)
        self.about_canvas.place(x = 0, y = 0, width = ss(350), height = ss(150))
        self.about_canvas.create_line(ss((0, 149, 350, 149)), width = 1, fill = gui.base.gray_500)

        self.control_canvas = ControlCanvas(self.base_canvas, data_manager)
        self.control_canvas.place(x = 0, y = ss(150), width = ss(350), height = ss(240))
        self.control_canvas.create_line(ss((0, 240, 350, 240)), width = 1, fill = gui.base.gray_500)
        self.base_canvas.create_line(ss((0, 390, 350, 390)), width = 1, fill = gui.base.gray_500)

        self.base_canvas.create_line(ss((350, 0, 350, 800)), width = 1, fill = gui.base.gray_500)
        self.base_canvas.create_line(ss((700, 0, 700, 800)), width = 1, fill = gui.base.gray_500)
        self.base_canvas.create_line(ss((0, 540, 350, 540)), width = 1, fill = gui.base.gray_500)
        self.base_canvas.create_line(ss((700, 400, 1200, 400)), width = 1, fill = gui.base.gray_500)

@gui.error_catcher.catch
def main(data_manager: core.base.DataManager = core.base.DataManager()) -> None:
    """
    主函数。

    :param data_manager: 数据管理器
    :type data_manager: core.base.DataManager
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
