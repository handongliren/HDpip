"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

自定义控件。
"""

from typing import *
from typing_extensions import override

import maliang
import maliang.standard.styles
import maliang.toolbox.utility

# maliang 样式表缺少 StillImage，一次性补充（图标不着色）
for _theme_dict in (maliang.standard.styles.ButtonStyle.light, maliang.standard.styles.ButtonStyle.dark):
    _theme_dict.setdefault("StillImage", {"normal": {}, "hover": {}, "active": {}})

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
        if self.icon and not self.use_original_icon:
            style = self.style.get()
            fills = [style["StillImage"]["normal"]["fill"]] * 3 if disabled else [style["StillImage"][state]["fill"] for state in ("normal", "hover", "active")]
            self.icon.prase({state: fill for state, fill in zip(("normal", "hover", "active"), fills)})
            self.images[0].widget.master.itemconfigure(self.images[0].items[0], image = self.icon["normal"])
            for theme_name in ("light", "dark"):
                for state, fill in zip(("normal", "hover", "active"), fills):
                    self.style.get(theme = theme_name)["Information"][state]["fill"] = fill
                    self.style.get(theme = theme_name)["StillImage"][state]["fill"] = fill

    @override
    def __init__(
        self,
        master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
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
        fontsize: int | None = utility.ss(25),
        weight: Literal['normal', 'bold'] = "normal",
        slant: Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: Literal["left", "center", "right"] = "left",
        command: Callable | None = None,
        icon: media.Image | None = None,
        icon_position: Literal["left", "right"] = "left",
        use_original_icon: bool = False,
        anchor: Literal["n", "e", "w", "s", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
        auto_update: bool | None = None,
        style: type[maliang.core.virtual.Style] | None = None,
    ):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
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
        :param icon: 图标图片
        :type icon: media.Image | None
        :param icon_position: 图标放置位置（仅当 icon 不为 None）
        :type icon_position: Literal["left", "right"]
        :param use_original_icon: 是否使用原图（不随主题染色）
        :type use_original_icon: bool
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

        self.icon = None
        self.icon_position = icon_position
        self.use_original_icon = use_original_icon
        if icon is not None:
            self.icon = media.Icon({"origin": None}, image = icon, size = (fontsize, fontsize))
            text = ("　" + text) if icon_position == "left" else (text + "　")
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
            image = self.icon["origin"] if self.icon else None,
            anchor = anchor,
            capture_events = capture_events,
            gradient_animation = gradient_animation,
            auto_update = auto_update,
            style = style
        )
        if self.icon is not None:
            self._placeIcon()
        self.theme = theme
        self.disabled = False
        self.switchTheme(theme, False)
        self.update()

    @override
    def get(self) -> str:
        """
        获取文本（不含占位空格）。

        :return: 文本
        :rtype: str
        """

        text = self.texts[0].get()
        if self.icon:
            text = text.removeprefix("　") if self.icon_position == "left" else text.removesuffix("　")
        return text

    @override
    def set(self, text: str) -> None:
        """
        设置文本（自动处理占位空格并重新定位图标）。

        :param text: 文本
        :type text: str
        """

        if self.icon:
            text = ("　" + text) if self.icon_position == "left" else (text + "　")
        super().set(text)
        if self.icon:
            self._placeIcon()

    def _placeIcon(self) -> None:
        """
        将图标定位到文本占位空格处。
        """

        text_x1, text_y1, text_x2, text_y2 = self.texts[0].region()
        space_width, _ = maliang.toolbox.utility.get_text_size("　", font = self.texts[0].font, master = self.master)
        if self.icon_position == "left":
            target_x = text_x1 + space_width / 2
        else:
            target_x = text_x2 - space_width / 2
        target_y = (text_y1 + text_y2) / 2
        icon_x1, icon_y1, icon_x2, icon_y2 = self.images[0].region()
        current_x = (icon_x1 + icon_x2) / 2
        current_y = (icon_y1 + icon_y2) / 2
        self.images[0].move(target_x - current_x, target_y - current_y)

    @override
    def update(
        self,
        state: str | None = None,
        *,
        gradient_animation: bool | None = None,
        nested: bool = False,
    ) -> None:
        """
        更新控件，并根据状态切换图标。

        :param state: 状态
        :type state: str | None
        :param gradient_animation: 过渡动画
        :type gradient_animation: bool | None
        :param nested: 是否嵌套更新
        :type nested: bool
        """

        super().update(state, gradient_animation = False, nested = nested)
        if self.icon:
            if self.use_original_icon:
                if self.disabled:
                    self.icon.setdefault("disabled", self.icon["origin"].prase(color.gray_500))
                    image = self.icon["disabled"]
                else:
                    image = self.icon["origin"]
            elif "normal" in self.icon:
                if self.disabled:
                    image = self.icon.get("disabled", self.icon["normal"])
                else:
                    image = self.icon.get(self.state, self.icon["normal"])
            else:
                image = None
            if image is not None:
                self.images[0].widget.master.itemconfigure(self.images[0].items[0], image = image)

    @override
    def disable(self, value: bool = True) -> None:
        """
        修改`Button`类的禁用状态。

        :param value: 是否禁用
        :type value: bool
        """

        self.disabled = value
        self.switchTheme(self.theme, value)
        self.update("normal")
        if value or self.state_before_disabled:
            super().disable(value)
        if value and self.icon and not self.use_original_icon:
            style = self.style.get()
            fill = style["Information"].get("disabled", {}).get("fill")
            if fill is not None:
                self.icon.prase({state: fill for state in ("normal", "hover", "active")})
                self.images[0].widget.master.itemconfigure(self.images[0].items[0], image = self.icon["normal"])
