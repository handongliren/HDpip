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

class Icon(dict[str, maliang.toolbox.enhanced.PhotoImage]):
    def prase(self, color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]]) -> None:
        for color_name, color_value in color_dict.items():
            self[color_name] = self._temp.copy()
            if color_value is not None:
                for x in range(self._temp.width()):
                    for y in range(self._temp.height()):
                        if not self._temp.transparency_get(x, y):
                            self[color_name].put(color_value, (x, y))

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
    @override
    def __init__(
        self, 
        bi: str, 
        color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]] = {"origin": None, "light": color.light, "light_subtle": color.light_subtle, "dark": color.dark, "dark_subtle": color.dark_subtle}, 
        *, 
        size: tuple[int, int] = ss((32, 32))
    ):
        svg = base_dir / f"assets/icons/bootstrap-icons/{bi}.svg"
        if svg.is_file():
            super().__init__(color_dict = color_dict, file = svg, size = size)
        else:
            raise FileNotFoundError(f"Bootstrap Icons '{bi}' 未找到。")
