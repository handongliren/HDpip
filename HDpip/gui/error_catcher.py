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

def catch(func: Callable[..., Any] | None = None, *, auto_close: int = 0):
    """
    装饰器，用于捕捉错误并显示对话框。

    :param func: 装饰的函数
    :type func: Callable[..., Any]
    :return: 装饰后的函数
    :rtype: _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any | None]
    """

    def _decorate(f: Callable[..., Any], *, auto_close: int = -1):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as error:
                auto_close = auto_close
                auto_close_arg = ["--auto-close", str(auto_close)] if auto_close and auto_close >= 0 else []

                subprocess.Popen(
                    [sys.executable, str(base_dir / "gui/error_dialog.py"), "--text", "".join(traceback.format_exception(error))] + auto_close_arg,
                    stdin = subprocess.DEVNULL,
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL,
                    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                return None

        return wrapper

    if func is None:
        return lambda f: _decorate(f, auto_close = auto_close)
    else:
        return _decorate(func, auto_close = auto_close)
