"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是GUI基础轮子，~~屎山2号💩~~。
"""

from typing import *
import ctypes
import ctypes.util
import os
import platform
import tkinter
import tkinter.scrolledtext
import tkinter.ttk

import darkdetect
import maliang
import maliang.theme
import maliang.animation
import maliang.standard.shapes
import maliang.core.virtual

blue = primary = "#0d6efd"
indigo = "#6610f2"
purple = "#6f42c1"
pink = "#d63384"
red = danger = "#dc3545"
orange = "#fd7e14"
yellow = warning = "#ffc107"
green = success = "#198754"
teal = "#20c997"
cyan = info = "#0dcaf0"
black = "#000"
white = "#fff"
gray = "#6c757d"
gray_dark = "#343a40"
gray_100 = light = "#f8f9fa"
gray_200 = "#e9ecef"
gray_300 = "#dee2e6"
gray_400 = "#ced4da"
gray_500 = "#adb5bd"
gray_600 = secondary = "#6c757d"
gray_700 = "#495057"
gray_800 = "#343a40"
gray_900 = dark = "#212529"

primary_subtle = "#6e9efe"
secondary_subtle = "#8e9499"
success_subtle = "#4da37c"
info_subtle = "#6ee5f8"
warning_subtle = "#ffe083"
danger_subtle = "#e86a76"
light_subtle = gray_300
dark_subtle = gray_700

colors = {
    "primary": [primary, primary_subtle],
    "secondary": [secondary, secondary_subtle],
    "success": [success, success_subtle],
    "info": [info, info_subtle],
    "warning": [warning, warning_subtle],
    "danger": [danger, danger_subtle],
    "light": [light, light_subtle],
    "dark": [dark, dark_subtle]
}

def getSystemDpi() -> float:
    """
    跨平台获取系统 DPI。

    :return: 当前系统 DPI，默认返回 96
    :rtype: float
    """

    system = platform.system().lower()

    if system == "windows":
        try:
            user32 = ctypes.windll.user32
            hdc = user32.GetDC(None)
            if hdc:
                dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
                dpi_y = ctypes.windll.gdi32.GetDeviceCaps(hdc, 90)
                user32.ReleaseDC(None, hdc)
                if dpi_x and dpi_y:
                    return float(dpi_x)
        except Exception:
            pass

    elif system == "darwin":
        try:
            core_graphics = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreGraphics"))
            core_graphics.CGMainDisplayID.restype = ctypes.c_uint32
            core_graphics.CGDisplayScreenSize.argtypes = [ctypes.c_uint32]

            class CGSize(ctypes.Structure):
                _fields_ = [("width", ctypes.c_double), ("height", ctypes.c_double)]

            core_graphics.CGDisplayScreenSize.restype = CGSize
            core_graphics.CGDisplayPixelsWide.argtypes = [ctypes.c_uint32]
            core_graphics.CGDisplayPixelsWide.restype = ctypes.c_size_t
            core_graphics.CGDisplayPixelsHigh.argtypes = [ctypes.c_uint32]
            core_graphics.CGDisplayPixelsHigh.restype = ctypes.c_size_t

            display_id = core_graphics.CGMainDisplayID()
            size = core_graphics.CGDisplayScreenSize(display_id)
            if size.width > 0 and size.height > 0:
                width = core_graphics.CGDisplayPixelsWide(display_id)
                height = core_graphics.CGDisplayPixelsHigh(display_id)
                dpi_x = width * 25.4 / size.width
                dpi_y = height * 25.4 / size.height
                if dpi_x > 0 and dpi_y > 0:
                    return float((dpi_x + dpi_y) / 2.0)
        except Exception:
            pass
        return 96.0

    elif system == "linux":
        env_candidates = [
            os.environ.get("GDK_SCALE"),
            os.environ.get("QT_SCALE_FACTOR"),
            os.environ.get("Xft.dpi"),
        ]
        for value in env_candidates:
            if not value:
                continue
            try:
                scale = float(value)
                if scale > 0:
                    if "GDK_SCALE" in os.environ or "QT_SCALE_FACTOR" in os.environ:
                        return 96.0 * scale
                    return scale
            except Exception:
                pass
        return 96.0

    return 96.0

def pxToPt(px: float, dpi: float | None = None) -> float:
    """
    将像素大小转换为点数字号。

    :param px: 像素大小
    :type px: float
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | None
    :return: 对应的点数字号
    :rtype: float
    """

    if dpi is None:
        dpi = getSystemDpi()
    return px * 72.0 / dpi

def ptToPx(pt: float, dpi: float | None = None) -> float:
    """
    将点数字号转换为像素大小。

    :param pt: 点数字号
    :type pt: float
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | None
    :return: 对应的像素大小
    :rtype: float
    """

    if dpi is None:
        dpi = getSystemDpi()
    return pt * dpi / 72.0

class Button(maliang.Button):
    """
    继承自`maliang.Button`，添加了bootstrap配色，使用`theme`参数指定主题。
    """

    def switchTheme(
        self,
        theme: Literal[
            "default",
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark",
            "outline-default",
            "outline-primary",
            "outline-secondary",
            "outline-success",
            "outline-info",
            "outline-warning",
            "outline-danger",
            "outline-light",
            "outline-dark"
        ] = "default",
        disabled: bool = False
    ) -> None:
        """
        切换主题。

        :param self: `Button`类
        :param theme: 主题
        :type theme: Literal["default", "primary", "secondary", "success", "info", "warning", "danger", "light", "dark", "outline-default", "outline-primary", "outline-secondary", "outline-success", "outline-info", "outline-warning", "outline-danger", "outline-light", "outline-dark"]
        :param disabled: 是否为禁用状态
        :type disabled: bool
        """

        _ = theme.split("outline-")
        if len(_) == 1:
            color = _[0]
            outline = False
        elif len(_) == 2:
            color = _[1]
            outline = True

        if not disabled:
            if not outline:
                match color:
                    case "default":
                        self.style.set(
                            "light",
                            fg = (light, light, light_subtle),
                            bg = (dark, dark, dark_subtle),
                            ol = (dark, dark, dark_subtle)
                        )
                        self.style.set(
                            "dark",
                            fg = (dark, dark, dark_subtle),
                            bg = (light, light, light_subtle),
                            ol = (light, light, light_subtle)
                        )
                    case "light":
                        self.style.set(
                            fg = (dark, dark, dark_subtle),
                            bg = (light, light, light_subtle),
                            ol = (light, light, light_subtle)
                        )
                    case _:
                        self.style.set(
                            fg = (light, light, light_subtle),
                            bg = (colors[color][0], colors[color][0], colors[color][1]),
                            ol = (colors[color][0], colors[color][0], colors[color][1])
                        )
            else:
                match color:
                    case "default":
                        self.style.set(
                            "light",
                            fg = (dark, light, light_subtle),
                            bg = ("", dark, dark_subtle),
                            ol = (dark, dark, dark_subtle)
                        )
                        self.style.set(
                            "dark",
                            fg = (light, dark, dark_subtle),
                            bg = ("", light, light_subtle),
                            ol = (light, light, light_subtle)
                        )
                    case "light":
                        self.style.set(
                            fg = (light, dark, dark_subtle),
                            bg = ("", light, light_subtle),
                            ol = (light, light, light_subtle)
                        )
                    case _:
                        self.style.set(
                            fg = (colors[color][0], light, light_subtle),
                            bg = ("", colors[color][0], colors[color][1]),
                            ol = (colors[color][0], colors[color][0], colors[color][1])
                        )
        else:
            if not outline:
                match color:
                    case "default":
                        self.style.set(
                            "light",
                            fg = light_subtle,
                            bg = dark_subtle,
                            ol = dark_subtle
                        )
                        self.style.set(
                            "dark",
                            fg = dark_subtle,
                            bg = light_subtle,
                            ol = light_subtle
                        )
                    case "light":
                        self.style.set(
                            fg = dark_subtle,
                            bg = light_subtle,
                            ol = light_subtle
                        )
                    case _:
                        self.style.set(
                            fg = light_subtle,
                            bg = colors[color][1],
                            ol = colors[color][1]
                        )
            else:
                match color:
                    case "default":
                        self.style.set(
                            "light",
                            fg = dark_subtle,
                            bg = "",
                            ol = dark_subtle
                        )
                        self.style.set(
                            "dark",
                            fg = light_subtle,
                            bg = "",
                            ol = light_subtle
                        )
                    case "light":
                        self.style.set(
                            fg = light_subtle,
                            bg = "",
                            ol = light_subtle
                        )
                    case _:
                        self.style.set(
                            fg = colors[color][1],
                            bg = "",
                            ol = colors[color][1]
                        )

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        theme: Literal[
            "default",
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark",
            "outline-default",
            "outline-primary",
            "outline-secondary",
            "outline-success",
            "outline-info",
            "outline-warning",
            "outline-danger",
            "outline-light",
            "outline-dark"
        ] = "default",
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: Literal['normal', 'bold'] = "normal",
        slant: Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: Literal["left", "center", "right"] = "left",
        command: Callable | None = None,
        image: maliang.toolbox.enhanced.PhotoImage | None = None,
        anchor: Literal["n", "e", "w", "s", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
        auto_update: bool | None = None,
        style: type[maliang.core.virtual.Style] | None = None,
    ):
        """
        :param self: `Button`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param position: 位置
        :type position: tuple[int, int]
        :param size: 大小
        :type size: tuple[int, int] | None
        :param theme: 主题
        :type theme: Literal["default", "primary", "secondary", "success", "info", "warning", "danger", "light", "dark", "outline-default", "outline-primary", "outline-secondary", "outline-success", "outline-info", "outline-warning", "outline-danger", "outline-light", "outline-dark"]
        :param text: 文本
        :type text: str
        :param family: 字体
        :type family: str | None
        :param fontsize: 字号
        :type fontsize: int | None
        :param weight: 字重
        :type weight: Literal['normal', 'bold']
        :param slant: 字形
        :type slant: Literal['roman', 'italic']
        :param underline: 下划线
        :type underline: bool
        :param overstrike: 重影
        :type overstrike: bool
        :param justify: 适应模式
        :type justify: Literal["left", "center", "right"]
        :param command: 绑定命令
        :type command: Callable | None
        :param image: 图片
        :type image: maliang.toolbox.enhanced.PhotoImage | None
        :param anchor: 锚点
        :type anchor: Literal["n", "e", "w", "s", "nw", "ne", "sw", "se", "center"]
        :param capture_events: 监听事件
        :type capture_events: bool | None
        :param gradient_animation: 过渡动画
        :type gradient_animation: bool | None
        :param auto_update: 自动更新
        :type auto_update: bool | None
        :param style: 样式
        :type style: type[maliang.core.virtual.Style] | None
        """

        super().__init__(
            master,
            position,
            size,
            text = text,
            family = family,
            fontsize = fontsize,
            weight = weight,
            slant = slant,
            underline = underline,
            overstrike = overstrike,
            justify = justify,
            command = command,
            image = image,
            anchor = anchor,
            capture_events = capture_events,
            gradient_animation = gradient_animation,
            auto_update = auto_update,
            style = style
        )
        self.theme = theme
        self.switchTheme(theme, False)
        self.update()

    def disable(self, value: bool = True) -> None:
        """
        修改`Button`类的禁用状态。

        :param self: `Button`类
        :param value: 是否禁用
        :type value: bool
        """

        self.switchTheme(self.theme, value)
        self.update("normal")
        super().disable(value)
        self.disabled = value

class ScrolledText(tkinter.scrolledtext.ScrolledText):
    """
    继承自`tkinter.scrolledtext.ScrolledText`，为`maliang`针对性地写了点代码，添加了明暗主题支持，优化了字体。

    ---
    *以下内容来自`tkinter.scrolledtext.ScrolledText`：*

    在父控件创建一个带有滚动条的文本块。
    """

    def switchTheme(self, theme: Literal["system", "light", "dark"] = "system") -> None:
        """
        切换主题。

        :param self: `Scrolled`类
        :param theme: 主题
        :type theme: Literal["system", "light", "dark"]
        """

        match theme:
            case "light":
                self.configure(bg = light, fg = dark, selectbackground = info, selectforeground = dark, insertbackground = dark)
            case "dark":
                self.configure(bg = dark, fg = light, selectbackground = primary, selectforeground = light, insertbackground = light)
            case "system":
                self.switchTheme("dark" if darkdetect.isDark() else "light")

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        *,
        wrap = tkinter.WORD,
        font = ("Consolas", 10),
        bg = light,
        fg = dark,
        relief = tkinter.FLAT,
        **kwargs: Any
    ):
        """
        :param self: `ScrolledText`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param kwargs: 其余参数
        :type kwargs: Any

        **标准参数**

        background, borderwidth, cursor, exportselection, font, foreground, highlightbackground, highlightcolor, highlightthickness, insertbackground, insertborderwidth, insertofftime, insertontime, insertwidth, padx, pady, relief, selectbackground, selectborderwidth, selectforeground, setgrid, takefocus, xscrollcommand, yscrollcommand,

        **特有参数**

        autoseparators, height, maxundo, spacing1, spacing2, spacing3, state, tabs, undo, width, wrap,
        """

        super().__init__(
            master,
            wrap = wrap,
            font = font,
            bg = bg,
            fg = fg,
            relief =relief,
            **kwargs
        )
        maliang.theme.register_event(self.switchTheme)
        self.switchTheme(maliang.theme.get_color_mode())
        self.update()

class WindowFadeIn(maliang.animation.Animation):
    """
    针对`maliang`的窗口写的渐入动画。
    """

    def __init__(
        self,
        window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel],
        duration: int,
        *,
        controller: Callable[[float], float] = maliang.animation.controllers.linear,
        end: Callable[[], Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:

        """
        :param self: `WindowFadeIn`类
        :param window: 要渐入的窗口
        :type window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel]
        :param duration: 持续时长
        :type duration: int
        :param controller: 控制函数
        :type controller: Callable[[float], float]
        :param end: 结束函数
        :type end: Callable[[], Any] | None
        :param fps: 每秒帧数
        :type fps: int
        :param repeat: 重复次数
        :type repeat: int
        :param repeat_delay: 重复前的延时
        :type repeat_delay: int
        """

        if isinstance(window, Sequence):
            def command(p: float) -> None:
                for w in window:
                    w.alpha(p)
        else:
            command = window.alpha

        super().__init__(duration, command, controller = controller, end = end, fps = fps, repeat = repeat, repeat_delay = repeat_delay)

class WindowFadeOut(maliang.animation.Animation):
    """
    针对`maliang`的窗口写的渐出动画。
    """

    def __init__(
        self,
        window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel],
        duration: int,
        *,
        controller: Callable[[float], float] = maliang.animation.controllers.linear,
        end: Callable[[], Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:

        """
        :param self: `WindowFadeOut`类
        :param window: 要渐出的窗口
        :type window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel]
        :param duration: 持续时长
        :type duration: int
        :param controller: 控制函数
        :type controller: Callable[[float], float]
        :param end: 结束函数
        :type end: Callable[[], Any] | None
        :param fps: 每秒帧数
        :type fps: int
        :param repeat: 重复次数
        :type repeat: int
        :param repeat_delay: 重复前的延时
        :type repeat_delay: int
        """

        if isinstance(window, Sequence):
            def command(p: float) -> None:
                for w in window:
                    w.alpha(1 - p)
        else:
            def command(p: float) -> None:
                window.alpha(1 - p)

        super().__init__(duration, command, controller = controller, end = end, fps = fps, repeat = repeat, repeat_delay = repeat_delay)

class RoundedRectangle(maliang.core.virtual.Widget):
    """
    圆角矩形的易用封装。
    """

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        width: int = 1,
        background: str | tuple[int, int, int] = "",
        outline: str | tuple[int, int, int],
        radius: int = 5,
        name: str | None = None,
        anchor: Literal['n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se', 'center'] = "nw",
        gradient_animation: bool = True,
        **kwargs: Any
    ):
        """
        :param self: `RoundedRectangle`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param position: 位置
        :type position: tuple[int, int]
        :param size: 大小
        :type size: tuple[int, int]
        :param width: 边框宽度
        :type width: int
        :param background: 背景色
        :type background: str | tuple[int, int, int]
        :param outline: 边框色
        :type outline: str | tuple[int, int, int]
        :param radius: 圆角半径
        :type radius: int
        :param name: 名称
        :type name: str | None
        :param anchor: 锚点
        :type anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"]
        :param gradient_animation: 是否启用渐变动画
        :type gradient_animation: bool
        """

        super().__init__(master, position, size, anchor = anchor, gradient_animation = gradient_animation)
        self.shape = maliang.standard.shapes.RoundedRectangle(self, (0, 0), size, radius = radius, name = name, gradient_animation = gradient_animation, **kwargs)

        for i in range(0, 14):
            if 0 <= i < 2 or 6 <= i < 10:
                master.itemconfigure(self.shape.items[i], fill = background)
            elif 2 <= i < 6:
                master.itemconfigure(self.shape.items[i], fill = outline, width = width)
            elif 10 <= i < 14:
                master.itemconfigure(self.shape.items[i], outline = outline, width = width)

class Treeview(maliang.Canvas):
    """
    Treeview 控件，基于 maliang.Canvas，内嵌 ttk.Treeview 和 tk.Scrollbar。
    """

    def switchTheme(self, theme: Literal["system", "light", "dark"] = "system") -> None:
        """
        切换主题。

        :param self: `Treeview`类
        :param theme: 主题
        :type theme: Literal["system", "light", "dark"]
        """

        self.style.theme_use("default")

        if theme == "system":
            theme = maliang.theme.get_color_mode()

        if theme == "light":
            self.style.configure("Treeview", rowheight = self.row_height, borderwidth = 0, background = light, foreground = dark, fieldbackground = light)
            self.style.configure("Treeview.Heading", background = light, foreground = dark, borderwidth = 0)
            self.style.map("Treeview.Heading", background = [("active", gray_200)])
            self.style.map("Treeview", background = [("selected", info)], foreground = [("selected", dark)])
            self.vbar.configure(bg = gray_400, troughcolor = gray_200, activebackground = gray_500, highlightthickness = 0, relief = "flat", borderwidth = 0)
        else:
            self.style.configure("Treeview", rowheight = self.row_height, borderwidth = 0, background = dark, foreground = light, fieldbackground = dark)
            self.style.configure("Treeview.Heading", background = dark, foreground = light, borderwidth = 0)
            self.style.map("Treeview.Heading", background = [("active", gray_800)])
            self.style.map("Treeview", background = [("selected", primary)], foreground = [("selected", light)])
            self.vbar.configure(bg = gray_600, troughcolor = gray_800, activebackground = gray_500, highlightthickness = 0, relief = "flat", borderwidth = 0)

    def setRowHeight(self, height: int) -> None:
        """
        设置行高。

        :param self: `Treeview`类
        :param height: 行高
        :type height: int
        """

        self.row_height = height
        self.style.configure("Treeview", rowheight = height)

    def __init__(
        self,
        master,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"] = "nw",
        show: Literal["tree", "headings", "tree headings", ""] = "headings",
        row_height: int = 40,
        **kwargs
    ):
        """
        :param self: `Treeview`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param position: 位置
        :type position: tuple[int, int]
        :param size: 大小
        :type size: tuple[int, int]
        :param anchor: 锚点
        :type anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"]
        :param show: 显示模式
        :type show: Literal["tree", "headings", "tree headings", ""]
        :param row_height: 行高
        :type row_height: int
        """

        self.row_height = row_height

        super().__init__(master, expand = "xy", auto_update = True)

        self.vbar = tkinter.Scrollbar(self, orient = tkinter.VERTICAL)
        self.vbar.place(x = 0, y = 0)
        self.update_idletasks()
        scrollbar_width = self.vbar.winfo_reqwidth()
        self.vbar.place_forget()

        tree_width = size[0] - scrollbar_width
        tree_height = size[1]
        self.place(x = position[0], y = position[1], anchor = anchor, width = size[0], height = size[1])

        self.treeview = tkinter.ttk.Treeview(self, show = show, **kwargs)
        self.treeview.place(x = 0, y = 0, width = tree_width, height = tree_height)

        self.heading = self.treeview.heading
        self.column = self.treeview.column
        self.item = self.treeview.item
        self.selection = self.treeview.selection
        self.selection_set = self.treeview.selection_set
        self.selection_add = self.treeview.selection_add
        self.selection_remove = self.treeview.selection_remove
        self.see = self.treeview.see
        self.get_children = self.treeview.get_children

        self.vbar.configure(command = self.treeview.yview)
        self.vbar.place(x = tree_width, y = 0, width = scrollbar_width, height = tree_height)
        self.treeview.configure(yscrollcommand = self.vbar.set)

        self.style = tkinter.ttk.Style()
        self.switchTheme()
        maliang.theme.register_event(self.switchTheme)

        self.checkbox_enabled = False

    def insert(self, parent: str = "", index: int | str = "end", text: str = "", values: tuple = (), **kwargs) -> str:
        """
        插入行。复选框启用时自动设 `#0` 为 "☐"。

        :param self: `Treeview`类
        :param parent: 父行
        :param index: 位置
        :param text: `#0` 列文本
        :param values: 数据列值
        :return: 行 iid
        :rtype: str
        """

        if self.checkbox_enabled and not text:
            text = "☐"
        return self.treeview.insert(parent, index, text = text, values = values, **kwargs)

    def enableCheckbox(self, enable: bool) -> None:
        """
        启用或禁用复选框功能。

        :param self: `Treeview`类
        :param enable: 是否启用
        :type enable: bool
        """

        self.checkbox_enabled = enable
        if enable:
            self.treeview.configure(show = "tree headings")
            self.treeview.column("#0", width = 50, minwidth = 50, stretch = False, anchor = "center")
            self.treeview.heading("#0", text = "☐")
            for iid in self.treeview.get_children(""):
                self.treeview.item(iid, text = "☐")
            self.treeview.bind("<ButtonRelease-1>", self._onCheckClick)
            self._blockResize = lambda e: "break" if self.treeview.identify_region(e.x, e.y) == "separator" and self.treeview.identify_column(e.x) == "#0" else None
            self.treeview.bind("<ButtonPress-1>", self._blockResize, add = True)
            self.treeview.bind("<B1-Motion>", self._blockResize, add = True)
            self.treeview.bind("<Button-3>", self._onInvertCheck)
            self.after_idle(self._syncSelectionToCheck)
        else:
            self.treeview.configure(show = "headings")
            self.treeview.unbind("<<TreeviewSelect>>")
            self.treeview.unbind("<ButtonRelease-1>")

    def _syncSelectionToCheck(self) -> None:
        """
        同步选中态到复选框显示，并更新全选框状态。

        :param self: `Treeview`类
        """

        if not self.checkbox_enabled:
            return
        selected = set(self.treeview.selection())
        all_checked, any_checked = True, False
        for iid in self.treeview.get_children(""):
            checked = iid in selected
            if not checked:
                all_checked = False
            else:
                any_checked = True
            self.treeview.item(iid, text = "☑" if checked else "☐")
        if all_checked:
            self.treeview.heading("#0", text = "☑")
        elif any_checked:
            self.treeview.heading("#0", text = "☒")
        else:
            self.treeview.heading("#0", text = "☐")

    def _onTreeSelect(self, _) -> None:
        """
        选中态变化时延迟同步复选框。

        :param self: `Treeview`类
        """

        self.treeview.after(10, self._syncSelectionToCheck)

    def _onCheckClick(self, event) -> None:
        """
        处理复选框列点击：单行切换、全选/全不选。

        :param self: `Treeview`类
        :param event: tkinter 事件
        :type event: tkinter.Event
        """

        region = self.treeview.identify_region(event.x, event.y)
        column = self.treeview.identify_column(event.x)
        iid = self.treeview.identify_row(event.y)
        if column == "#0":
            if region == "heading":
                all_checked = self.treeview.heading("#0", "text") == "☑"
                for iid in self.treeview.get_children(""):
                    self.treeview.item(iid, text = "☐" if all_checked else "☑")
                if all_checked:
                    self.treeview.selection_set()
                else:
                    self.treeview.selection_set(*self.treeview.get_children(""))
            elif iid:
                current = self.treeview.item(iid, "text")
                self.treeview.item(iid, text = "☐" if current == "☑" else "☑")
                checked = [i for i in self.treeview.get_children("") if self.treeview.item(i, "text") == "☑"]
                self.treeview.selection_set(*checked)
        self.treeview.after(10, self._syncSelectionToCheck)

    def _onInvertCheck(self, event) -> None:
        """
        右键全选框时反选所有复选框。

        :param self: `Treeview`类
        :param event: tkinter 事件
        :type event: tkinter.Event
        """

        if self.treeview.identify_region(event.x, event.y) != "heading" or self.treeview.identify_column(event.x) != "#0":
            return
        for iid in self.treeview.get_children(""):
            current = self.treeview.item(iid, "text")
            self.treeview.item(iid, text = "☐" if current == "☑" else "☑")
        checked = [i for i in self.treeview.get_children("") if self.treeview.item(i, "text") == "☑"]
        self.treeview.selection_set(*checked)
        self._syncSelectionToCheck()

    def getSelectedValues(self) -> list[tuple]:
        """
        返回所有选中行的 values 数据。

        :return: values 列表
        :rtype: list[tuple]
        """

        result = []
        for i in self.treeview.selection():
            result.append(self.treeview.item(i, "values"))
        return result

    def isChecked(self, iid: str) -> bool:
        """
        返回指定行是否被勾选。

        :param self: `Treeview`类
        :param iid: 行 ID
        :type iid: str
        :return: 是否勾选
        :rtype: bool
        """

        return self.treeview.item(iid, "text") == "☑"
