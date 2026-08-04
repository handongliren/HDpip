"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

SDK 函数 + 路径操作 + Version 类。
"""

import locale
import os
import pathlib
import platform
import subprocess
import sys
import traceback

import pip

try:
    from .. import version
except ImportError:
    base_dir = pathlib.Path(__file__).parents[1].resolve()
    sys.path.append(str(base_dir))
    from HDpip import version

try:
    from . import util
    from .util import Version
except ImportError:
    import util
    from util import Version

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
        raise util.HDpipError(f"打开\"{path}\"失败！\n错误如上。")

def isDev() -> bool:
    """
    检测是否是开发模式，如果启用，请在父目录创建`dev`文件。

    ***您不应该使用它**，如果您不是HDpip的开发者。*

    :return: 是否是开发模式
    :rtype: bool
    """

    return (pathlib.Path(f"{getBaseDir}").parent / "dev").resolve().is_file()

def shellDecode(raw: str | bytes) -> str:
    """
    对`HDpip.core.system.shell`的输出进行解码。

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
        print(HDpip.core.system.shell(
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
