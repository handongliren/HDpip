"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

形状控件封装。
"""

from typing import *
from typing_extensions import override

import maliang
import maliang.standard.shapes
import maliang.core.virtual

try:
    from . import utility
except ImportError:
    import utility

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

    @override
    def __init__(
        self,
        master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        width: int = 1,
        background: str | tuple[int, int, int] = "",
        outline: str | tuple[int, int, int] = "",
        radius: int = utility.ss(10),
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
