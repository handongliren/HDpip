"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

自定义控件。
"""

from typing import *
from typing_extensions import override

import maliang
import maliang.theme

try:
    from . import color
    from . import utility
    from . import media
except ImportError:
    import color
    import utility
    import HDpip.gui.custom.media as media

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

        if not disabled:
            if not outline:
                match color_:
                    case "default":
                        self.style.set(
                            "light",
                            fg = (color.light, color.light, color.light_subtle),
                            bg = (color.dark, color.dark, color.dark_subtle),
                            ol = (color.dark, color.dark, color.dark_subtle)
                        )
                        self.style.set(
                            "dark",
                            fg = (color.dark, color.dark, color.dark_subtle),
                            bg = (color.light, color.light, color.light_subtle),
                            ol = (color.light, color.light, color.light_subtle)
                        )
                    case "light":
                        self.style.set(
                            fg = (color.dark, color.dark, color.dark_subtle),
                            bg = (color.light, color.light, color.light_subtle),
                            ol = (color.light, color.light, color.light_subtle)
                        )
                    case _:
                        self.style.set(
                            fg = (color.light, color.light, color.light_subtle),
                            bg = (color.colors[color_][0], color.colors[color_][0], color.colors[color_][1]),
                            ol = (color.colors[color_][0], color.colors[color_][0], color.colors[color_][1])
                        )
            else:
                match color_:
                    case "default":
                        self.style.set(
                            "light",
                            fg = (color.dark, color.light, color.light_subtle),
                            bg = ("", color.dark, color.dark_subtle),
                            ol = (color.dark, color.dark, color.dark_subtle)
                        )
                        self.style.set(
                            "dark",
                            fg = (color.light, color.dark, color.dark_subtle),
                            bg = ("", color.light, color.light_subtle),
                            ol = (color.light, color.light, color.light_subtle)
                        )
                    case "light":
                        self.style.set(
                            fg = (color.light, color.dark, color.dark_subtle),
                            bg = ("", color.light, color.light_subtle),
                            ol = (color.light, color.light, color.light_subtle)
                        )
                    case _:
                        self.style.set(
                            fg = (color.colors[color_][0], color.light, color.light_subtle),
                            bg = ("", color.colors[color_][0], color.colors[color_][1]),
                            ol = (color.colors[color_][0], color.colors[color_][0], color.colors[color_][1])
                        )
        else:
            if not outline:
                match color_:
                    case "default":
                        self.style.set(
                            "light",
                            fg = color.light_subtle,
                            bg = color.dark_subtle,
                            ol = color.dark_subtle
                        )
                        self.style.set(
                            "dark",
                            fg = color.dark_subtle,
                            bg = color.light_subtle,
                            ol = color.light_subtle
                        )
                    case "light":
                        self.style.set(
                            fg = color.dark_subtle,
                            bg = color.light_subtle,
                            ol = color.light_subtle
                        )
                    case _:
                        self.style.set(
                            fg = color.light_subtle,
                            bg = color.colors[color_][1],
                            ol = color.colors[color_][1]
                        )
            else:
                match color_:
                    case "default":
                        self.style.set(
                            "light",
                            fg = color.dark_subtle,
                            bg = "",
                            ol = color.dark_subtle
                        )
                        self.style.set(
                            "dark",
                            fg = color.light_subtle,
                            bg = "",
                            ol = color.light_subtle
                        )
                    case "light":
                        self.style.set(
                            fg = color.light_subtle,
                            bg = "",
                            ol = color.light_subtle
                        )
                    case _:
                        self.style.set(
                            fg = color.colors[color_][1],
                            bg = "",
                            ol = color.colors[color_][1]
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
        self.disabled = False
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

class IconButton(Button):
    """
    继承自`Button`，用于带图标的按钮，图标支持左右两种放置位置。
    """

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
        image: media.Image,
        icon_position: Literal["left", "right"] = "left",
        anchor: Literal["n", "e", "w", "s", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
        auto_update: bool | None = None,
        style: type[maliang.core.virtual.Style] | None = None,
    ):
        """
        :param self: `IconButton`类
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
        :type image: media.Image
        :param icon_position: 图标放置位置
        :type icon_position: Literal["left", "right"]
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

        self.disabled = False
        self.icon = media.Icon({}, image = image)
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
        offset = self.size[0] // 4
        self.images[0].move(offset if icon_position == "left" else -offset, 0)
        maliang.theme.register_event(lambda _: self.switchTheme(self.theme, self.disabled))

    @override
    def update(
        self,
        state: str | None = None,
        *,
        gradient_animation: bool | None = None,
        nested: bool = False,
    ) -> None:
        """
        更新控件，并根据状态切换图标颜色。

        :param self: `IconButton`类
        :param state: 状态
        :type state: str | None
        :param gradient_animation: 过渡动画
        :type gradient_animation: bool | None
        :param nested: 是否嵌套更新
        :type nested: bool
        """

        super().update(state, gradient_animation = gradient_animation, nested = nested)
        if self.icon:
            self.images[0].configure({"image": self.icon.get(self.state, self.icon["normal"])})

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
        切换主题，并同步图标颜色（从样式表读取前景色）。

        :param self: `IconButton`类
        :param theme: 主题
        :type theme: Literal["default", "primary", "secondary", "success", "info", "warning", "danger", "light", "dark", "outline-default", "outline-primary", "outline-secondary", "outline-success", "outline-info", "outline-warning", "outline-danger", "outline-light", "outline-dark"]
        :param disabled: 是否为禁用状态
        :type disabled: bool
        """

        for theme_dict in (self.style.light, self.style.dark):
            theme_dict.setdefault("StillImage", {"normal": {}, "hover": {}, "active": {}})
        super().switchTheme(theme, disabled)
        icon_style = self.style.dark["StillImage"] if maliang.theme.get_color_mode() == "dark" else self.style.light["StillImage"]
        self.icon.prase({state: icon_style[state]["fill"] for state in ("normal", "hover", "active")})
        self.images[0].configure({"image": self.icon["normal"]})
