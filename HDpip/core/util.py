"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

纯工具函数，不依赖 HDpip 其他模块。
"""

import pip._vendor.packaging.version
from typing import *
from typing_extensions import override, overload

class HDpipError(Exception):
    """
    抛出一个HDpip错误，初始化函数可以接受一个`message`参数。

    例如：
    ```
    raise HDpip.core.util.HDpipError("炸了！")
    ```

    ***您不应该使用它**，如果您不是HDpip的开发者。*
    """

    def __init__(self, message = None) -> None:
        self.message = message
        super().__init__(self.message)

def unfinished() -> None:
    """
    用于未完成功能的占位，使用`HDpipError`抛出一个错误。
    """

    raise HDpipError("不是，哥们，你写了这个功能吗？！")

class Version(pip._vendor.packaging.version.Version):
    """
    版本类，继承 pip 的 Version，支持 PEP 440。

    >>> Version("0.1.0")
    0.1.0
    """

    @overload
    def __init__(self, version: str): ...
    @overload
    def __init__(self, version: tuple[str, int] | list[str | int]): ...
    @override
    def __init__(self, version: str | tuple[str, int] | list[str | int]):
        if isinstance(version, (tuple, list)):
            version = ".".join(str(x) for x in version)
        super().__init__(version)

    @override
    def __len__(self):
        return len(self.release)

    @override
    def __iter__(self):
        return iter(self.release)

    @override
    def __getitem__(self, key):
        return self.release[key]

    @overload
    def isCloseTo(self, value: str): ...
    @overload
    def isCloseTo(self, value: tuple[int, str] | list[str | int]): ...
    @override
    def isCloseTo(self, value: str | tuple[int, str] | list[str | int]) -> bool:
        """
        富比较中的约等于（默认比较前两位）。

        >>> Version("0.1.0").isCloseTo("0.1.1")
        True

        :param self: `Version`类
        :param value: 另一个版本
        :type value: Version | str | tuple[int, str] | list[str | int]
        :return: 结果
        :rtype: bool
        """

        if not isinstance(value, Version):
            value = Version(value)
        if not isinstance(value, Version):
            value = Version(value)
        return self.release[:2] == value.release[:2]

    def multipleCompare(self, standard: str | list[str]) -> bool:
        """
        多重富比较，即开即用。

        >>> version = Version("0.1.0")
        "0.1.0"

        >>> version.multipleCompare(">0.0.0,<2,~=0.1.1,!=0.1.5")
        True

        >>> version.multipleCompare([">0.0.0", "<2", "~=0.1.1", "!=0.1.5"])
        True

        :param self: `Version`类
        :param standard: 富比较标准
        :type standard: str | list[str]
        :return: 结果
        :rtype: bool
        """

        if isinstance(standard, str):
            standard = standard.split(",")
        for i in standard:
            mode = i[:2]
            if not mode in ["==", "!=", "~=", ">=", "<="]:
                mode = i[:1]
                if not mode in [">", "<"]:
                    mode = "=="
                    value = Version(i)
                else:
                    value = Version(i[1:])
            else:
                value = Version(i[2:])

            if mode == "==" and not self == value:
                return False
            elif mode == "!=" and not self != value:
                return False
            elif mode == "~=" and not self.isCloseTo(value):
                return False
            elif mode == ">" and not self > value:
                return False
            elif mode == "<" and not self < value:
                return False
            elif mode == ">=" and not self >= value:
                return False
            elif mode == "<=" and not self <= value:
                return False
        return True

def multipleSpilt(string: str, spilt_symbol: str | list[str]) -> list[str]:
    """
    按照多个分隔符分割字符串，请输入如同`"|,."`或`["|", "."]`的分隔符，`str`模式以`,`分割列表。

    :param string: 字符串
    :type string: str
    :param spilt_symbol: 分隔符字符串或列表
    :type spilt_symbol: str | list[str]
    :return: 结果
    :rtype: list[str]
    """
    if isinstance(spilt_symbol, str):
        spilt_symbol = spilt_symbol.split(",")

    if len(spilt_symbol) == 0:
        ValueError("分隔符列表不能为空！")
    elif len(spilt_symbol) > 1:
        for i in range(1, len(spilt_symbol)):
            string = string.replace(spilt_symbol[i], spilt_symbol[0])
    return string.split(spilt_symbol[0])
