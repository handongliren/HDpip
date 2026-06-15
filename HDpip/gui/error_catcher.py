"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是错误捕捉器。
"""

from typing import *
from functools import *
import traceback
import pathlib
import subprocess
import sys

base_dir = pathlib.Path(__file__).parents[1].resolve()

def catch(func: Callable[..., Any]):
    """
    装饰器，用于捕捉错误并显示对话框。

    :param func: 装饰的函数
    :type func: Callable[..., Any]
    :return: 装饰后的函数
    :rtype: _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any | None]
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            result = None
            subprocess.Popen(
                [sys.executable, str(base_dir / "gui/error_dialog.py"), "".join(traceback.format_exception(error))],
                stdin = subprocess.DEVNULL,
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL,
                creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
        return result
    return wrapper
