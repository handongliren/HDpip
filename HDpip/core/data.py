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
from typing_extensions import overload, Self

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

    `__getitem__` 和 `__delitem__` 在键不存在时直接抛出 `KeyError`（`list` 越界抛 `IndexError`）；
    `__setitem__` 在目标键不存在时静默新增，路径中间层不存在时仍会抛出 `KeyError`/`IndexError`。

    `Data` 同时是可迭代对象和迭代器：`for x in data` 会重置游标从头遍历，
    `next(data)` 从当前游标继续取。嵌套迭代会共享同一游标，和文件对象一样。
    """

    def __init__(self):
        self.event_list = []
        self.file = {}
        self.data = None
        self._iterator: Iterator | None = None

    def open(self, file: str | pathlib.Path, encoding: str = "utf-8") -> dict[str, str]:
        """
        绑定一个`.json`文件，且返回绑定的文件字典。

        :param file: 一个指向`.json`文件的路径，如`data.json`
        :type file: str | pathlib.Path
        :param encoding: 编码字符串，如`utf-8`
        :type encoding: str
        :raises OSError: 路径无法解析为绝对路径时
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

        :raises FileNotFoundError: 绑定的文件不存在时
        :raises PermissionError: 没有读取权限时
        :raises json.JSONDecodeError: 文件内容不是合法 JSON 时
        :return: 数据
        :rtype: list | dict
        """

        with open(**self.file, mode="r") as f:
            self.data = json.load(f)
        self._iterator = None
        self.notifyEvent("load", {"data": self.data})
        return self.data

    def save(self) -> list | dict:
        """
        保存`.json`文件的数据至文件并返回。

        使用临时文件 + 原子替换，避免写入中途失败导致原文件损坏。

        :raises TypeError: 数据包含无法序列化为 JSON 的对象时
        :raises OSError: 写入临时文件或替换目标文件失败时
        :return: 数据
        :rtype: list | dict
        """

        target = pathlib.Path(self.file["file"])
        temp = target.with_suffix(target.suffix + ".tmp")
        with open(temp, mode="w", encoding=self.file["encoding"]) as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(", ", ": "))
        temp.replace(target)
        self.notifyEvent("save", {"data": self.data})
        return self.data

    def __iter__(self):
        """
        重置迭代游标并返回自身。

        每次 `for` 循环都会从头开始，但嵌套迭代会共享同一游标。
        """

        self._iterator = iter(self.data)
        return self

    def __next__(self):
        """
        返回下一个元素。

        首次调用时自动初始化游标；游标耗尽后抛出 `StopIteration`。

        :raises StopIteration: 数据已耗尽时
        :return: 下一个元素
        """

        if self._iterator is None:
            self._iterator = iter(self.data)
        return next(self._iterator)

    @overload
    def __getitem__(self, key: str | int): ...
    @overload
    def __getitem__(self, key: tuple | list): ...
    def __getitem__(self, key: str | int | tuple | list):
        """
        访问数据。键不存在时直接抛出 `KeyError` 或 `IndexError`。

        :param key: 键，可以是字符串、整数，或由它们组成的路径
        :type key: str | int | tuple | list
        :raises KeyError: 字典键不存在时
        :raises IndexError: 列表索引越界时
        :raises TypeError: 键类型不受支持时
        :return: 对应的值
        """

        if isinstance(key, str | int):
            result = self.data[key]
        elif isinstance(key, tuple | list):
            result = self.data
            for i in key:
                result = result[i]
        else:
            raise TypeError(f"不支持的键类型：{type(key).__name__}")
        self.notifyEvent("__getitem__", {"key": key, "value": result})
        return result

    @overload
    def __setitem__(self, key: str | int, value: Any): ...
    @overload
    def __setitem__(self, key: tuple | list, value: Any): ...
    def __setitem__(self, key: str | int | tuple | list, value: Any):
        """
        设置数据。

        目标键不存在时静默新增，`old_value` 为 `None`。
        路径中间层不存在时抛出 `KeyError` 或 `IndexError`，因为无法推断中间层应创建 `dict` 还是 `list`。

        :param key: 键，可以是字符串、整数，或由它们组成的路径
        :type key: str | int | tuple | list
        :param value: 新值
        :type value: Any
        :raises KeyError: 嵌套路径的中间层键不存在时
        :raises IndexError: 嵌套路径的中间层索引越界时
        :raises ValueError: 键为空 tuple/list 时
        :raises TypeError: 键类型不受支持时
        """

        if isinstance(key, str | int):
            try:
                old_value = self.data[key]
            except (KeyError, IndexError):
                old_value = None
            self.data[key] = value
        elif isinstance(key, tuple | list):
            if not key:
                raise ValueError("键不能为空。")
            parent = self.data
            for i in key[:-1]:
                parent = parent[i]
            try:
                old_value = parent[key[-1]]
            except (KeyError, IndexError):
                old_value = None
            parent[key[-1]] = value
        else:
            raise TypeError(f"不支持的键类型：{type(key).__name__}")
        self._iterator = None
        self.notifyEvent("__setitem__", {"key": key, "value": value, "old_value": old_value})
        return None

    @overload
    def __delitem__(self, key: str | int): ...
    @overload
    def __delitem__(self, key: tuple | list): ...
    def __delitem__(self, key: str | int | tuple | list):
        """
        删除数据并返回被删除的值。

        键不存在时直接抛出 `KeyError`（`list` 越界抛 `IndexError`）。

        :param key: 键，可以是字符串、整数，或由它们组成的路径
        :type key: str | int | tuple | list
        :raises KeyError: 字典键不存在时
        :raises IndexError: 列表索引越界时
        :raises ValueError: 键为空 tuple/list 时
        :raises TypeError: 键类型不受支持时
        :return: 被删除的值
        """

        if isinstance(key, str | int):
            old_value = self.data[key]
            del self.data[key]
        elif isinstance(key, tuple | list):
            if not key:
                raise ValueError("键不能为空。")
            parent = self.data
            for i in key[:-1]:
                parent = parent[i]
            old_value = parent[key[-1]]
            del parent[key[-1]]
        else:
            raise TypeError(f"不支持的键类型：{type(key).__name__}")
        self._iterator = None
        self.notifyEvent("__delitem__", {"key": key, "old_value": old_value})
        return old_value

    def __eq__(self, value: list | dict | Self):
        """
        比较相等。

        - 与另一个 `Data` 比较时，同时比较 `file` 和 `data`
        - 与裸 `list`/`dict` 比较时，只比较底层数据
        - 其他类型返回 `NotImplemented`
        """

        if isinstance(value, self.__class__):
            return self.file == value.file and self.data == value.data
        elif isinstance(value, (list, dict)):
            return self.data == value
        else:
            return NotImplemented

    def __add__(self, value: list | dict | Self):
        """
        返回合并后的新 `Data`，不修改原对象。

        字典合并为顶层键覆盖（`dict.update`），列表合并为拼接。

        :param value: 要合并的数据
        :type value: list | dict | Self
        :raises TypeError: 底层数据类型不匹配时
        :return: 合并后的新 `Data`
        :rtype: Self
        """

        result = copy.deepcopy(self)
        result._iterator = None
        if isinstance(value, self.__class__):
            value = value.data
        if isinstance(self.data, list) and isinstance(value, list):
            result.data = self.data + value
        elif isinstance(self.data, dict) and isinstance(value, dict):
            result.data.update(value)
        else:
            raise TypeError(f"本Data类存取的数据为{type(self.data).__name__}类型，但您尝试合并一个{type(value).__name__}类型！")
        self.notifyEvent("__add__", {"value": value, "result": result})
        return result

    def __iadd__(self, value: list | dict | Self):
        """
        原地合并并返回自身。

        字典合并为顶层键覆盖（`dict.update`），列表合并为拼接。

        :param value: 要合并的数据
        :type value: list | dict | Self
        :raises TypeError: 底层数据类型不匹配时
        :return: 自身
        :rtype: Self
        """

        if isinstance(value, self.__class__):
            value = value.data
        if isinstance(self.data, list) and isinstance(value, list):
            self.data += value
        elif isinstance(self.data, dict) and isinstance(value, dict):
            self.data.update(value)
        else:
            raise TypeError(f"本Data类存取的数据为{type(self.data).__name__}类型，但您尝试合并一个{type(value).__name__}类型！")
        self._iterator = None
        self.notifyEvent("__iadd__", {"value": value})
        return self

    def registerEvent(self, callback: Callable[[str, dict[str, Any]], Any]):
        """
        注册事件回调函数。

        :param callback: 回调函数，接收两个参数：(`event_type`, `event_data`)
        :type callback: Callable[[str, dict[str, Any]], Any]

        **event_type**

        `open`, `load`, `save`, `__getitem__`, `__setitem__`, `__delitem__`, `__add__`, `__iadd__`

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
                "old_value": Any      # 原来的值，键不存在时为 None
            }
        ```

        - `__delitem__`:
        ```
            {
                "key": str | int,     # 删除的键
                "old_value": Any      # 被删除的值
            }
        ```

        - `__add__`:
        ```
            {
                "value": dict | list | Data,  # 被合并的数据
                "result": Data                # 合并后的结果
            }
        ```

        - `__iadd__`:
        ```
            {
                "value": dict | list | Data  # 被合并的数据
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
            "__add__", 
            "__iadd__"
        ], 
        event_data: dict[str, Any]
    ):
        """
        通知所有事件。

        单个观察者抛出的异常会被捕获并打印，不影响其他观察者。

        :param event_type: 事件类型
        :type event_type: Literal["open", "load", "save", "\\_\\_getitem\\_\\_", "\\_\\_setitem\\_\\_", "\\_\\_delitem\\_\\_", "\\_\\_add\\_\\_", "\\_\\_iadd\\_\\_"]
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
        :raises OSError: 复制文件失败时
        :raises json.JSONDecodeError: 导入的文件不是合法 JSON 时
        """

        path = pathlib.Path(path).resolve()
        shutil.copy(path, self.custom_setting)
        self.setting.load()

    def exportSetting(self, path: str | pathlib.Path) -> None:
        """
        导出设置。

        :param path: 路径
        :type path: str | pathlib.Path
        :raises OSError: 复制文件失败时
        """

        path = pathlib.Path(path).resolve()
        shutil.copy(self.custom_setting, path)

    def generateLanguageDict(self) -> dict[str, pathlib.Path]:
        """
        生成语言字典。

        :raises OSError: 默认语言目录不可读时
        :return: 语言字典
        :rtype: dict[str: Path]
        """

        default_language_list = list(self.default_language_dir.iterdir())
        custom_language_list = list(self.custom_language_dir.iterdir()) if self.custom_language_dir.is_dir() else []
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
        :raises FileNotFoundError: 未找到对应语言代码的语言文件时
        :raises json.JSONDecodeError: 语言文件不是合法 JSON 时
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
        :raises OSError: 创建目录或复制文件失败时
        """

        path = pathlib.Path(path).resolve()
        self.custom_language_dir.mkdir(parents=True, exist_ok=True)
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

    def init(self, must=False):
        """
        设置基本数据并初始化。

        已初始化后重复调用不会重建内存数据，共用同一数据管理器时已注册事件不会被清除。

        :param must: 是否强制初始化（*这将会覆盖用户数据！*）
        :type must: bool
        :raises OSError: 创建目录或复制默认设置失败时
        :raises json.JSONDecodeError: 设置或语言文件不是合法 JSON 时
        """

        if must or not self.isInited():
            self.custom_setting.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.default_setting, self.custom_setting)
            self.custom_language_dir.mkdir(parents=True, exist_ok=True)

        if must or not hasattr(self, "setting"):
            self.setting = Data()
            self.setting.open(self.custom_setting)
            self.setting.load()

            self.language_dict = self.generateLanguageDict()
            self.language = Data()
            self.getLanguage(self.setting["language"])
            self.setting.registerEvent(self.onLanguageChange)

data_manager = DataManager()

def isBelongedToHDpip(path: pathlib.Path) -> bool:
    """
    判断一个路径是否属于HDpip。

    :param path: 路径
    :type path: pathlib.Path
    :return: 结果
    :rtype: bool
    """

    return any(path.is_relative_to(p) for p in [system.getBaseDir(), system.getPythonPath().parent / "HDpip"])
