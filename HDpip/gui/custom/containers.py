"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于定制容器。
"""

from typing import *
from typing_extensions import Self, override

import abc
import pathlib
import sys

import maliang.core.containers
import maliang.theme
import maliang.animation
import maliang.toolbox.enhanced

base_dir = pathlib.Path(__file__).parents[2].resolve()

sys.path.append(str(base_dir))
import core

try:
    from . import animations, media
    from .utility import ss
except ImportError:
    import animations, media
    from utility import ss

class Tk(maliang.core.containers.Tk, abc.ABC):
    """
    自定义`Tk`容器。
    """

    @override
    def __init__(
        self, 
        data_manager: core.data.DataManager = core.data.DataManager(), 
        size: tuple[int, int] = ss((1200, 800)),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        icon: str | media.Image | maliang.toolbox.enhanced.PhotoImage | None = maliang.toolbox.enhanced.PhotoImage(file = str(base_dir / "assets" / "image" / "icon.png")),
        **kwargs: Any,
    ):
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__(size, position, title = title, icon = icon, **kwargs)
        animations.WindowFadeIn(self, 500, controller = maliang.animation.smooth, fps = 60).start()
        if position is None:
            self.center()
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        self.data_manager.language.registerEvent(self.onLanguageChange)

    @abc.abstractmethod
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        ...

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `Welcome`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    @override
    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `Welcome`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        animations.WindowFadeOut(self, 500, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()

class Toplevel(maliang.core.containers.Toplevel, abc.ABC):
    """
    自定义`Toplevel`容器。
    """

    @override
    def __init__(
        self, 
        master: Tk | Self | maliang.core.containers.Tk | maliang.core.containers.Toplevel, 
        data_manager: core.data.DataManager = core.data.DataManager(), 
        size: tuple[int, int] = ss((1200, 800)),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        icon: str | media.Image | maliang.toolbox.enhanced.PhotoImage | None = maliang.toolbox.enhanced.PhotoImage(file = str(base_dir / "assets" / "image" / "icon.png")),
        **kwargs: Any,
    ):
        """
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__(master, size, position, title = title, icon = icon, **kwargs)
        animations.WindowFadeIn(self, 500, controller = maliang.animation.smooth, fps = 60).start()
        if position is None:
            self.center()
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        self.data_manager.language.registerEvent(self.onLanguageChange)

    @abc.abstractmethod
    def renderLanguage(self) -> None:
        """
        渲染语言。
        """

        ...

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `Welcome`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    @override
    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `Welcome`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        animations.WindowFadeOut(self, 500, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()
