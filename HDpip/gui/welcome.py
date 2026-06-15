"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是欢迎页面。
"""

import difflib
from typing import *
import pathlib
import locale
import tkinter.filedialog
import json

import maliang
import maliang.core.configs
import maliang.theme
import maliang.animation
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

try:
    from .. import core
    from .. import main
except ImportError:
    import sys
    sys.path.append(str(base_dir))
    import core
    import main

try:
    from . import base
except ImportError:
    import base

class LanguageCanvas(maliang.Canvas):
    """
    语言选择画布，用于显示语言选择界面。
    """

    def chose(self, index: int) -> None:
        """
        选择语言，`self.option`的回调函数。

        :param self: `LanguageCanvas`类
        :param index: 索引
        :type index: int
        """

        self.data_manager.setting["language"] = self.language_code_list[index]

    def renderOption(self, position: tuple[int, int] = (800, -400)) -> None:
        """
        渲染选项按钮。

        :param self: `LanguageCanvas`类
        :param position: 位置
        :type position: tuple[int, int]
        """

        self.language_list = []
        self.language_code_list = []
        for i in self.data_manager.language_dict:
            try:
                self.language_list.append(self.data_manager.language_code_dict[i])
            except KeyError:
                self.language_list.append(i)
            self.language_code_list.append(i)
        self.option = maliang.OptionButton(self, position, (250, 80), fontsize = 30, text = self.language_list, anchor = "center", command = self.chose, auto_update = True)

    def import_(self):
        """
        导入语言，`self.import_button`的回调函数。

        :param self: `LanguageCanvas`类
        """

        file = pathlib.Path(tkinter.filedialog.askopenfilename(filetypes = [("语言文件 Language file", ".json"), ("所有文件 All files", ".*")], title = "选择一个语言文件以导入 Chose a language file to import", initialdir = core.base.getBaseDir())).resolve()
        if file.is_file():
            self.data_manager.importLanguage(file)
            self.option.destroy()
            self.renderOption((800, 250))

    def __init__(self, master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.data_manager = data_manager

        self.tip = maliang.Text(self, (400, -400), (600, 200), text = "选择一个语言\nSelect a language", fontsize = 40, anchor = "center", auto_update = True)
        self.renderOption()
        local_language = locale.getdefaultlocale()[0]
        possible_language = difflib.get_close_matches(local_language, self.language_code_list, n = 1)
        if len(possible_language) > 0:
            self.option.set(self.language_code_list.index(possible_language[0]))
            self.data_manager.getLanguage(possible_language[0])
        maliang.animation.MoveWidget(self.tip, (0, 650), 1000, controller = maliang.animation.rebound, fps = 60).start()
        maliang.animation.MoveWidget(self.option, (0, 650), 1000, controller = maliang.animation.ease_out, fps = 60).start()

        self.card = base.RoundedRectangle(self, (600, -400), (800, 100), outline = base.primary, anchor = "center")
        maliang.animation.MoveWidget(self.card, (0, 850), 1000, controller = maliang.animation.smooth, fps = 60).start()
        self.import_tip = maliang.Text(self, (-400, 450), (600, 100), text = "没有您的语言？\nHaven't found your language?", fontsize = 30, anchor = "center", auto_update = True)
        self.import_tip.style.set(fg = base.primary)
        maliang.animation.MoveWidget(self.import_tip, (840, 0), 1000, controller = maliang.animation.ease_out, fps = 60).start(delay = 1000)
        self.import_button = base.Button(self, (1600, 450), (300, 50), text = "导入语言 Import language", theme = "outline-primary", anchor = "center", command = self.import_, auto_update = True)
        maliang.animation.MoveWidget(self.import_button, (-780, 0), 1000, controller = maliang.animation.rebound, fps = 60).start(delay = 1000)

class LicenseCanvas(maliang.Canvas):
    """
    许可画布。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `LicenseCanvas`类
        """

        self.tip.set(self.data_manager.language["welcome", "license_tip"])

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `LicenseCanvas`类
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

        :param self: `LicenseCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def command(self, agree: bool) -> None:
        self.data_manager.setting["license"] = True
        self.master.button_canvas.next_button.disable(not agree)

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

        self.license = base.ScrolledText(self)
        text = (core.base.getBaseDir() / "LICENSE").read_text(encoding = "utf-8")
        self.license.delete(1.0, tkinter.END)
        self.license.insert(1.0, text)
        self.license.tag_configure("center", justify = "center")
        self.license.tag_add("center", "1.0", "end")
        self.license.configure(state = tkinter.DISABLED)
        self.license.place(x = 600, y = -500, width = 1000, height = 500, anchor = "center")
        maliang.animation.MoveTkWidget(self.license, (0, 800), 1000, controller = maliang.animation.rebound, fps = 60).start(delay = 500)

        self.tip = maliang.Text(self, (600, -200), (300, 50), fontsize = 40, anchor = "center")
        self.checkbox = maliang.CheckBox(self, (200, -200), length = 50, default = False, command = self.command, anchor = "center")
        maliang.animation.MoveWidget((self.tip, self.checkbox), (0, 800), 1000, controller = maliang.animation.smooth, fps = 60).start(delay = 1000)

        self.renderLanguage()

class ThemeCanvas(maliang.Canvas):
    """
    主题画布。
    """

    def renderLanguage(self, option_position: tuple[int, int] = (800, 350)) -> None:
        """
        渲染语言。

        :param self: `ThemeCanvas`类
        :param option_position: 选项位置
        :type position: tuple[int, int]
        """

        self.tip.set(self.data_manager.language["welcome", "theme_tip"])
        try:
            self.option.destroy()
        except AttributeError:
            pass
        self.option = maliang.OptionButton(self, option_position, (250, 80), fontsize = 30, text = self.data_manager.language["welcome", "theme_list"], command = self.command, anchor = "center", auto_update = True)
        if isinstance(self.value, int):
            self.option.set(self.value)

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `LicenseCanvas`类
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

        :param self: `LicenseCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def command(self, index: int):
        theme_list = ["system", "light", "dark"]
        self.data_manager.setting["theme"] = theme_list[index]
        maliang.theme.set_color_mode(theme_list[index])
        self.value = index

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
        self.value: int = None

        self.tip = maliang.Text(self, (400, -400), (600, 200), fontsize = 40, anchor = "center", auto_update = True)
        self.renderLanguage((800, -400))
        maliang.animation.MoveWidget(self.tip, (0, 750), 1000, controller = maliang.animation.rebound, fps = 60).start()
        maliang.animation.MoveWidget(self.option, (0, 750), 1000, controller = maliang.animation.ease_out, fps = 60).start()

class InfoCanvas(maliang.Canvas):
    """
    信息画布。
    """

    def renderLanguage(self, option_position: tuple[int, int] = (800, 350)) -> None:
        """
        渲染语言。

        :param self: `ThemeCanvas`类
        :param option_position: 选项位置
        :type position: tuple[int, int]
        """

        self.tip.set(self.data_manager.language["welcome"]["info_tip"])
        self.treeview.treeview.heading("item", text = self.data_manager.language["welcome"]["item"])
        self.treeview.treeview.heading("value", text = self.data_manager.language["welcome"]["value"])

        info_data = [
            core.base.getSystemVersion(),
            str(core.base.getPythonVersion()),
            str(core.base.getPythonPath()),
            str(core.base.getPipVersion()),
            core.pip_api.pip_head,
            str(core.base.getVersion())
        ]
        self.treeview.treeview.delete(*self.treeview.treeview.get_children())
        for i in range(0, len(info_data)):
            self.treeview.treeview.insert("", "end", values = (self.data_manager.language["welcome"]["info_treeview"][i], info_data[i]))

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `LicenseCanvas`类
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

        :param self: `LicenseCanvas`类
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

        self.tip = maliang.Text(self, (600, -200), (300, 50), fontsize = 40, anchor = "center")
        self.treeview = base.Treeview(self, (600, -400), (1000, 500), columns = ("item", "value"), show = "headings", selectmode = "extended", anchor = "center")
        self.treeview.treeview.column("item", width = 250, minwidth = 60)
        self.treeview.treeview.column("value", width = 650, minwidth = 60)
        self.renderLanguage()
        maliang.animation.MoveWidget(self.tip, (0, 250), 1000, controller = maliang.animation.rebound, fps = 60).start()
        maliang.animation.MoveTkWidget(self.treeview, (0, 750), 1000, controller = maliang.animation.smooth, fps = 60).start(delay = 500)

class EndCanvas(maliang.Canvas):
    """
    结束画布。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `EndCanvas`类
        """

        self.tip.set(self.data_manager.language["welcome", "end_tip"])
        self.button.set(self.data_manager.language["welcome", "end_button"])

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `EndCanvas`类
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

        :param self: `EndCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def command(self, *argvs, **kargvs):
        self.button.disable(True)
        self.master.button_canvas.back_button.disable(True)
        self.scrolled_text.configure(state = tkinter.NORMAL)
        self.scrolled_text.delete(1.0, tkinter.END)
        self.scrolled_text.insert(tkinter.END, self.data_manager.language["welcome", "auto_setting"])
        auto_setting = base_dir / ("setting/auto." + str(self.data_manager.setting["language"]) + ".json")
        if auto_setting.is_file():
            auto_setting_data = json.load(auto_setting.open("r", encoding = "utf-8"))
            self.data_manager.setting += auto_setting_data
        self.scrolled_text.insert(tkinter.END, self.data_manager.language["welcome", "done"])
        self.scrolled_text.insert(tkinter.END, "\n")
        self.scrolled_text.insert(tkinter.END, self.data_manager.language["welcome", "save_setting"])
        self.data_manager.setting.save()
        self.scrolled_text.insert(tkinter.END, self.data_manager.language["welcome", "done"])
        self.scrolled_text.insert(tkinter.END, "\n")
        self.scrolled_text.configure(state = tkinter.DISABLED)
        maliang.animation.MoveWidget(
            (
                self.master.button_canvas.back_button, 
                self.master.button_canvas.next_button
            ), 
            (0, 200), 1000, controller = maliang.animation.smooth, fps = 60
        ).start()
        def _() -> None:
            import sys
            import subprocess
            self.master.master.master.destroy()
            subprocess.Popen(
                [sys.executable, str(base_dir / "main.py")],
                stdin = subprocess.DEVNULL,
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL,
                creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
        self.after(1000, _)

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

        self.tip = maliang.Text(self, (600, -200), (600, 40), fontsize = 40, anchor = "center", auto_update = True)
        self.scrolled_text = base.ScrolledText(self, state = tkinter.DISABLED)
        self.scrolled_text.place(x = 600, y = -400, width = 1000, height = 500, anchor = "center")
        self.button = base.Button(self, (600, 800), (250, 50), theme = "outline-primary", anchor = "center")
        self.button.bind("<Button-1>", self.command)
        maliang.animation.MoveWidget(self.tip, (0, 250), 1000, controller = maliang.animation.ease_out, fps = 60).start()
        maliang.animation.MoveTkWidget(self.scrolled_text, (0, 750), 1000, controller = maliang.animation.rebound, fps = 60).start(delay = 500)
        maliang.animation.MoveWidget(self.button, (0, -150), 1000, controller = maliang.animation.rebound, fps = 60).start()

        self.renderLanguage()
        self.after(2000, self.renderLanguage)

class ContentCanvas(maliang.Canvas):
    """
    内容画布，包含欢迎页面的主要内容区域。
    """

    def __init__(self, master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.data_manager = data_manager
        self.button_canvas: ButtonCanvas = None
        self.canvas_index = 0
        self.canvas_list = []
        self.canvas_guide = [
            LanguageCanvas,
            LicenseCanvas,
            ThemeCanvas,
            InfoCanvas,
            EndCanvas
        ]
        for _ in range(0, len(self.canvas_guide)):
            self.canvas_list.append("uninited")

    def switchCanvas(self, index: int) -> None:
        """
        切换至指定画布。

        :param self: `ContentCanvas`类
        :param index: 索引
        :type index: int
        """

        if index == 0:
            self.button_canvas.back_button.disable()
            self.button_canvas.next_button.disable(False)
        elif index == len(self.canvas_guide) - 1:
            self.button_canvas.back_button.disable(False)
            self.button_canvas.next_button.disable()
        else:
            self.button_canvas.back_button.disable(False)
            self.button_canvas.next_button.disable(False)
        if self.canvas_list[index] == "uninited":
            self.canvas_list[index] = self.canvas_guide[index](self, self.data_manager)
            self.canvas_list[index].place(x = index * 1200, y = 0, width = 1200, height = 700)
        if index == 1:
            self.button_canvas.next_button.disable(not self.canvas_list[1].checkbox.get())
        maliang.animation.MoveTkWidget(self, ((self.canvas_index - index) * 1200, 0), 500, controller = maliang.animation.smooth, fps = 60).start()
        self.canvas_index = index

    def walkCanvas(self, index: int) -> None:
        """
        相对步进画布。

        :param self: `ContentCanvas`类
        :param index: 索引
        :type index: int
        """

        self.switchCanvas(self.canvas_index + index)

class ButtonCanvas(maliang.Canvas):
    """
    按钮画布，包含欢迎页面的底部按钮区域。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `ButtonCanvas`类
        """

        self.back_button.set(self.data_manager.language["welcome", "back_button"])
        self.next_button.set(self.data_manager.language["welcome", "next_button"])

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `ButtonCanvas`类
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

        :param self: `ButtonCanvas`类
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
        data_manager.language.registerEvent(self.onLanguageChange)
        self.content_canvas: ContentCanvas = None
        self.button: base.Button = None
        self.back_button: base.Button = None
        self.next_button: base.Button = None

    def start(self) -> None:
        """
        启动按钮画布的动画效果。

        :param self: `ButtonCanvas`类
        """

        self.button_bar = self.create_rectangle(0, 0, 1200, 100, outline = "")
        def _() -> None:
            def _() -> None:
                def _() -> None:
                    def back() -> None:
                        content_canvas.walkCanvas(-1)
                    def next() -> None:
                        content_canvas.walkCanvas(1)
                    back_button = self.back_button = base.Button(self, (100, 150), (100, 50), theme = "outline-light", text = "上一步", anchor = "center", command = back)
                    next_button = self.next_button = base.Button(self, (1100, 150), (100, 50), theme = "outline-light", text = "下一步", anchor = "center", command = next)
                    self.content_canvas.destroy()
                    content_canvas = self.content_canvas = ContentCanvas(self.master, self.data_manager)
                    content_canvas.button_canvas = self
                    content_canvas.place(x = 0, y = 0, width = 1200 * len(content_canvas.canvas_list), height = 700)
                    content_canvas.switchCanvas(0)
                    maliang.animation.MoveWidget((back_button, next_button), (0, -100), 500, controller = maliang.animation.smooth, fps = 60).start(delay = 250)
                maliang.animation.MoveTkWidget(self.content_canvas, (0, -1000), 1000, controller = maliang.animation.ease_in, end = _, fps = 60).start()
                maliang.animation.MoveElement(self.button, (0, 200), 500, controller = maliang.animation.smooth, end = self.button.destroy, fps = 60).start()

            self.button = base.Button(self, (600, 50), (400, 50), theme = "outline-light", text = "让我们开始吧！ Let's begin!", anchor = "center", command = _)
            self.configure(bg = base.primary)
            maliang.theme.register_event(lambda _: self.configure(bg = base.primary))
            self.delete(self.button_bar)
        maliang.animation.GradientItem(self, self.button_bar, "fill", (base.light, base.primary), 500, controller = maliang.animation.smooth, fps = 60, end = _).start(delay = 2500)


class Welcome(maliang.Tk):
    """
    欢迎窗口，HDpip的主欢迎界面。
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
        base.WindowFadeOut(self, 500, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()

    def __init__(self, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__((1200, 800), title = data_manager.language["program_name"] + "(" + data_manager.language["program_subname"] + ")")
        base.WindowFadeIn(self, 500, controller = maliang.animation.smooth, fps = 60).start()
        self.icon_ = maliang.PhotoImage(file = str(core.base.getBaseDir() / "asset" / "image" / "icon.png"))
        self.iconphoto(True, self.icon_)
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True
        self.center()
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        self.data_manager.language.registerEvent(self.onLanguageChange)

        self.root_canvas = maliang.Canvas(self, expand = "xy", auto_zoom = True, auto_update = True)
        self.root_canvas.place(width = 1200, height = 800, x = 0, y = 0)
        self.content_canvas = maliang.Canvas(self.root_canvas, expand = "xy", auto_zoom = True, auto_update = True)
        self.content_canvas.place(width = 1200, height = 700, x = 0, y = 0)
        self.button_canvas = ButtonCanvas(self.root_canvas, self.data_manager)
        self.button_canvas.content_canvas = self.content_canvas
        self.button_canvas.place(width = 1200, height = 100, x = 0, y = 700)

        self.icon_show = maliang.Image(self.content_canvas, (600, 1000), (256, 256), image = self.icon_, anchor = "center")
        maliang.animation.MoveWidget(self.icon_show, (0, 350 - 1000), 1000, controller = maliang.animation.rebound, fps = 60).start()
        self.title_ = maliang.Text(self.content_canvas, (600, 1000), (1200, 50), text = "寒冬pip(HDpip)", fontsize = 40, weight = "bold", anchor = "center")
        maliang.animation.MoveWidget(self.icon_show, (0, 200 - 350), 500, controller = maliang.animation.smooth, fps = 60).start(delay = 1250)
        maliang.animation.MoveWidget(self.title_, (0, 400 - 1000), 500, controller = maliang.animation.smooth, fps =60).start(delay = 1250)
        self.subtitle_ = maliang.Text(self.content_canvas, (600, 1000), (1200, 50), text = "一个基于马良框架的pip GUI\nA pip GUI based on maliang", fontsize = 30, anchor = "center")
        maliang.animation.MoveWidget(self.subtitle_, (0, 500 - 1000), 500, controller = maliang.animation.smooth, fps = 60).start(delay = 1500)
        self.button_canvas.start()

if __name__ == "__main__":
    Welcome().mainloop()
