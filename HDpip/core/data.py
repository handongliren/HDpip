"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

Data 数据系统。
"""

import copy
import json
import pathlib
import shutil
import traceback
from typing import *
from typing_extensions import overload

try:
    from . import system
except ImportError:
    import system

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

    @overload
    def __getitem__(self, key: str | int): ...
    @overload
    def __getitem__(self, key: tuple | list): ...
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

    @overload
    def __setitem__(self, key: str | int, value: Any): ...
    @overload
    def __setitem__(self, key: tuple | list, value: Any): ...
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

    @overload
    def __delitem__(self, key: str | int): ...
    @overload
    def __delitem__(self, key: tuple | list): ...
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
        self.default_setting = (system.getBaseDir() / "setting" / "global.json").resolve()
        self.custom_setting = (system.getPythonPath().parent / "HDpip" / "setting.json").resolve()
        self.language_code_dict = {
            "en": "English",
            "zh-CN": "简体中文",
            "zh-TW": "繁體中文",
            "ko": "한국어",
            "fr": "Français",
            "de": "Deutsch",
            "es": "Español",
            "ru": "Русский",
            "ar": "العربية",
            "hi": "हिन्दी"
        }
        self.default_language_dir = (system.getBaseDir() / "language").resolve()
        self.custom_language_dir = (system.getPythonPath().parent / "HDpip" / "language").resolve()

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

    return any(path.is_relative_to(p) for p in [system.getBaseDir(), system.getPythonPath().parent / "HDpip"])
