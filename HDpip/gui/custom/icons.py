"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于渲染自定义图标。
"""

from typing import *
from typing_extensions import override

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

class Image(maliang.toolbox.enhanced.PhotoImage, PIL.ImageTk.PhotoImage, tkinter.PhotoImage):
    """
    图片类，统一支持 file / data / image 三种输入，兼容 Tk、PIL 与 maliang 图片类型。
    """

    @override
    def __init__(
        self, 
        *, 
        file: str | pathlib.Path | None = None, 
        data: str | bytes | bytearray | memoryview | None = None, 
        image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | None = None
    ):
        """
        从图片源加载图片。

        :param self: `Image`类
        :param file: 图片文件路径，支持 PNG/GIF/BMP/ICO/SVG
        :type file: str | pathlib.Path | None
        :param data: 原始图片数据
        :type data: str | bytes | bytearray | memoryview | None
        :param image: 已有图片对象
        :type image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | None
        """

        if file is not None:
            if pathlib.Path(file).suffix.lower() == ".svg":
                import resvg_py
                png_bytes = resvg_py.svg_to_bytes(svg_path = str(file))
                super().__init__(PIL.Image.open(io.BytesIO(png_bytes)))
            else:
                super().__init__(file = file)
        elif data is not None:
            super().__init__(data = data)
        elif image is not None:
            super().__init__(PIL.ImageTk.getimage(image))
        else:
            raise ValueError("必须在 file、data 或 image 中至少提供一个参数。")

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

        if not color_dict.get(color_name, "None") == self.color_dict.get(color_name, "None"):
            for color_name, color_value in color_dict.items():
                self[color_name] = self._temp.copy()
                if color_value is not None:
                    for x in range(self._temp.width()):
                        for y in range(self._temp.height()):
                            if not self._temp.transparency_get(x, y):
                                self[color_name].put(color_value, (x, y))
                                self.color_dict[color_name] = color_value

    @override
    def __init__(
        self,
        color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]] = {"origin": None, "light": color.light, "light_subtle": color.light_subtle, "dark": color.dark, "dark_subtle": color.dark_subtle},
        *,
        file: str | pathlib.Path | None = None,
        data: str | bytes | bytearray | memoryview | None = None,
        image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | None = None,
        size: tuple[int, int] = ss((32, 32))
    ):
        """
        从图片源加载并渲染图标。

        :param self: `Icon`类
        :param color_dict: 颜色字典，键为颜色名，值为颜色值或 None（保留原色）
        :type color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]
        :param file: 图片文件路径，支持 PNG/GIF/BMP/ICO/SVG
        :type file: str | pathlib.Path | None
        :param data: 原始图片数据
        :type data: str | bytes | bytearray | memoryview | None
        :param image: 已有图片对象
        :type image: tkinter.PhotoImage | PIL.ImageTk.PhotoImage | maliang.toolbox.enhanced.PhotoImage | None
        :param size: 渲染尺寸
        :type size: tuple[int, int]
        """

        self.color_dict = color_dict
        if file is not None:
            try:
                self.origin = tkinter.PhotoImage(file = file)
            except tkinter.TclError:
                if pathlib.Path(file).suffix.lower() == ".svg":
                    import resvg_py
                    png_bytes = resvg_py.svg_to_bytes(svg_path = str(file), width = size[0], height = size[1])
                    self.origin = PIL.ImageTk.PhotoImage(PIL.Image.open(io.BytesIO(png_bytes)))
                else:
                    self.origin = PIL.ImageTk.PhotoImage(PIL.Image.open(file))
        elif data is not None:
            self.origin = PIL.ImageTk.PhotoImage(data = data)
        elif image is not None:
            self.origin = image
        else:
            raise ValueError("必须在 file、data 或 image 中至少提供一个参数。")
        self._temp = maliang.toolbox.enhanced.PhotoImage(self.origin.copy())
        self._temp = self._temp.resize(*size)
        self.prase(color_dict)

class BootstrapIcon(Icon):
    """
    Bootstrap Icons 图标，从本地 SVG 文件渲染。
    """

    @override
    def __init__(
        self,
        bi_name: str,
        color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]] = {"origin": None, "light": color.light, "light_subtle": color.light_subtle, "dark": color.dark, "dark_subtle": color.dark_subtle},
        *,
        size: tuple[int, int] = ss((32, 32))
    ):
        """
        加载指定名称的 Bootstrap Icons SVG 并渲染。

        :param self: `BootstrapIcon`类
        :param bi_name: Bootstrap Icons 名称（不含扩展名）
        :type bi_name: str
        :param color_dict: 颜色字典，键为颜色名，值为颜色值或 None（保留原色）
        :type color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]
        :param size: 渲染尺寸
        :type size: tuple[int, int]
        """

        svg = base_dir / f"assets/icons/bootstrap-icons/{bi_name}.svg"
        if svg.is_file():
            super().__init__(color_dict = color_dict, file = svg, size = size)
        else:
            raise FileNotFoundError(f"Bootstrap Icons '{bi_name}' 未找到。")

bi = BootstrapIcon
