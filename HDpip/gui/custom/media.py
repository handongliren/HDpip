"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于渲染自定义图标。
"""

from typing import *
from typing_extensions import Self, override

import io
import pathlib
import tkinter
import PIL.Image
import PIL.ImageTk

import maliang.toolbox.enhanced

try:
    from . import color
    from .utility import ss
except ImportError:
    import color
    from utility import ss

base_dir = pathlib.Path(__file__).parents[2].resolve()

class Image(maliang.toolbox.enhanced.PhotoImage):
    """
    图片类，统一支持 file / data / image 三种输入，兼容 Tk、PIL 与 maliang 图片类型。
    """

    @override
    def __init__(
        self,
        *,
        file: str | pathlib.Path | None = None,
        data: str | bytes | bytearray | memoryview | None = None,
        image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | PIL.Image.Image | None = None,
        size: tuple[int, int] | None = None
    ):
        """
        从图片源加载图片。

        :param self: `Image`类
        :param file: 图片文件路径，支持 PNG/GIF/BMP/ICO/SVG
        :type file: str | pathlib.Path | None
        :param data: 原始图片数据
        :type data: str | bytes | bytearray | memoryview | None
        :param image: 已有图片对象
        :type image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | PIL.Image.Image | None
        :param size: 渲染尺寸（仅 SVG 有效）
        :type size: tuple[int, int] | None
        """

        if file is not None:
            try:
                super().__init__(file = file)
            except (tkinter.TclError, PIL.Image.UnidentifiedImageError):
                if pathlib.Path(file).suffix.lower() == ".svg":
                    import resvg_py
                    options = {"width": size[0], "height": size[1]} if size else {}
                    self._fromPil(PIL.Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_path = str(file), **options))))
                else:
                    self._fromPil(PIL.Image.open(file))
        elif data is not None:
            super().__init__(data = data)
        elif image is not None:
            if isinstance(image, PIL.Image.Image):
                self._fromPil(image)
            else:
                self._fromPil(PIL.ImageTk.getimage(image))
        else:
            raise ValueError("必须在 file、data 或 image 中至少提供一个参数。")
        self.name = str(self)

    def _fromPil(self, image: PIL.Image.Image) -> None:
        """
        通过 PIL Image 中转加载。

        :param self: `Image`类
        :param image: PIL 图片
        :type image: PIL.Image.Image
        """

        buffer = io.BytesIO()
        image.save(buffer, "PNG")
        super().__init__(data = buffer.getvalue())

    @override
    def copy(self) -> Self:
        """
        复制图片，返回新的 `Image` 实例。

        :param self: `Image`类
        :return: 复制后的图片
        :rtype: Self
        """

        return Image(image = self)

    @override
    def resize(self, width: int, height: int) -> Self:
        """
        缩放图片，返回新的 `Image` 实例。

        :param self: `Image`类
        :param width: 新宽度
        :type width: int
        :param height: 新高度
        :type height: int
        :return: 缩放后的图片
        :rtype: Self
        """

        return Image(image = super().resize(width, height))

    def prase(
        self,
        color_value: str | tuple[int, int, int] | tuple[int, int, int, int]
    ) -> Self:
        """
        按指定颜色渲染图片。

        :param self: `Image`类
        :param color_value: 颜色值
        :type color_value: str | tuple[int, int, int] | tuple[int, int, int, int]
        :return: 渲染后的图片对象
        :rtype: Self
        """

        result = self.copy()
        for x in range(result.width()):
            for y in range(result.height()):
                if not result.transparency_get(x, y):
                    result.put(color_value, (x, y))
        return result

class Icon(dict[str, maliang.toolbox.enhanced.PhotoImage]):
    """
    图标类，用于渲染不同颜色的图标，支持多种图片格式。
    """

    def prase(self, color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]) -> None:
        """
        按颜色字典渲染图标，每种颜色生成一个独立变体存入。

        :param self: `Icon`类
        :param color_dict: 颜色字典，键为颜色名，值为颜色值或 None（保留原色）
        :type color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]
        """

        for color_name, color_value in color_dict.items():
            self[color_name] = self.origin.prase(color_value) if color_value is not None else self.origin.copy()

    @override
    def __init__(
        self,
        color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]] = {"origin": None, "light": color.light, "light_subtle": color.light_subtle, "dark": color.dark, "dark_subtle": color.dark_subtle},
        *,
        image: Image, 
        size: tuple[int, int] = ss((32, 32))
    ):
        """
        从图片源加载并渲染图标。

        :param self: `Icon`类
        :param color_dict: 颜色字典，键为颜色名，值为颜色值或 None（保留原色）
        :type color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]
        :param image: 图片对象
        :type image: Image
        :param size: 渲染尺寸
        :type size: tuple[int, int]
        """

        self.color_dict = color_dict
        self.origin = image.resize(*size)
        self.prase(color_dict)

class BootstrapIcon(Image):
    """
    Bootstrap Icons 图标，从本地 SVG 文件渲染。
    """

    @override
    def __init__(
        self,
        bi_name: str,
        *,
        size: tuple[int, int] | None = None
    ):
        """
        加载指定名称的 Bootstrap Icons SVG。

        :param self: `BootstrapIcon`类
        :param bi_name: Bootstrap Icons 名称（不含扩展名）
        :type bi_name: str
        :param size: 渲染尺寸
        :type size: tuple[int, int]
        """

        svg = base_dir / f"assets/icons/bootstrap-icons/{bi_name}.svg"
        if svg.is_file():
            super().__init__(file = svg, size = size)
        else:
            raise FileNotFoundError(f"Bootstrap Icons '{bi_name}' 未找到。")

bi = BootstrapIcon
