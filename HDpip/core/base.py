"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件包含本包所有的基础功能，~~全是屎山💩~~。
"""

import pathlib
import os
import sys
import traceback
import json
import platform
import pip._vendor.packaging.version
import subprocess
import locale
import shutil
import copy
from typing import *
import pathlib

try:
    from .. import version
except ImportError:
    base_dir = pathlib.Path(__file__).parents[1].resolve()
    sys.path.append(str(base_dir))
    from HDpip import version

class HDpipError(Exception):
    """
    抛出一个HDpip错误，初始化函数可以接受一个`message`参数。

    例如：
    ```
    raise HDpip.core.base.HDpipError("炸了！")
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


class Data():
    """
    接受一个`.json`文件（使用`open`函数打开文件，并使用`load`函数加载。），生成一个数据类。

    但是，您应该如此获得数据：

    ```
    d = Data()
    d.open("data.json")
    d.load() #这是必须的，因为在open后不会自动运行load函数。
    print(d["a"][0])
    ```

    您可以便捷地使用`==`运算符判断相等或使用`+`运算符合并数据，还支持事件管理，可以注册回调函数来监听事件。

    实际上，由于我写了点神奇的代码，以下写法也可行：

    ```
    d["a", 0]
    ```

    等同于：

    ```
    d["a"][0]
    ```
    """

    def __init__(self):
        self.event_list = []
        self.file = {}
        self.data = None

    def open(self, file: str | pathlib.Path, encoding: str = "utf-8") -> dict[str, str]:
        """
        绑定一个`.json`文件，且返回绑定的文件字典。

        :param self: `Data`类
        :param file: 一个指向`.json`文件的路径，如`data.json`
        :type file: str | pathlib.Path
        :param encoding: 编码字符串，如`utf-8`
        :type encoding: str
        :return: 文件字典
        :rtype: dict[str, str]
        """

        file = str(pathlib.Path(file).resolve())
        self.file = {"file": file, "encoding": encoding}
        self.notifyEvent("open", self.file)
        return self.file

    def load(self) -> list | dict:
        """
        加载`.json`文件的数据至数据类并返回。

        :param self: `Data`类
        :return: 数据
        :rtype: list | dict
        """

        with open(**self.file, mode = "r") as f:
            self.data = json.load(f)
        self.notifyEvent("load", {"data": self.data})
        return self.data

    def save(self) -> list | dict:
        """
        保存`.json`文件的数据至文件并返回。

        :param self: `Data`类
        :return: 数据
        :rtype: list | dict
        """

        with open(**self.file, mode = "w") as f:
            json.dump(self.data, f)
        self.notifyEvent("save", {"data": self.data})
        return self.data

    def __iter__(self):
        return self.data.__iter__()

    def __next__(self):
        return self.data.__next__()

    def __getitem__(self, key: str | int | tuple | list):
        if isinstance(key, str | int):
            result = value = self.data.__getitem__(key)
        elif isinstance(key, tuple | list):
            result = self.data
            for i in key:
                result = result.__getitem__(i)
                value = result
        self.notifyEvent("__getitem__", {"key": key, "value": value})
        return result

    def __setitem__(self, key: str | int | tuple | list, value: Any):
        if isinstance(key, str | int):
            old_value = self.data.__getitem__(key) or None
            result = self.data.__setitem__(key, value)
        elif isinstance(key, tuple | list):
            result = self.data
            for i in range(0, len(key)):
                if i == len(key) - 1:
                    old_value = result.__getitem__(key[i]) or None
                    result.__setitem__(key[i], value)
                else:
                    result = result.__getitem__(key[i])
        self.notifyEvent("__setitem__", {"key": key, "value": value, "old_value": old_value})
        return result

    def __delitem__(self, key: str | int | tuple | list):
        if isinstance(key, str | int):
            old_value = self.data[key] or None
            result = old_value = self.data.__delitem__(key)
        elif isinstance(key, tuple | list):
            result = self.data
            for i in range(0, len(key)):
                if i == len(key) - 1:
                    old_value = result.__getitem__(key[i]) or None
                    result.__delitem__(key[i])
                else:
                    result = result.__getitem__(key[i])
        self.notifyEvent("__delitem__", {"key": key, "old_value": old_value})
        return result

    def __eq__(self, value):
        return self.file == value.file and self.data == self.data

    def __add__(self, value: list | dict):
        result = copy.deepcopy(self)
        if isinstance(value, Data):
            value = value.data
        if isinstance(self.data, list) and isinstance(value, list):
            result.data = self.data + value
        elif isinstance(self.data, dict) and isinstance(value, dict):
            result.data.update(value)
        else:
            raise TypeError(f"本Data类存取的数据为{type(self.data).__name__}类型，但您尝试合并一个{type(value).__name__}类型！")
        self.notifyEvent("__add__", {"value": value, "result": result})
        return result

    def __iadd__(self, value: list | dict):
        if isinstance(value, Data):
            value = value.data
        if isinstance(self.data, list) and isinstance(value, list):
            self.data += value
        elif isinstance(self.data, dict) and isinstance(value, dict):
            self.data.update(value)
        else:
            raise TypeError(f"本Data类存取的数据为{type(self.data).__name__}类型，但您尝试合并一个{type(value).__name__}类型！")
        self.notifyEvent("__iadd__", {"value": value})
        return self

    def registerEvent(self, callback: Callable[[str, dict[str, Any]], Any]):
        """
        注册事件回调函数。

        :param callback: 回调函数，接收两个参数：(`event_type`, `event_data`)
        :type callback: Callable[[str, dict[str, Any]], Any]

        **event_type**

        `open`, `load`, `save`, `__getitem__`, `__setitem__`, `__delitem__`, `__add__`

        **event_data**

        根据不同的事件类型，event_data包含不同的数据：

        - `open`:
        ```
            {
                "file": str,      # 文件路径
                "encoding": str   # 编码格式
            }
        ```

        - `load`:
        ```
            {
                "data": dict | list  # 加载的数据
            }
        ```

        - `save`:
        ```
            {
                "data": dict | list  # 保存的数据
            }
        ```

        - `__getitem__`:
        ```
            {
                "key": str | int,     # 访问的键
                "value": Any          # 获取的值
            }
        ```

        - `__setitem__`:
        ```
            {
                "key": str | int,     # 设置的键
                "value": Any,         # 新设置的值
                "old_value": Any      # 原来的值（如果存在）
            }
        ```

        - `__delitem__`:
        ```
            {
                "key": str | int,     # 删除的键
                "old_value": Any      # 被删除的值（如果存在）
            }
        ```

        - `__add__`:
        ```
            {
                "value": dict | list | Data,  # 被合并的数据
                "result": Data                # 合并后的结果
            }
        ```
        """

        if callback not in self.event_list:
            self.event_list.append(callback)

    def unregisterEvent(self, callback: Callable[[str, dict[str, Any]], Any]):
        """
        注销事件回调函数。

        :param callback: 要注销的回调函数
        :type callback: Callable[[str, dict[str, Any]], Any]
        """

        if callback in self.event_list:
            self.event_list.remove(callback)

    def notifyEvent(
        self,
        event_type: Literal[
            "open",
            "load",
            "save",
            "__getitem__",
            "__setitem__",
            "__delitem__",
            "__add__"
        ],
        event_data: dict[str, Any]
    ):
        """
        通知所有事件。

        :param event_type: 事件类型
        :type event_type: Literal["open", "load", "save", "\\_\\_getitem\\_\\_", "\\_\\_setitem\\_\\_", "\\_\\_delitem\\_\\_", "\\_\\_add\\_\\_"]
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        for observer in self.event_list[:]:
            try:
                observer(event_type, event_data)
            except Exception as error:
                traceback.print_exception(error)

def getBaseDir() -> pathlib.Path:
    """
    获取HDpip的根目录，即`main.py`所在目录。

    :return: 路径
    :rtype: pathlib.Path
    """

    return pathlib.Path(__file__).parents[1]

def getPythonPath() -> pathlib.Path:
    """
    获取运行HDpip的Python的路径。

    :return: 路径
    :rtype: pathlib.Path
    """

    return pathlib.Path(sys.executable)

class Version(pip._vendor.packaging.version.Version):
    """
    版本类，继承 pip 的 Version，支持 PEP 440。

    >>> Version("0.1.0")
    0.1.0
    """

    def __init__(self, version: str | tuple[str, int] | list[str | int]):
        if isinstance(version, (tuple, list)):
            version = ".".join(str(x) for x in version)
        super().__init__(version)

    def __len__(self):
        return len(self.release)

    def __iter__(self):
        return iter(self.release)

    def __getitem__(self, key):
        return self.release[key]

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

        如你所见，`~=`和`!=`**都是支持的**。

        对于`==`模式，可以不写`==`，如`version.multipleCompare("0.1.0,>0.0.0")`，但为何不直接用富比较呢？

        :param self: `Version`类
        :param standard: 富比较标准
        :type standard: str | list[str]
        :return: 结果
        :rtype: bool | NotImplemented
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

def getPythonVersion() -> Version:
    """
    获取运行HDpip的Python的版本。

    :return: 版本
    :rtype: Version
    """

    return Version(platform.python_version_tuple())

def getPipVersion() -> Version:
    """
    获取运行HDpip的Python所对应的pip的版本。

    :return: 版本
    :rtype: Version
    """

    return Version(pip.__version__)

def getVersion() -> Version:
    """
    获取HDpip的版本。

    :return: 版本
    :rtype: Version
    """

    return Version(version)

def getSystemVersion() -> str:
    """
    获取系统详细版本，三平台统一格式。

    :return: 系统版本字符串，如 \"Windows 10 x64\"
    :rtype: str
    """

    system = platform.system()
    machine = platform.machine()

    if system == "Windows":
        win_ver = platform.win32_ver()
        return f"Windows {win_ver[1]} ({machine})"
    elif system == "Darwin":
        mac_ver = platform.mac_ver()
        return f"macOS {mac_ver[1]} ({machine})"
    else:
        release = platform.release()
        return f"Linux {release} ({machine})"

def openInExplorer(path: str | pathlib.Path) -> None:
    """
    在文件资源管理器中打开一个文件夹或文件（Windows下选中，Linux或MacOS下打开父文件夹。）。

    :param path: 要打开的文件夹
    :type path: str | pathlib.Path
    """

    path = pathlib.Path(path).resolve()
    system = platform.system()
    if system != "Windows" and path.is_file():
        path = path.parent.resolve()

    try:
        if system == "Windows":
            if path.is_file():
                os.system(f"explorer /select, \"{path}\"")
            else:
                os.startfile(path)
        elif system == "Linux":
            os.system(f"xdg-open \"{path}\"")
        elif system == "Darwin":
            os.system(f"open \"{path}\"")
        else:
            raise NotImplementedError(f"不支持的系统：{system}！")
    except Exception as error:
        traceback.print_exception(error)
        raise HDpipError(f"打开\"{path}\"失败！\n错误如上。")

def shellDecode(raw: str | bytes) -> str:
    """
    对`HDpip.core.base.shell`的输出进行解码。

    :param raw: 原始数据
    :type raw: str | bytes
    :return: 解码结果
    :rtype: str
    """

    for encoding in [locale.getpreferredencoding(), "utf-8", "cp936", "gbk", "gb2312", "big5"]:
        try:
            return bytes(raw).decode(encoding)
        except TypeError:
            return raw
        except UnicodeDecodeError:
            continue
    return bytes(raw).decode("latin-1", errors="replace")

def shell(command: str, realtime: bool = True, callback = print) -> str:
    """
    使用系统shell运行一条指令，每输出一行，如果启用实时模式，运行以更新行为输入的回调函数，并返回标准输出。

    **注意，*禁止运行交互式命令！***

    例如：
    ```
    with open("result.txt", "a", encoding = "utf-8") as file:
        print(HDpip.core.base.shell(
            "ping 127.0.0.1",
            lambda line: file.write(f"{line}\n")
        ).returncode)
    ```

    :param command: 命令
    :type command: str
    :param realtime: 实时模式
    :type realtime: bool
    :param callback: 回调函数
    :return: 标准输出
    :rtype: str
    """

    if realtime:
        popen = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True,
            shell = True
        )
        for line in popen.stdout:
            callback(line.strip())
    else:
        popen = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            text = True,
            shell = True
        )
    return shellDecode(popen.communicate()[0])

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

def isDev() -> bool:
    """
    检测是否是开发模式，如果启用，请在父目录创建`dev`文件。

    ***您不应该使用它**，如果您不是HDpip的开发者。*

    :return: 是否是开发模式
    :rtype: bool
    """

    return (pathlib.Path(f"{getBaseDir}").parent / "dev").resolve().is_file()

class DataManager():
    def importSetting(self, path: str | pathlib.Path) -> None:
        """
        导入设置。

        :param path: 路径
        :type path: str | pathlib.Path
        """

        path = pathlib.Path(path).resolve()
        shutil.copy(path, self.custom_setting)
        self.setting.load()

    def exportSetting(self, path: str | pathlib.Path) -> None:
        """
        导出设置。

        :param path: 路径
        :type path: str | pathlib.Path
        """

        path = pathlib.Path(path).resolve()
        shutil.copy(self.custom_setting, path)

    def generateLanguageDict(self) -> dict[str, pathlib.Path]:
        """
        生成语言字典。

        :return: 语言字典
        :rtype: dict[str: Path]
        """

        default_language_list = list(self.default_language_dir.iterdir())
        custom_language_list = list(self.custom_language_dir.iterdir())
        language_list = default_language_list + custom_language_list
        language_dict = {}
        for i in language_list:
            language_dict[i.stem] = i
        return language_dict

    def getLanguage(self, language_code: str) -> None:
        """
        通过语言代码获取语言数据。

        :param language_code: 语言代码
        :type language_code: str
        """

        try:
            self.language.open(self.language_dict[language_code])
            self.language.load()
        except KeyError:
            raise FileNotFoundError(f"未找到语言代码为{language_code}的语言文件！")

    def importLanguage(self, path: str | pathlib.Path) -> None:
        """
        导入语言。

        :param path: 路径
        :type path: str | pathlib.Path
        """

        path = pathlib.Path(path).resolve()
        shutil.copy(path, self.custom_language_dir / path.name)
        self.language_dict = self.generateLanguageDict()

    def isInited(self) -> bool:
        """
        返回是否已经初始化。

        :return: 是否已经初始化
        :rtype: bool
        """

        if not self.custom_setting.is_file():
            return False
        if not self.custom_language_dir.is_dir():
            return False
        return True

    def onLanguageChange(self, event_type: str, event_data: dict):
        if event_type == "__setitem__" and event_data["key"] == "language":
            self.getLanguage(event_data["value"])
        elif event_type == "load":
            self.getLanguage(self.setting["language"])

    def __init__(self):
        self.default_setting = (getBaseDir() / "setting" / "global.json").resolve()
        self.custom_setting = (getPythonPath().parent / "HDpip" / "setting.json").resolve()
        self.language_code_dict = {
            "en": "English",
            "zh-CN": "简体中文",
            "zh-TW": "繁體中文",
            # "ja": "日本語",
            # 由于日本军国主义复苏，日本正在严重威胁亚太地区和平稳定，出于全球开源精神，予以制裁。
            "ko": "한국어",
            "fr": "Français",
            "de": "Deutsch",
            "es": "Español",
            "ru": "Русский",
            "ar": "العربية",
            "hi": "हिन्दी"
        }
        self.default_language_dir = (getBaseDir() / "language").resolve()
        self.custom_language_dir = (getPythonPath().parent / "HDpip" / "language").resolve()

    def init(self, must = False):
        """
        设置基本数据并初始化。

        :param must: 是否强制初始化（*这将会覆盖用户数据！*）
        :type must: bool
        """

        if must or not self.isInited():
            self.custom_setting.parent.mkdir(exist_ok = True)
            shutil.copy(self.default_setting, self.custom_setting)
            self.custom_language_dir.mkdir(exist_ok = True)

        self.setting = Data()
        self.setting.open(self.custom_setting)
        self.setting.load()

        self.language_dict = self.generateLanguageDict()
        self.language = Data()
        self.getLanguage(self.setting["language"])
        self.setting.registerEvent(self.onLanguageChange)

def isBelongedToHDpip(path: pathlib.Path) -> bool:
    """
    判断一个路径是否属于HDpip。

    :param path: 路径
    :type path: pathlib.Path
    :return: 结果
    :rtype: bool
    """

    return any(path.is_relative_to(p) for p in [getBaseDir(), getPythonPath().parent / "HDpip"])
