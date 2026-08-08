"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

自定义控件。
"""

from typing import *
from typing_extensions import override

import maliang

try:
    from . import color
    from . import utility
except ImportError:
    import color
    import utility

class Button(maliang.Button):
    """
    继承自`maliang.Button`，添加了bootstrap配色，使用`theme`参数指定主题。
    """

    @override
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
            color_ = _[0]
            outline = False
        elif len(_) == 2:
            color_ = _[1]
            outline = True

        light = color.light
        dark = color.dark
        light_subtle = color.light_subtle
        dark_subtle = color.dark_subtle
        colors = color.colors

        if not disabled:
            if not outline:
                match color_:
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
                            bg = (colors[color_][0], colors[color_][0], colors[color_][1]),
                            ol = (colors[color_][0], colors[color_][0], colors[color_][1])
                        )
            else:
                match color_:
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
                            fg = (colors[color_][0], light, light_subtle),
                            bg = ("", colors[color_][0], colors[color_][1]),
                            ol = (colors[color_][0], colors[color_][0], colors[color_][1])
                        )
        else:
            if not outline:
                match color_:
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
                            bg = colors[color_][1],
                            ol = colors[color_][1]
                        )
            else:
                match color_:
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
                            fg = colors[color_][1],
                            bg = "",
                            ol = colors[color_][1]
                        )

    @override
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
        fontsize: int | None = utility.ss(20),
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

    @override
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
