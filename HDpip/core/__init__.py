"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本模块是本包核心。
"""

import sys as _sys

from . import data as _data
from . import system as _system
from . import util as _util

class _BaseProxy:
    """兼容旧 core.base 引用，透明代理到 util / system / data。"""

    _modules = [_util, _system, _data]

    def __getattr__(self, name):
        for mod in self._modules:
            if hasattr(mod, name):
                return getattr(mod, name)
        raise AttributeError(f"module 'HDpip.core.base' has no attribute '{name}'")

base = _BaseProxy()
_sys.modules["HDpip.core.base"] = base

from . import pip_api
