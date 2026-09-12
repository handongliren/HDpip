"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件用于定制容器。
"""

from typing import *
from typing_extensions import Self, override

import copy
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
    from . import animations, media, widgets
    from .util import ss
except ImportError:
    import animations, media, widgets
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
        maliang.configs.Env.system = "Windows11"
        maliang.configs.Env.auto_update = True
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        maliang.theme.set_color_mode(data_manager.setting["theme"])
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
        maliang.configs.Env.system = "Windows11"
        maliang.configs.Env.auto_update = True
        maliang.theme.customize_window(self, disable_maximize_button = True)
        self.resizable(False, False)
        maliang.theme.set_color_mode(data_manager.setting["theme"])
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

class PageView(maliang.Canvas):
    """
    页面视图容器，用于切换多个画布，效果类似于`Wizard`。
    """

    def bindBackButton(self, button: widgets.Button) -> None:
        """
        绑定上一步按钮。

        :param button: 上一步按钮
        :type button: widgets.Button
        """

        self.back_button = button
        self.back_button.bind("<Button-1>", lambda event: self.back() if not button.disabled else None)

    def bindNextButton(self, button: widgets.Button) -> None:
        """
        绑定下一步按钮。

        :param button: 下一步按钮
        :type button: widgets.Button
        """

        self.next_button = button
        self.next_button.bind("<Button-1>", lambda event: self.next() if not button.disabled else None)

    @override
    def __init__(
        self, 
        master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, 
        canvas_class: list[type[Canvas]] = [], 
        content_argvs: list[Any] = [], 
        content_kwargs: dict[str, Any] = {}, 
        *, 
        animation: bool = True, 
        back_button: widgets.Button | None = None, 
        next_button: widgets.Button | None = None
    ):
        """
        :param master: 父控件
        :type master: maliang.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param canvas_class: 画布类列表
        :type canvas_class: list[type[Canvas]]
        :param content_argvs: 内容参数列表
        :type content_argvs: list[Any]
        :param content_kwargs: 内容关键字参数
        :type content_kwargs: dict[str, Any]
        :param animation: 是否启用动画
        :type animation: bool
        :param back_button: 返回按钮
        :type back_button: widgets.Button | None
        :param next_button: 下一步按钮
        :type next_button: widgets.Button | None
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)

        self.canvas_index = 0
        self.canvas_list: list[Canvas] = []
        self.canvas_class = canvas_class
        self.content_argvs = content_argvs
        self.content_kwargs = content_kwargs
        self.animation = animation
        if back_button is not None:
            self.bindBackButton(back_button)
        if next_button is not None:
            self.bindNextButton(next_button)
        self.move_lock = False

        for _ in range(0, len(self.canvas_class)):
            self.canvas_list.append("uninited")

    def switchCanvas(self, index: int) -> None:
        """
        切换至指定画布。

        :param index: 索引
        :type index: int
        """

        if self.move_lock:
            return
        if index == 0:
            if hasattr(self, "back_button") and self.back_button is not None:
                self.back_button.disable()
            if hasattr(self, "next_button") and self.next_button is not None:
                self.next_button.disable(False)
        elif index == len(self.canvas_class) - 1:
            if hasattr(self, "back_button") and self.back_button is not None:
                self.back_button.disable(False)
            if hasattr(self, "next_button") and self.next_button is not None:
                self.next_button.disable()
        else:
            if hasattr(self, "back_button") and self.back_button is not None:
                self.back_button.disable(False)
            if hasattr(self, "next_button") and self.next_button is not None:
                self.next_button.disable(False)
        if self.canvas_list[index] == "uninited":
            self.canvas_list[index] = self.canvas_class[index](self, *self.content_argvs, **self.content_kwargs)
            self.canvas_list[index].place(x = index * ss(1200), y = 0, width = ss(1200), height = ss(700))
        if self.animation:
            self.move_lock = True
            maliang.animation.MoveTkWidget(self, ((self.canvas_index - index) * ss(1200), 0), 500, controller = maliang.animation.smooth, fps = 60, end = lambda: setattr(self, "move_lock", False)).start()
        else:
            self.place(x = -index * ss(1200), y = 0)
        self.canvas_index = index

    def walkCanvas(self, index: int) -> None:
        """
        相对步进画布。

        :param index: 索引
        :type index: int
        """

        self.switchCanvas(self.canvas_index + index)

    def back(self) -> None:
        """
        上一步。
        """

        self.walkCanvas(-1)

    def next(self) -> None:
        """
        下一步。
        """

        self.walkCanvas(1)
