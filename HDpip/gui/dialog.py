"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是对话框。
"""

import tkinter
from typing import *

import maliang

try:
    from . import base
except ImportError:
    import base

class DialogCanvas(maliang.Canvas):
    """
    对话框控件，基于`maliang.Canvas`。
    """

    def closeCommand(self, *argvs, **kargvs) -> None:
        """
        关闭对话框。

        :param self: `DialogCanvas`类
        """

        self.after(1, self.destroy)

    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        outline: bool = True,
        title: str | None = None,
        text: str = "",
        button: list[dict[str, str | Callable[[], Any]]] = [{"text": "确认"}],
        theme: Literal["info", "primary", "danger", "warning", "success"] = "primary",
        anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"] = "nw",
        closeCommand: Callable[[], None] | None = None,
    ):
        """
        :param self: `DialogCanvas`类
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param position: 位置
        :type position: tuple[int, int]
        :param size: 大小
        :type size: tuple[int, int]
        :param outline: 是否启用轮廓
        :type outline: bool
        :param title: 标题
        :type title: str | None
        :param text: 文本
        :type text: str
        :param button: 按钮组
        :type button: list[dict[str, str | Callable[[], Any]]]
        :param theme: 主题
        :type theme: Literal["info", "primary", "danger", "warning", "success"]
        :param anchor: 锚点
        :type anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"]
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.place(x = position[0], y = position[1], anchor = anchor, width = size[0], height = size[1])

        self.theme_color = base.colors[theme][0]
        title_height = 80
        button_width = 160
        button_height = 80
        margin = 20

        self.create_line(margin, title_height, size[0] - margin, title_height, fill = self.theme_color, width = 1)
        self.create_line(margin, size[1] - button_height, size[0] - margin, size[1] - button_height, fill = self.theme_color, width = 1)

        if outline:
            self.outline = base.RoundedRectangle(self, (0, 0), (size[0] - 2, size[1] - 2), outline = self.theme_color)

        if title == None:
            title = theme
        self.title = maliang.Text(self, (margin, 40), size = [size[0] - 2 * margin, title_height], text = title, fontsize = 50, weight = "bold", anchor = "w", justify = "left", auto_update = True)

        self.scrolled_text = base.ScrolledText(self)
        self.scrolled_text.place(x = size[0] / 2, y = size[1] / 2, width = size[0] - 4 * margin, height = size[1] - 2 * margin - title_height - button_height, anchor = "center")
        self.scrolled_text.delete(1.0, tkinter.END)
        self.scrolled_text.insert(1.0, text)
        self.scrolled_text.configure(state = tkinter.DISABLED)

        buttons_width = len(button) * button_width + (len(button) - 1) * margin + 2
        self.button_canvas = maliang.Canvas(self, auto_update = True)
        self.button_canvas.place(x = (size[0] - buttons_width) / 2, y = size[1] - button_height + margin / 4, anchor = "nw", width = buttons_width, height = button_height - margin / 2)

        self.button_list: list[base.Button] = []
        for i in range(0, len(button)):
            button[i].setdefault("theme", theme)
            cmd = closeCommand if closeCommand else self.closeCommand
            button[i].setdefault("command", cmd)

            self.button_list.append(
                base.Button(self.button_canvas, [i * (button_width + margin), (button_height - margin / 2) / 2], [button_width, button_height - margin], anchor = "w", text = button[i]["text"], theme = button[i]["theme"])
            )
            self.button_list[i].bind("<Button-1>", button[i]["command"])

class DialogToplevel(maliang.Toplevel):
    """
    对话框控件，基于`maliang.Toplevel`，内嵌`DialogCanvas`。
    """

    def closeCommand(self, *argvs, **kargvs) -> None:
        """
        关闭对话框。

        :param self: `DialogToplevel`类
        """

        self.after(1, self.destroy)

    def __init__(
        self,
        master: maliang.Tk | maliang.Toplevel | None = None,
        size: tuple[int, int] = (800, 600),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        text: str = "",
        button: list[dict[str, str | Callable[[], Any]]] = ({"text": "确认"},),
        theme: Literal["info", "primary", "danger", "warning", "success"] = "primary"
    ):
        """
        :param self: `DialogToplevel`类
        :param master: 父窗口
        :type master: maliang.Tk | maliang.Toplevel | None
        :param size: 大小
        :type size: tuple[int, int]
        :param title: 标题
        :type title: str | None
        :param text: 文本
        :type text: str
        :param button: 按钮组
        :type button: list[dict[str, str | Callable[[], Any]]]
        :param theme: 主题
        :type theme: Literal["info", "primary", "danger", "warning", "success"]
        """

        if title == None:
            title = theme

        super().__init__(master, size = size, title = title)
        self.resizable(False, False)
        if position is None:
            self.center()
        elif isinstance(position, tuple[int, int]):
            self.geometry(position = position)

        for i in button:
            i.setdefault("command", self.closeCommand)
        self.dialog_canvas = DialogCanvas(self, (0, 0), size, outline = False, title = title, text = text, button = button, theme = theme, closeCommand = self.closeCommand)


class DialogTk(maliang.Tk):
    """
    对话框控件，基于`maliang.Tk`，内嵌`DialogCanvas`。
    """

    def closeCommand(self, *argvs, **kargvs) -> None:
        """
        关闭对话框。

        :param self: `DialogTk`类
        """

        self.after(1, self.destroy)

    def __init__(
        self,
        size: tuple[int, int] = (800, 600),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        text: str = "",
        button: list[dict[str, str | Callable[[], Any]]] = ({"text": "确认"},),
        theme: Literal["info", "primary", "danger", "warning", "success"] = "primary"
    ):
        """
        :param self: `DialogTk`类
        :param size: 大小
        :type size: tuple[int, int]
        :param title: 标题
        :type title: str | None
        :param text: 文本
        :type text: str
        :param button: 按钮组
        :type button: list[dict[str, str | Callable[[], Any]]]
        :param theme: 主题
        :type theme: Literal["info", "primary", "danger", "warning", "success"]
        """

        if title == None:
            title = theme

        super().__init__(size = size, title = title)
        self.resizable(False, False)
        if position is None:
            self.center()
        elif isinstance(position, tuple[int, int]):
            self.geometry(position = position)

        for i in button:
            i.setdefault("command", self.closeCommand)
        self.dialog_canvas = DialogCanvas(self, (0, 0), size, outline = False, title = title, text = text, button = button, theme = theme, closeCommand = self.closeCommand)
