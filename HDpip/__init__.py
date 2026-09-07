"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3
"""

try:
    from .info import (
        __version__, __author__, __copyright__,
        version, author, copyright
    )
except ImportError:
    from info import (
        __version__, __author__, __copyright__,
        version, author, copyright
    )

from . import core, gui
