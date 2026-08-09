"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于渲染自定义图标。
"""

from typing import *

import io
import pathlib
import tkinter
import PIL.Image
import PIL.ImageTk

import maliang.toolbox.enhanced

try:
    from .utility import ss
except ImportError:
    from utility import ss

class Icon(dict[str, maliang.toolbox.enhanced.PhotoImage]):
    def __init__(
        self,
        color_dict: dict[str, str | tuple[int, int, int] | tuple[int, int, int, int]],
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
            self.origin = tkinter.PhotoImage(data = data)
        elif image is not None:
            self.origin = image
        else:
            raise ValueError("必须在 file、data 或 image 中至少提供一个参数。")
