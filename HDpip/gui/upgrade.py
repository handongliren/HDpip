"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是更新器。
"""

from typing import *
from typing_extensions import override
import pathlib
import queue
import threading

import maliang.core.configs
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

try:
    from .. import core
except ImportError:
    import sys
    sys.path.append(str(base_dir))
    import core

try:
    from . import custom
    from .custom.util import ss
    from .custom.media import bi
except ImportError:
    import custom
    from custom.util import ss
    from custom.media import bi

current_version = core.system.getVersion()

latest_version: core.util.Version | None = None
_latest_event = threading.Event()

def _fetch_latest_version() -> None:
    """
    后台线程：拉取最新版本，写入模块级变量并置位事件。
    """

    global latest_version
    try:
        latest_version = core.pip_api.getLatestVersion("hdpip")
    except Exception:
        latest_version = None
    finally:
        _latest_event.set()

def _ensure_latest_version(timeout: float = 10.0) -> core.util.Version | None:
    """
    等待后台拉取完成，最多等 `timeout` 秒。

    :param timeout: 最长等待秒数
    :type timeout: float
    :return: 最新版本，超时或失败返回 `None`
    :rtype: core.util.Version | None
    """

    if latest_version is not None:
        return latest_version
    _latest_event.wait(timeout)
    return latest_version

def checkUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    检查是否有更新。

    后台拉取尚未完成时最多等 10 秒，超时视为无更新。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否有更新
    :rtype: bool
    """

    data_manager.init()
    latest = _ensure_latest_version()
    if latest is None:
        return False
    return current_version < latest

class ConfirmCanvas(custom.containers.Canvas):
    """
    确认画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        latest_text = str(latest_version) if latest_version is not None else "……"
        self.tip.set(self.data_manager.language["upgrade", "tip"].format(
            current_version = current_version, 
            latest_version = latest_text, 
        ))
        self.note_button.set(self.data_manager.language["upgrade", "note_button"])
        self.confirm_button.set(self.data_manager.language["upgrade", "confirm_button"])
        self.delay_next_button.set(self.data_manager.language["upgrade", "delay_next_button"])
        self.delay_week_button.set(self.data_manager.language["upgrade", "delay_week_button"])

    @override
    def __init__(self, master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.data.DataManager = core.data.data_manager) -> None:
        """
        初始化确认画布。

        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True, data_manager = data_manager)

        self.tip = maliang.Text(self, ss((300, 75)), None, anchor = "center", justify = "center", fontsize = ss(30))
        self.note_button = custom.widgets.Button(self, ss((300, 200)), ss((300, 50)), anchor = "center", theme = "outline-primary")
        self.confirm_button = custom.widgets.Button(self, ss((150, 275)), ss((200, 50)), anchor = "center", theme = "primary")
        self.delay_next_button = custom.widgets.Button(self, ss((450, 275)), ss((200, 50)), anchor = "center", theme = "outline-warning")
        self.delay_week_button = custom.widgets.Button(self, ss((300, 350)), ss((300, 50)), anchor = "center", theme = "outline-danger")

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

        latest_text = str(latest_version) if latest_version is not None else "……"
        self.tip.set(self.data_manager.language["upgrade", "install_tip"].format(
            current_version = current_version, 
            latest_version = latest_text, 
        ))

    def _installWorker(self) -> None:
        """
        后台线程：执行 pip 安装，把每一行日志推入队列。
        """

        try:
            core.pip_api.install(
                "--upgrade hdpip", 
                callback = self.log_queue.put, 
            )
        except Exception as e:
            self.log_queue.put("[{}]\n".format(self.data_manager.language["upgrade", "error"]) + str(e))
        finally:
            self.log_queue.put(None)

    def _pollLog(self) -> None:
        """
        GUI 线程：从队列取出日志并插入 ScrolledText。
        """

        try:
            while True:
                line = self.log_queue.get_nowait()
                if line is None:
                    self.log.configure(state = "normal")
                    self.log.insert("end", "\n[{}]\n".format(self.data_manager.language["upgrade", "install_success"]))
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
        轮询后台拉取状态，就绪后刷新所有画布的语言。
        """

        if _latest_event.is_set():
            self.confirm_canvas.renderLanguage()
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

if __name__ == "__main__":
    threading.Thread(target = _fetch_latest_version, daemon = True).start()
    Upgrade().mainloop()
