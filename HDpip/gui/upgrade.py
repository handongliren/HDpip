"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是更新器。
"""

from typing import *
from typing_extensions import override
import importlib.metadata
import json
import os
import pathlib
import queue
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import threading
import time
import traceback

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    __package__ = "HDpip.gui"

import maliang.core.configs
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

from .. import core

from . import custom, dialog
from .custom.util import ss
from .custom.media import bi

current_version = core.system.getVersion()

latest_version: core.util.Version | None = None
latest_failed = False
_latest_event = threading.Event()
_latest_thread: threading.Thread | None = None
_latest_lock = threading.Lock()

def _creationFlags() -> int:
    """
    返回子进程创建标志，Windows 下隐藏控制台窗口。

    :return: 创建标志
    :rtype: int
    """

    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

def _siteMain() -> pathlib.Path:
    """
    返回已安装包的 `main.py` 路径。

    :return: 路径
    :rtype: pathlib.Path
    """

    try:
        distribution = importlib.metadata.distribution("hdpip")
        return pathlib.Path(distribution.locate_file("HDpip/main.py")).resolve()
    except importlib.metadata.PackageNotFoundError:
        return (pathlib.Path(sysconfig.get_path("purelib")) / "HDpip" / "main.py").resolve()

def _copyRoot(data_manager: core.data.DataManager = core.data.data_manager) -> pathlib.Path:
    """
    返回更新副本根目录，即 `Python310/HDpip/copy/`。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 更新副本根目录
    :rtype: pathlib.Path
    """

    return (data_manager.custom_setting.parent / "copy").resolve()

def _statePath(data_manager: core.data.DataManager = core.data.data_manager) -> pathlib.Path:
    """
    返回更新状态文件路径。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 状态文件路径
    :rtype: pathlib.Path
    """

    return _copyRoot(data_manager) / "state.json"

def _readState(data_manager: core.data.DataManager = core.data.data_manager) -> dict[str, Any] | None:
    """
    读取更新状态。

    文件不存在、不是合法 JSON、不是字典或缺少字段时返回 `None`。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 状态字典，失败返回 `None`
    :rtype: dict[str, Any] | None
    """

    try:
        with open(_statePath(data_manager), "r", encoding = "utf-8") as file:
            state = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(state, dict):
        return None
    for key in ("from_version", "to_version", "attempts"):
        if key not in state:
            return None
    try:
        int(state["attempts"])
        str(state["from_version"])
        str(state["to_version"])
    except (TypeError, ValueError):
        return None
    return state

def _writeState(state: dict[str, Any], data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    写入更新状态。

    :param state: 状态字典
    :type state: dict[str, Any]
    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :raises OSError: 写入失败时
    """

    path = _statePath(data_manager)
    path.parent.mkdir(parents = True, exist_ok = True)
    with open(path, "w", encoding = "utf-8") as file:
        json.dump(state, file, ensure_ascii = False, indent = 4, sort_keys = True)

