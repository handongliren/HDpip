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

current_version = core.system.getVersion(), 
latest_version = core.pip_api.getLatestVersion("hdpip")

def checkUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    检查是否有更新。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否有更新
    :rtype: bool
    """

    data_manager.init()

    return current_version < latest_version

class ConfirmCanvas(custom.containers.Canvas):
    """
    确认画布。
    """

    @override
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        self.tip.set(self.data_manager.language["upgrade", "tip"].format(
            current_version = current_version, 
            latest_version = latest_version
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

        self.tip.set(self.data_manager.language["upgrade", "install_tip"].format(
            current_version = current_version, 
            latest_version = latest_version
        ))
        #self.progress.set(self.data_manager.language["upgrade", "install_progress"])

    def _installWorker(self) -> None:
        """
        后台线程：执行 pip 安装，把每一行日志推入队列。
        """

        try:
            core.pip_api.install(
                "--upgrade hdpip",
                callback = lambda line: self.log_queue.put(line),
            )
        except Exception as e:
            self.log_queue.put(f"[错误] {e}")
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
                    self.log.insert("end", "\n[安装结束]\n")
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
        #self.progress_bar = maliang.ProgressBar(self, ss((300, 200)), ss((400, 50)), anchor = "center")
        #self.progress = maliang.Text(self, ss((300, 275)), None, anchor = "center", justify = "center", fontsize = ss(20))
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

        self.confirm_canvas = InstallCanvas(self, data_manager = data_manager)
        self.confirm_canvas.place(width = ss(600), height = ss(400), x = 0, y = 0)

        self.renderLanguage()

if __name__ == "__main__":
    Upgrade().mainloop()
