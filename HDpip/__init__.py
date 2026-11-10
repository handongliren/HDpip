"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3
"""

from types import ModuleType
from typing import TYPE_CHECKING

from .info import (
    __version__, __author__, __copyright__, 
    version, author, copyright
)

if TYPE_CHECKING:
    from . import core, gui

def __getattr__(name: str) -> ModuleType:
    """
    按需加载 `core` 和 `gui` 子包，避免 `import HDpip` 时拖入 GUI 链。

    `import HDpip` 只加载 `info`，不触发 `maliang`、`tkinter` 等重型依赖。
    首次访问 `HDpip.core` 或 `HDpip.gui` 时，通过 `importlib` 加载对应子包，
    之后由 Python 缓存到 `HDpip.__dict__`，不再经过本函数。

    :param name: 属性名
    :type name: str
    :raises AttributeError: 属性名不是 `core` 或 `gui` 时
    :return: 对应的子包模块
    :rtype: ModuleType
    """

    if name in ("core", "gui"):
        import importlib
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
