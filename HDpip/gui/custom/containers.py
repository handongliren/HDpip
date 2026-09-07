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

try:
    from ... import core
except ImportError:
    sys.path.append(str(base_dir))
    import core

try:
    from . import animations, media
    from .util import ss
except ImportError:
    import animations, media
    from util import ss

class Tk(maliang.core.containers.Tk, abc.ABC):
    """
    自定义`Tk`容器。
    """

    @override
    def __init__(
        self, 
        size: tuple[int, int] = ss((1200, 800)), 
        position: tuple[int, int] | None = None, 
        *, 
        data_manager: core.data.DataManager = core.data.data_manager, 
        title: str | None = None, 
        icon: str | pathlib.Path | media.Image | maliang.toolbox.enhanced.PhotoImage | None = base_dir / "assets" / "image" / "icon.png",
        **kwargs: Any
    ):
        """
        :param size: 窗口大小
        :type size: tuple[int, int]
        :param position: 窗口位置
        :type position: tuple[int, int] | None
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        :param title: 窗口标题
        :type title: str | None
        :param icon: 窗口图标
        :type icon: str | pathlib.Path | media.Image | maliang.toolbox.enhanced.PhotoImage | None
        :param kwargs: 其他参数
        :type kwargs: Any
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__(size, position, title = title, icon = None, **kwargs)
        if isinstance(icon, (str, pathlib.Path)):
            icon = media.Image(file = icon)
        if icon is not None:
            self.icon(icon)
        animations.WindowFadeIn(self, 250, controller = maliang.animation.smooth, fps = 60).start()
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
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        animations.WindowFadeOut(self, 250, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()

    def quickTitle(self, window_name: str) -> None:
        """
        快速设置标题。

        :param window_name: 窗口名称
        :type window_name: str
        """

        self.wm_title(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ") - " + window_name)

class Toplevel(maliang.core.containers.Toplevel, abc.ABC):
    """
    自定义`Toplevel`容器。
    """

    @override
    def __init__(
        self, 
        master: Tk | Self | maliang.core.containers.Tk | maliang.core.containers.Toplevel, 
        size: tuple[int, int] = ss((1200, 800)), 
        position: tuple[int, int] | None = None, 
        *, 
        data_manager: core.data.DataManager = core.data.data_manager, 
        title: str | None = None, 
        icon: str | pathlib.Path | media.Image | maliang.toolbox.enhanced.PhotoImage | None = base_dir / "assets" / "image" / "icon.png",
        **kwargs: Any
    ):
        """
        :param master: 父窗口
        :type master: Tk | Self | maliang.core.containers.Tk | maliang.core.containers.Toplevel
        :param size: 窗口大小
        :type size: tuple[int, int]
        :param position: 窗口位置
        :type position: tuple[int, int] | None
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        :param title: 窗口标题
        :type title: str | None
        :param icon: 窗口图标
        :type icon: str | pathlib.Path | media.Image | maliang.toolbox.enhanced.PhotoImage | None
        :param kwargs: 其他参数
        :type kwargs: Any
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__(master, size, position, title = title, icon = None, **kwargs)
        if isinstance(icon, (str, pathlib.Path)):
            icon = media.Image(file = icon)
        if icon is not None:
            self.icon(icon)
        animations.WindowFadeIn(self, 250, controller = maliang.animation.smooth, fps = 60).start()
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
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        animations.WindowFadeOut(self, 250, controller = maliang.animation.smooth, fps = 60, end = super().destroy).start()

    def quickTitle(self, window_name: str) -> None:
        """
        快速设置标题。

        :param window_name: 窗口名称
        :type window_name: str
        """

        self.wm_title(self.data_manager.language["program_name"] + "(" + self.data_manager.language["program_subname"] + ") - " + window_name)

class Canvas(maliang.core.containers.Canvas, abc.ABC):
    """
    自定义`Canvas`容器。
    """

    @override
    def __init__(
        self, 
        master: Tk | Toplevel | Self | maliang.core.containers.Tk | maliang.core.containers.Toplevel | maliang.core.containers.Canvas | None = None, 
        *, 
        data_manager: core.data.DataManager = core.data.data_manager, 
        expand: Literal['', 'x', 'y', 'xy'] = "xy", 
        auto_zoom: bool = False, 
        keep_ratio: Literal['min', 'max'] | None = None, 
        free_anchor: bool = False, 
        auto_update: bool | None = None, 
        zoom_all_items: bool = False,
        **kwargs: Any
    ):
        """
        :param master: 父控件
        :type master: Tk | Toplevel | Self | maliang.core.containers.Tk | maliang.core.containers.Toplevel | maliang.core.containers.Canvas | None
        :param data_manager: 数据管理器
        :type data_manager: core.data.DataManager
        :param expand: 扩展模式
        :type expand: Literal['', 'x', 'y', 'xy']
        :param auto_zoom: 是否自动缩放
        :type auto_zoom: bool
        :param keep_ratio: 宽高比模式
        :type keep_ratio: Literal['min', 'max'] | None
        :param free_anchor: 锚点是否自由浮动
        :type free_anchor: bool
        :param auto_update: 是否自动更新
        :type auto_update: bool | None
        :param zoom_all_items: 是否缩放所有项
        :type zoom_all_items: bool
        :param kwargs: 其他参数
        :type kwargs: Any
        """

        self.data_manager = data_manager
        self.data_manager.init()

        super().__init__(master, expand = expand, auto_zoom = auto_zoom, keep_ratio = keep_ratio, free_anchor = free_anchor, auto_update = auto_update, zoom_all_items = zoom_all_items, **kwargs)
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
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()
