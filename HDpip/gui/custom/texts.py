"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

文本组件。
"""

import tkinter
import tkinter.font
import tkinter.scrolledtext
from typing import *
from typing_extensions import override

import darkdetect
import maliang
import maliang.theme

try:
    from . import color
    from . import utility
except ImportError:
    import color
    import utility

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
                self.configure(bg = color.light, fg = color.dark, selectbackground = color.info, selectforeground = color.dark, insertbackground = color.dark)
            case "dark":
                self.configure(bg = color.dark, fg = color.light, selectbackground = color.primary, selectforeground = color.light, insertbackground = color.light)
            case "system":
                self.switchTheme("dark" if darkdetect.isDark() else "light")

    @override
    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        *,
        wrap = tkinter.WORD,
        font: tuple[str, int] | tkinter.font.Font = ("TkDefaultFont", utility.pxToPt(utility.ss(20))),
        bg = color.light,
        fg = color.dark,
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
            relief = relief,
            **kwargs
        )
        maliang.theme.register_event(self.switchTheme)
        self.switchTheme(maliang.theme.get_color_mode())
        self.update()
