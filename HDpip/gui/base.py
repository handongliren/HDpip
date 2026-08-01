"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是GUI基础轮子，~~屎山2号💩~~。
"""

from typing import *
import decimal
import tkinter
import tkinter.font
import tkinter.scrolledtext

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

_dpi_cache: decimal.Decimal | None = None

def getDpi(use_cache: bool = True) -> decimal.Decimal:
    """
    通过 Tk 根窗口获取系统 DPI。

    :param use_cache: 是否使用缓存，默认 True
    :type use_cache: bool
    :return: 当前系统 DPI，默认返回 96
    :rtype: decimal.Decimal
    """

    global _dpi_cache
    if use_cache and _dpi_cache is not None:
        return _dpi_cache

    try:
        _ = tkinter.Tk()
    except Exception:
        return decimal.Decimal("96.0")

    try:
        _.withdraw()
        _.update_idletasks()
        dpi = _.winfo_fpixels("1i")
        if dpi > 0:
            _dpi_cache = decimal.Decimal(round(dpi, 2))
            return _dpi_cache
    except Exception:
        return decimal.Decimal("96.0")
    finally:
        try:
            _.destroy()
        except Exception:
            pass

    return decimal.Decimal("96.0")

def pxToPt(px: int | decimal.Decimal, dpi: float | decimal.Decimal = getDpi(), *, auto_int: bool = True) -> decimal.Decimal | int:
    """
    将像素大小转换为点数字号。

    :param px: 像素大小
    :type px: int | decimal.Decimal
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | decimal.Decimal
    :param auto_int: 是否自动取整为整数点数字号，默认 True
    :type auto_int: bool
    :return: 对应的点数字号
    :rtype: decimal.Decimal | int
    """

    result = decimal.Decimal(px) * decimal.Decimal("72.0") / decimal.Decimal(dpi)
    result = round(result, 2)
    if auto_int:
        result = result.to_integral_value(rounding = decimal.ROUND_HALF_UP)
    return result

def ptToPx(pt: int | decimal.Decimal, dpi: float | decimal.Decimal = getDpi(), *, auto_int: bool = True) -> decimal.Decimal | int:
    """
    将点数字号转换为像素大小。

    :param pt: 点数字号
    :type pt: int | decimal.Decimal
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | decimal.Decimal
    :param auto_int: 是否自动取整为整数像素大小，默认 True
    :type auto_int: bool
    :return: 对应的像素大小
    :rtype: decimal.Decimal | int
    """

    result = decimal.Decimal(pt) * decimal.Decimal(dpi) / decimal.Decimal("72.0")
    result = round(result, 2)
    if auto_int:
        result = result.to_integral_value(rounding = decimal.ROUND_HALF_UP)
    return result

def getScreenSize() -> tuple[int, int]:
    """
    获取当前屏幕分辨率。

    :return: 当前屏幕分辨率
    :rtype: tuple[int, int]
    """

    _ = tkinter.Tk()
    _.withdraw()
    width = _.winfo_screenwidth()
    height = _.winfo_screenheight()
    _.destroy()
    return (width, height)

_smart_cache: dict[tuple[tuple[int, int], tuple[int, int], bool], decimal.Decimal] = {}

def getSmartScaleValue(
        base_size: tuple[int, int] = (1200, 800), 
        screen_size: tuple[int, int] = getScreenSize(), 
        *, 
        strict_mode: bool = True, 
        use_cache: bool = True
    ) -> decimal.Decimal:
    """
    根据屏幕分辨率和基准分辨率计算智能缩放值。

    :param base_size: 基准尺寸
    :type base_size: tuple[int, int]
    :param screen_size: 屏幕尺寸
    :type screen_size: tuple[int, int]
    :param strict_mode: 是否启用严格模式
    :type strict_mode: bool
    :param use_cache: 是否使用缓存
    :type use_cache: bool
    :return: 智能缩放值
    :rtype: decimal.Decimal
    """

    if use_cache:
        if (base_size, screen_size, strict_mode) in _smart_cache:
            return _smart_cache[(base_size, screen_size, strict_mode)]

    if strict_mode:
        x_start = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[0]) * 5)
        x_end = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.6") / decimal.Decimal(base_size[0]) * 5)
        y_start = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[1]) * 5)
        y_end = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.6") / decimal.Decimal(base_size[1]) * 5)
        start = max(x_start, y_start)
        end = min(x_end, y_end)
    else:
        if (base_size[0] / screen_size[0]) <= (base_size[1] / screen_size[1]):
            start = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[1]) * 5)
            end = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("1") / decimal.Decimal(base_size[1]) * 5)
        else:
            start = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[0]) * 5)
            end = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("1") / decimal.Decimal(base_size[0]) * 5)

    available_list = [decimal.Decimal(i) * decimal.Decimal("0.2") for i in range(start, end + 1)]
    seed_list = [i for i in available_list if i == i.to_integral_value()]

    if len(seed_list) > 0:
        result = max(seed_list)
    elif len(available_list) > 0:
        result = max(available_list)
    if len(available_list) == 0 or result < decimal.Decimal("0.6"):
        if strict_mode:
            result = getSmartScaleValue(base_size, screen_size, strict_mode = False, use_cache = use_cache)
        else:
            result = decimal.Decimal("0.6")

    _smart_cache[(base_size, screen_size, strict_mode)] = result
    return result

def smartScale(value: int | decimal.Decimal | Iterable[int | decimal.Decimal], 
    base_size: tuple[int, int] = (1200, 800), 
    screen_size: tuple[int, int] = getScreenSize(), 
    *, 
    strict_mode: bool = True, 
    use_cache: bool = True, 
    return_type: Literal["Decimal", "float", "int"] = "int"
) -> decimal.Decimal | Iterable[decimal.Decimal] | float | Iterable[float] | int | Iterable[int]:
    """
    对给定的值进行智能缩放。

    :param value: 要缩放的值
    :type value: int | decimal.Decimal | Iterable[int | decimal.Decimal]
    :param base_size: 基准尺寸
    :type base_size: tuple[int, int]
    :param screen_size: 屏幕尺寸
    :type screen_size: tuple[int, int]
    :param strict_mode: 是否启用严格模式
    :type strict_mode: bool
    :param use_cache: 是否使用缓存
    :type use_cache: bool
    :param return_type: 返回类型
    :type return_type: Literal["Decimal", "float", "int"]
    :return: 缩放后的值
    :rtype: decimal.Decimal | Iterable[decimal.Decimal] | float | Iterable[float] | int | Iterable[int]
    """

    scale_value = getSmartScaleValue(base_size, screen_size, strict_mode = strict_mode, use_cache = use_cache)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return type(value)([smartScale(v, base_size, screen_size, strict_mode = strict_mode, use_cache = use_cache, return_type = return_type) for v in value])
    elif isinstance(value, (int, decimal.Decimal)):
        result = decimal.Decimal(value) * scale_value
        if return_type == "Decimal":
            return result
        elif return_type == "float":
            return float(result)
        elif return_type == "int":
            return int(result)
    else:
        raise TypeError(f"不支持的类型：{type(value).__name__}，仅支持 int、decimal.Decimal 或 Iterable[int | decimal.Decimal]。")

ss = smartScale

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
        fontsize: int | None = ss(20),
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
        font: tuple[str, int] | tkinter.font.Font = ("TkDefaultFont", pxToPt(ss(20))),
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

    def setAppearance(
        self, 
        outline: str | tuple[int, int, int], 
        background: str | tuple[int, int, int] = "", 
        width: int = 1
    ) -> None:
        """
        设置圆角矩形的外观。

        :param self: `RoundedRectangle`类
        :param background: 背景色
        :type background: str | tuple[int, int, int]
        :param outline: 边框色
        :type outline: str | tuple[int, int, int]
        :param width: 边框宽度
        :type width: int
        """

        for i in range(0, 14):
            if 0 <= i < 2 or 6 <= i < 10:
                self.master.itemconfigure(self.shape.items[i], fill = background)
            elif 2 <= i < 6:
                self.master.itemconfigure(self.shape.items[i], fill = outline, width = width)
            elif 10 <= i < 14:
                self.master.itemconfigure(self.shape.items[i], outline = outline, width = width)

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        width: int = 1,
        background: str | tuple[int, int, int] = "",
        outline: str | tuple[int, int, int] = "",
        radius: int = ss(10),
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
        self.setAppearance(outline = outline, background = background, width = width)

class Line(maliang.core.virtual.Widget):
    """
    直线的易用封装。
    """

    def setAppearance(
        self,
        color: str | tuple[int, int, int],
        width: int = 1
    ) -> None:
        """
        设置直线的外观。

        :param self: `Line`类
        :param color: 颜色
        :type color: str | tuple[int, int, int]
        :param width: 宽度
        :type width: int
        """

        self.master.itemconfigure(self._item, fill = color, width = width)

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        color: str | tuple[int, int, int] = "",
        width: int = 1,
        name: str | None = None,
        anchor: Literal['n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se', 'center'] = "nw",
        gradient_animation: bool = True,
        **kwargs: Any
    ):
        """
        :param self: `Line`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param position: 位置
        :type position: tuple[int, int]
        :param size: 大小
        :type size: tuple[int, int]
        :param color: 颜色
        :type color: str | tuple[int, int, int]
        :param width: 宽度
        :type width: int
        :param name: 名称
        :type name: str | None
        :param anchor: 锚点
        :type anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"]
        :param gradient_animation: 是否启用渐变动画
        :type gradient_animation: bool
        """

        super().__init__(master, position, size, anchor = anchor, gradient_animation = gradient_animation)
        x1, y1 = self.position
        dx, dy = size[0] or 1, size[1] or 1
        self._item = self.master.create_line(x1, y1, x1 + dx, y1 + dy, fill = color, width = width, tags = ("fill",))