def _writeError(message: str, data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    把错误信息追加写入 `copy/error.log`。

    :param message: 错误信息
    :type message: str
    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    path = _copyRoot(data_manager) / "error.log"
    try:
        path.parent.mkdir(parents = True, exist_ok = True)
        with open(path, "a", encoding = "utf-8") as file:
            file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except OSError:
        traceback.print_exc()

def _incrementAttempts(data_manager: core.data.DataManager = core.data.data_manager) -> int:
    """
    递增更新状态中的失败重试次数。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 递增后的次数，状态不可读时返回 `0`
    :rtype: int
    """

    state = _readState(data_manager)
    if state is None:
        return 0
    try:
        state["attempts"] = int(state["attempts"]) + 1
    except (TypeError, ValueError):
        state["attempts"] = 1
    _writeState(state, data_manager)
    return state["attempts"]

def _fetchLatestVersion(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    后台线程：通过缓存拉取最新版本，写入模块级变量并置位事件。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    global latest_version, latest_failed
    try:
        value = data_manager.cache.get("hdpip")
        if value is None:
            raise ValueError("最新版本为空。")
        latest_version = core.util.Version(str(value))
        latest_failed = False
    except Exception:
        latest_version = None
        latest_failed = True
        try:
            data_manager.cache.clear("hdpip")
        except Exception:
            pass
    finally:
        _latest_event.set()

def _ensureLatestVersion(timeout: float = 10.0, data_manager: core.data.DataManager = core.data.data_manager) -> core.util.Version | None:
    """
    启动后台拉取并等待完成，最多等 `timeout` 秒。

    `timeout` 为 `0` 时只启动线程、不等待，返回当前已知版本（可能为 `None`）。
    GUI 线程不要传大于 `0` 的 `timeout`，否则会阻塞事件循环。

    :param timeout: 最长等待秒数
    :type timeout: float
    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 最新版本，超时或失败返回 `None`
    :rtype: core.util.Version | None
    """

    global _latest_thread
    data_manager.init()
    if latest_version is not None:
        return latest_version
    if _latest_thread is None:
        with _latest_lock:
            if _latest_thread is None:
                _latest_thread = threading.Thread(target = _fetchLatestVersion, args = (data_manager,), daemon = True)
                _latest_thread.start()
    _latest_event.wait(timeout)
    return latest_version

def checkUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    检查是否有更新。

    后台拉取尚未完成时最多等 10 秒，超时视为无更新。
    会阻塞调用线程，不要在 GUI 线程调用。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否有更新
    :rtype: bool
    """

    data_manager.init()
    latest = _ensureLatestVersion(10.0, data_manager)
    if latest is None:
        return False
    return current_version < latest

def _intervalSeconds(interval: str | int | float) -> float:
    """
    把设置中的检查间隔转换为秒数。

    :param interval: 间隔，支持数字或 `hourly`、`daily`、`weekly`、`monthly`
    :type interval: str | int | float
    :return: 秒数
    :rtype: float
    """

    if isinstance(interval, (int, float)):
        return float(interval)
    return {
        "hourly": 3600, 
        "daily": 86400, 
        "weekly": 7 * 86400, 
        "monthly": 30 * 86400
    }.get(str(interval).lower(), 86400)

def copyToTarget(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    把当前包复制到用户目录下的更新副本。

    忽略 `__pycache__` 和 `.pyc`。副本已存在且起止版本都与目标一致时跳过复制。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :raises core.util.HDpipError: 目标版本未知时
    :raises OSError: 删除旧副本或复制文件失败时
    """

    if latest_version is None:
        raise core.util.HDpipError("未知的目标版本，无法复制更新副本。")
    root = _copyRoot(data_manager)
    target = root / "HDpip"
    from_version = str(current_version)
    to_version = str(latest_version)
    state = _readState(data_manager)
    if state is not None and target.is_dir():
        if str(state["from_version"]) == from_version and str(state["to_version"]) == to_version:
            return
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents = True, exist_ok = True)
    shutil.copytree(base_dir, target, ignore = shutil.ignore_patterns("__pycache__", "*.pyc"))
    _writeState({"from_version": from_version, "to_version": to_version, "attempts": 0}, data_manager)

def _removeCopy(path: pathlib.Path) -> bool:
    """
    删除目录，失败时最多重试 10 次，每次间隔 500 毫秒。

    :param path: 要删除的目录
    :type path: pathlib.Path
    :return: 是否删除成功
    :rtype: bool
    """

    for _ in range(10):
        if not path.exists():
            return True
        try:
            shutil.rmtree(path)
        except OSError:
            time.sleep(0.5)
        else:
            return True
    return not path.exists()

def cleanupCopy(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    清理已经完成更新、已过期或状态损坏的更新副本。

    当前版本达到目标版本，或当前版本已不等于复制时的版本时删除副本。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    root = _copyRoot(data_manager)
    state = _readState(data_manager)
    if state is None:
        _removeCopy(root)
        return
    try:
        current = core.util.Version(str(current_version))
        from_version = core.util.Version(str(state["from_version"]))
        to_version = core.util.Version(str(state["to_version"]))
    except Exception:
        _removeCopy(root)
        return
    if current >= to_version or current != from_version:
        _removeCopy(root)

def launchUpdater(silent: bool, data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    启动更新进程并立即退出主进程，释放 `site-packages/HDpip` 的文件锁。

    启动失败时返回 `False`，不退出进程，由调用方处理。

    :param silent: 是否静默更新
    :type silent: bool
    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否成功启动并退出（成功时不会返回）
    :rtype: bool
    """

    root = _copyRoot(data_manager)
    script = root / "HDpip" / "gui" / "upgrade.py"
    if not script.is_file():
        _writeError(f"更新副本不存在：{script}", data_manager)
        return False
    try:
        subprocess.Popen(
            [sys.executable, str(script), "--updater"] + (["--silent"] if silent else []), 
            cwd = tempfile.gettempdir(), 
            creationflags = _creationFlags(), 
            close_fds = True, 
        )
    except OSError:
        _writeError(traceback.format_exc(), data_manager)
        return False
    os._exit(0)

def pipCommand(to_version: str) -> list[str]:
    """
    构造锁定版本的 pip 升级命令。

    :param to_version: 目标版本
    :type to_version: str
    :return: 命令参数
    :rtype: list[str]
    """

    return [sys.executable, "-m", "pip", "install", "--upgrade", f"hdpip=={to_version}"]

def _notifyThenInstall(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    显示通知框，短暂延时后自动启动更新进程。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    latest_text = str(latest_version) if latest_version is not None else "……"
    window = dialog.DialogTk(
        size = ss((600, 320)), 
        title = data_manager.language["upgrade", "title"], 
        text = data_manager.language["upgrade", "notify_tip"].format(
            current_version = current_version, 
            latest_version = latest_text
        ), 
        button = [{"text": data_manager.language["upgrade", "know_button"], "theme": "primary"}], 
        theme = "primary"
    )
    window.after(2500, window.destroy)
    window.mainloop()
    launchUpdater(False, data_manager)

def checkAndUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    检查更新并按设置决定是否复制和安装。

    检查失败时不更新 `last_check`。`silent` 和 `notify&install` 连续失败 3 次后
    会把设置中的模式降级为 `notify`。返回时表示应正常启动 GUI。
    会阻塞调用线程，不要在 GUI 线程直接调用。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    data_manager.init()
    setting = data_manager.setting
    upgrade = setting["upgrade"]
    if not upgrade.get("enable", True):
        return
    mode = str(upgrade.get("mode", "notify"))
    if mode not in ("notify", "notify&install", "silent"):
        mode = "notify"
    state = _readState(data_manager)
    attempts = int(state["attempts"]) if state is not None else 0
    auto_mode = mode in ("notify&install", "silent")
    degrade = auto_mode and attempts >= 3
    force = degrade
    if degrade:
        mode = "notify"
    pending = False
    if state is not None and auto_mode and attempts > 0:
        try:
            pending = core.util.Version(str(current_version)) == core.util.Version(str(state["from_version"])) and core.util.Version(str(current_version)) < core.util.Version(str(state["to_version"]))
        except Exception:
            pending = False
    now = time.time()
    try:
        last_check = float(upgrade.get("last_check", 0))
    except (TypeError, ValueError):
        last_check = 0
    if not force and not pending and now - last_check < _intervalSeconds(upgrade.get("interval", "daily")):
        return
    latest = _ensureLatestVersion(10.0, data_manager)
    if latest is None:
        return
    upgrade["last_check"] = now
    setting.save()
    if latest <= current_version:
        return
    if degrade:
        upgrade["mode"] = "notify"
        setting.save()
    try:
        copyToTarget(data_manager)
    except Exception:
        _writeError(traceback.format_exc(), data_manager)
        return
    if mode == "silent":
        launchUpdater(True, data_manager)
    elif mode == "notify&install":
        _notifyThenInstall(data_manager)
    else:
        Upgrade(data_manager = data_manager).mainloop()

class ConfirmCanvas(custom.containers.Canvas):
    """
    确认画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        if latest_version is None:
            if latest_failed and _latest_event.is_set():
                tip = self.data_manager.language["upgrade", "check_failed"].format(current_version = current_version)
            else:
                tip = self.data_manager.language["upgrade", "checking_tip"].format(current_version = current_version)
        elif latest_version <= current_version:
            tip = self.data_manager.language["upgrade", "latest_tip"].format(current_version = current_version)
        else:
            tip = self.data_manager.language["upgrade", "tip"].format(
                current_version = current_version, 
                latest_version = str(latest_version)
            )
        state = _readState(self.data_manager)
        attempts = int(state["attempts"]) if state is not None else 0
        if attempts >= 3:
            tip += "\n" + self.data_manager.language["upgrade", "degrade_tip"].format(attempts = attempts)
        available = latest_version is not None and latest_version > current_version
        self.tip.set(tip)
        self.note_button.set(self.data_manager.language["upgrade", "cancel_button"])
        self.confirm_button.set(self.data_manager.language["upgrade", "confirm_button"])
        self.delay_next_button.set(self.data_manager.language["upgrade", "delay_next_button"])
        self.delay_week_button.set(self.data_manager.language["upgrade", "delay_week_button"])
        self.confirm_button.disable(not available)
        self.delay_next_button.disable(not available)
        self.delay_week_button.disable(not available)

    def _close(self) -> None:
        """
        关闭更新窗口。
        """

        self.winfo_toplevel().destroy()

    def _delay(self, seconds: float) -> None:
        """
        更新 `last_check` 并关闭窗口。

        :param seconds: 从现在起延后的秒数
        :type seconds: float
        """

        self.data_manager.setting["upgrade"]["last_check"] = time.time() + seconds
        self.data_manager.setting.save()
        self._close()

    def _delayNext(self) -> None:
        """
        下次再检查。
        """

        self._delay(0)

    def _delayWeek(self) -> None:
        """
        一周内不再检查。
        """

        self._delay(7 * 86400)

    def _cancel(self) -> None:
        """
        取消更新，不修改 `last_check`。
        """

        self._close()

    def _showError(self) -> None:
        """
        弹窗提示更新启动失败。
        """

        try:
            dialog.DialogTk(
                size = ss((600, 320)), 
                title = self.data_manager.language["upgrade", "title"], 
                text = self.data_manager.language["upgrade", "state_error"], 
                button = [{"text": self.data_manager.language["upgrade", "know_button"], "theme": "primary"}], 
                theme = "danger"
            ).mainloop()
        except Exception:
            _writeError(traceback.format_exc(), self.data_manager)

    def _install(self) -> None:
        """
        确保更新副本存在后启动更新进程。失败时弹窗提示，不退出进程。

        目标版本未就绪（`latest_version` 为 `None` 或已是最新）时直接提示失败，
        不在 GUI 线程等待后台拉取。
        """

        if latest_version is None or latest_version <= current_version:
            self._showError()
            return

        try:
            copyToTarget(self.data_manager)
        except Exception:
            _writeError(traceback.format_exc(), self.data_manager)
            self._showError()
            return

        if launchUpdater(False, self.data_manager):
            return

        self._showError()

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        初始化确认画布。

        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.tip = maliang.Text(self, ss((300, 75)), None, anchor = "center", justify = "center", fontsize = ss(30))
        self.note_button = custom.widgets.Button(self, ss((300, 200)), ss((300, 50)), anchor = "center", theme = "outline-primary", command = self._cancel)
        self.confirm_button = custom.widgets.Button(self, ss((150, 275)), ss((200, 50)), anchor = "center", theme = "primary", command = self._install)
        self.delay_next_button = custom.widgets.Button(self, ss((450, 275)), ss((200, 50)), anchor = "center", theme = "outline-warning", command = self._delayNext)
        self.delay_week_button = custom.widgets.Button(self, ss((300, 350)), ss((300, 50)), anchor = "center", theme = "outline-danger", command = self._delayWeek)

        self.renderLanguage()

class InstallCanvas(custom.containers.Canvas):
    """
    安装画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.tip.set(self.data_manager.language["upgrade", "install_tip"].format(
            current_version = current_version, 
            latest_version = self._targetVersionText()
        ))

    def _targetVersionText(self) -> str:
        """
        返回正在安装的目标版本文本。

        :return: 目标版本
        :rtype: str
        """

        if latest_version is not None:
            return str(latest_version)
        state = _readState(self.data_manager)
        if state is not None:
            return str(state["to_version"])
        return self.data_manager.language["upgrade", "checking"]

    def _installWorker(self) -> None:
        """
        后台线程：执行锁定版本的 pip 安装，把每一行日志推入队列。
        """

        state = _readState(self.data_manager)
        if state is None:
            message = self.data_manager.language["upgrade", "state_error"]
            self._install_success = False
            self.log_queue.put(message)
            _writeError(message, self.data_manager)
            self.log_queue.put(None)
            return
        command = pipCommand(str(state["to_version"]))
        output = []
        try:
            process = subprocess.Popen(
                command, 
                cwd = tempfile.gettempdir(), 
                stdin = subprocess.DEVNULL, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.STDOUT, 
                creationflags = _creationFlags(), 
            )
            for line in process.stdout:
                text = core.system.shellDecode(line).rstrip()
                output.append(text)
                self.log_queue.put(text)
            returncode = process.wait()
        except Exception:
            text = traceback.format_exc()
            output.append(text)
            self.log_queue.put(text)
            returncode = -1
        if returncode == 0:
            self._install_success = True
        else:
            self._install_success = False
            _writeError("\n".join(output), self.data_manager)
            _incrementAttempts(self.data_manager)
        self.log_queue.put(None)

    def _startNewBody(self) -> None:
        """
        启动安装完成后的新主体并关闭更新窗口。
        """

        try:
            subprocess.Popen(
                [sys.executable, str(_siteMain())], 
                cwd = tempfile.gettempdir(), 
                creationflags = _creationFlags(), 
                close_fds = True
            )
        except OSError:
            _writeError(traceback.format_exc(), self.data_manager)
            return
        self.winfo_toplevel().destroy()

    def _pollLog(self) -> None:
        """
        GUI 线程：从队列取出日志并插入 ScrolledText。
        """

        try:
            while True:
                line = self.log_queue.get_nowait()
                if line is None:
                    self.log.configure(state = "normal")
                    if self._install_success:
                        self.log.insert("end", "\n[{}]\n".format(self.data_manager.language["upgrade", "install_success"]))
                        self.log.see("end")
                        self.log.configure(state = "disabled")
                        self.after(500, self._startNewBody)
                    else:
                        self.log.insert("end", "\n[{}]\n".format(self.data_manager.language["upgrade", "install_failed"]))
                        self.log.see("end")
                        self.log.configure(state = "disabled")
                    return
                self.log.configure(state = "normal")
                self.log.insert("end", line + "\n")
                self.log.see("end")
                self.log.configure(state = "disabled")
        except queue.Empty:
            pass

        self.after(50, self._pollLog)

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        初始化安装画布。

        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.tip = maliang.Text(self, ss((100, 50)), None, anchor = "w", justify = "center", fontsize = ss(25))
        self.log = custom.texts.ScrolledText(self)
        self.log.place(width = ss(500), height = ss(250), x = ss(300), y = ss(250), anchor = "center")

        self._install_success = False
        self.log_queue: queue.Queue[str | None] = queue.Queue()
        threading.Thread(target = self._installWorker, daemon = True).start()
        self.after(50, self._pollLog)

        self.renderLanguage()

class Upgrade(custom.containers.Tk):
    """
    更新窗口。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.quickTitle(self.data_manager.language["upgrade", "title"])

    def _watchLatest(self) -> None:
        """
        轮询后台拉取状态，就绪后刷新画布并在需要时复制更新副本。

        `copyToTarget` 是幂等的（起止版本一致时直接返回），
        复制的是本地源码，窗口此时已显示，不会造成启动前卡顿。
        """

        if _latest_event.is_set():
            self.confirm_canvas.renderLanguage()
            if latest_version is not None and latest_version > current_version:
                try:
                    copyToTarget(self.data_manager)
                except Exception:
                    _writeError(traceback.format_exc(), self.data_manager)
            return
        self.after(100, self._watchLatest)

    @override
    def __init__(self, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(ss((600, 400)), data_manager = data_manager, icon = str(base_dir / "assets" / "image" / "icon.png"))
        self.icon_ = maliang.PhotoImage(file = str(base_dir / "assets" / "image" / "icon.png"))
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True

        self.confirm_canvas = ConfirmCanvas(self, data_manager = data_manager)
        self.confirm_canvas.place(width = ss(600), height = ss(400), x = 0, y = 0)

        self.renderLanguage()
        self.after(100, self._watchLatest)

class InstallWindow(custom.containers.Tk):
    """
    安装窗口，由更新进程显示。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.quickTitle(self.data_manager.language["upgrade", "title"])

    @override
    def __init__(self, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(ss((600, 400)), data_manager = data_manager, icon = str(base_dir / "assets" / "image" / "icon.png"))
        self.icon_ = maliang.PhotoImage(file = str(base_dir / "assets" / "image" / "icon.png"))
        maliang.core.configs.Env.system = "Windows11"
        maliang.core.configs.Env.auto_update = True

        self.install_canvas = InstallCanvas(self, data_manager = data_manager)
        self.install_canvas.place(width = ss(600), height = ss(400), x = 0, y = 0)

        self.renderLanguage()

def runUpdater(silent: bool = False, data_manager: core.data.DataManager = core.data.data_manager) -> None:
    """
    运行更新进程入口。

    `silent` 为 `True` 时不加载 GUI，直接执行 pip 安装；安装成功后启动新主体。
    `silent` 为 `False` 时显示安装窗口，由 `InstallCanvas` 完成安装和重启。
    任何未捕获异常都会写入 `copy/error.log`，`silent=False` 时弹窗提示。

    :param silent: 是否静默更新
    :type silent: bool
    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    """

    try:
        data_manager.init()
        state = _readState(data_manager)
        if state is None:
            message = data_manager.language["upgrade", "state_error"]
            _writeError(message, data_manager)
            if not silent:
                try:
                    dialog.DialogTk(
                        size = ss((600, 320)), 
                        title = data_manager.language["upgrade", "title"], 
                        text = message, 
                        button = [{"text": data_manager.language["upgrade", "know_button"], "theme": "primary"}], 
                        theme = "danger", 
                    ).mainloop()
                except Exception:
                    _writeError(traceback.format_exc(), data_manager)
            return
        to_version = str(state["to_version"])
        if not silent:
            try:
                InstallWindow(data_manager = data_manager).mainloop()
            except Exception:
                _writeError(traceback.format_exc(), data_manager)
            return
        try:
            result = subprocess.run(
                pipCommand(to_version), 
                cwd = tempfile.gettempdir(), 
                stdin = subprocess.DEVNULL, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.STDOUT, 
                creationflags = _creationFlags(), 
            )
        except Exception:
            _writeError(traceback.format_exc(), data_manager)
            _incrementAttempts(data_manager)
            return
        if result.returncode != 0:
            _writeError(core.system.shellDecode(result.stdout or b""), data_manager)
            _incrementAttempts(data_manager)
            return
        try:
            subprocess.Popen(
                [sys.executable, str(_siteMain())], 
                cwd = tempfile.gettempdir(), 
                creationflags = _creationFlags(), 
                close_fds = True
            )
        except OSError:
            _writeError(traceback.format_exc(), data_manager)
    except Exception:
        _writeError(traceback.format_exc(), data_manager)
        if not silent:
            try:
                dialog.DialogTk(
                    size = ss((600, 320)), 
                    title = data_manager.language["upgrade", "title"], 
                    text = data_manager.language["upgrade", "state_error"], 
                    button = [{"text": data_manager.language["upgrade", "know_button"], "theme": "primary"}], 
                    theme = "danger", 
                ).mainloop()
            except Exception:
                _writeError(traceback.format_exc(), data_manager)

if __name__ == "__main__":
    if "--updater" in sys.argv:
        runUpdater("--silent" in sys.argv)
    else:
        core.data.data_manager.init()
        _ensureLatestVersion(0, core.data.data_manager)
        Upgrade().mainloop()
