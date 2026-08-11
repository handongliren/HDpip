"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于类型检查验证。
"""

from HDpip.gui.custom import utility

# 标量分岔
a = utility.smartScale(100)
b = utility.smartScale(100, return_type = "Decimal")
c = utility.smartScale(100, return_type = "float")

# Iterable 分岔
d = utility.smartScale((1, 1))
e = utility.smartScale((1, 1), return_type = "Decimal")
f = utility.smartScale([1, 2], return_type = "float")

reveal_type(a)
reveal_type(b)
reveal_type(c)
reveal_type(d)
reveal_type(e)
reveal_type(f)
