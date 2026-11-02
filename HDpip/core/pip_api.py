"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件包含本包使用的所有pip API。
"""

import json
import pathlib
import yaml
import subprocess
import urllib.parse
import time
import urllib.request
from packaging.utils import parse_sdist_filename, parse_wheel_filename

try:
    from . import system
    from . import util
except ImportError:
    import system
    import util

def getPip(python: str | pathlib.Path = system.getPythonPath()) -> str:
    """
    获取指定Python对应的pip执行头。

    :param python: 指定的Python
    :type python: str | pathlib.Path
    :return: pip执行头
    :rtype: str
    """
    return f"\"{python}\" -m pip"

pip_head = getPip()

def version(pip_head: str = pip_head) -> dict[str, util.Version | pathlib.Path]:
    """
    返回运行`pip -V`的结果。

    :param pip_head: pip执行头
    :type pip_head: str
    :return: 数据字典
    :rtype: dict
    """

    string = system.shell(f"{pip_head} -V", False)
    string = util.multipleSpilt(string, ["pip ", " from ", " (python ", ")", "\r", "\n"])
    string_ = []
    for i in string:
        if not i == "":
            string_.append(i)
    result = {
        "pip_version": util.Version(string_[0]), 
        "pip_path": pathlib.Path(string_[1]), 
        "python_version": util.Version(string_[2]), 
    }
    return result

def list_(option: str | None = None, pip_head: str = pip_head) -> list:
    """
    返回运行`pip list --format=json`的结果。

    :param option: 额外参数
    :type option: str | None
    :param pip_head: pip执行头
    :type pip_head: str
    :return: 包列表
    :rtype: list
    """

    if not (option is None or option == ""):
        option = f" {option}"
    else:
        option = ""
    return json.loads(system.shell(f"{pip_head} list --format=json{option}", False, merge_error=False))

def show(package: str, pip_head: str = pip_head) -> dict:
    """
    返回运行`pip show`的结果。

    :param package: 要获取信息的包
    :type package: str
    :param pip_head: pip执行头
    :type pip_head: str
    :return: 包信息
    :rtype: dict
    """

    return yaml.safe_load(system.shell(f"{pip_head} show {package}", False, merge_error=False))

def getPackageDir(package: str, pythonPath: pathlib.Path | str = system.getPythonPath()) -> pathlib.Path:
    """
    返回包路径。

    :param package: 包名
    :type package: str
    :return: 包路径
    :rtype: pathlib.Path
    """

    pythonPath = pathlib.Path(pythonPath)

    if not system.isDev():
        return (system.getBaseDir().parent / package).resolve()
    else:
        return (pythonPath.parent / "Lib" / "site-packages" / package).resolve()

def install(package: str, callback=print, index: str | None = None, pip_head: str = pip_head) -> subprocess.Popen:
    """
    返回运行`pip install`的结果。

    :param package: 包名
    :type package: str
    :param callback: 回调函数
    :param index: 索引（镜像）
    :type index: str | None
    :param pip_head: pip执行头
    :return: 管道
    :rtype: subprocess.Popen
    """

    if not (index is None or index == ""):
        host = urllib.parse.urlparse(index).netloc
        option = f" -i {index} --trusted-host {host}"
    else:
        option = ""
    return system.shell(f"{pip_head} install {package}{option}", True, callback)

def uninstall(package: str, callback=print, pip_head: str = pip_head) -> subprocess.Popen:
    """
    返回运行`pip uninstall`的结果。

    :param package: 包名
    :type package: str
    :param callback: 回调函数
    :param pip_head: pip执行头
    :return: 管道
    :rtype: subprocess.Popen
    """

    return system.shell(f"{pip_head} uninstall {package} --yes")

def compareMirrorSpeed(mirrors: list[dict], timeout: float = 1.0) -> list[dict[str, str | float]]:
    """
    测试镜像源的响应速度。

    :param mirrors: 镜像列表，每项含 "url" 字段
    :type mirrors: list[dict]
    :param timeout: 超时时间
    :type timeout: float
    :return: 由快到慢的列表
    :rtype: list[dict]
    """

    results = []
    for mirror in mirrors:
        if mirror.get("test", False):
            continue
        url = mirror["url"]
        t0 = time.time()
        try:
            urllib.request.urlopen(url, timeout = timeout)
            elapsed = time.time() - t0
            results.append({"url": url, "time": elapsed})
        except Exception:
            results.append({"url": url, "time": timeout})

    return sorted(results, key=lambda x: x["time"])

def _parseJsonVersions(body: str) -> set[str] | None:
    """
    按 PEP 691 JSON 解析版本集合。

    :param body: 响应体
    :type body: str
    :return: 版本集合，不是合法结构时返回 None
    :rtype: set[str] | None
    """

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    versions = data.get("versions")
    if not isinstance(versions, list):
        return None
    return {str(v) for v in versions}

def _parseHtmlVersions(body: str) -> set[str]:
    """
    从 HTML 页面解析版本集合。

    :param body: 响应体
    :type body: str
    :return: 版本集合
    :rtype: set[str]
    """

    versions = set()
    for line in body.splitlines():
        for ext, parser in ((".tar.gz", parse_sdist_filename), (".whl", parse_wheel_filename)):
            if ext not in line:
                continue
            start = line.find(">") + 1
            end = line.find(ext + "<")
            if start > 0 and end > start:
                filename = line[start:end + len(ext)]
                try:
                    _, ver = parser(filename)
                    versions.add(str(ver))
                except Exception:
                    pass
    return versions

def getLatestVersion(package: str, mirror: str | None = None) -> util.Version | None:
    """
    通过 Simple API 获取最新版本，优先 JSON，回退 HTML。

    :param package: 包名
    :type package: str
    :param mirror: 镜像地址，默认官方 PyPI
    :type mirror: str | None
    :return: 最新版本，失败返回 None
    :rtype: util.Version | None
    """

    if not mirror:
        mirror = "https://pypi.org/simple/"

    url = mirror.rstrip("/") + f"/{package}/"
    req = urllib.request.Request(
        url, 
        headers={"Accept": "application/vnd.pypi.simple.v1+json"}, 
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    versions = _parseJsonVersions(body)
    if versions is None:
        versions = _parseHtmlVersions(body)

    if not versions:
        return None

    valid: list[util.Version] = []
    for v in versions:
        try:
            valid.append(util.Version(v))
        except Exception:
            pass

    if not valid:
        return None
    return max(valid)
