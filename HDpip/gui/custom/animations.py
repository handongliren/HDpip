"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

自定义动画。
"""

from typing import *
from typing_extensions import override

import maliang
import maliang.animation

class WindowFadeIn(maliang.animation.Animation):
    """
    针对`maliang`的窗口写的渐入动画。
    """

    @override
    def __init__(
        self,
        window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel],
        duration: int,
        *,
        controller: Callable[[float], float] = maliang.animation.controllers.linear,
        end: Callable[[], Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:

        """
        :param self: `WindowFadeIn`类
        :param window: 要渐入的窗口
        :type window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel]
        :param duration: 持续时长
        :type duration: int
        :param controller: 控制函数
        :type controller: Callable[[float], float]
        :param end: 结束函数
        :type end: Callable[[], Any] | None
        :param fps: 每秒帧数
        :type fps: int
        :param repeat: 重复次数
        :type repeat: int
        :param repeat_delay: 重复前的延时
        :type repeat_delay: int
        """

        if isinstance(window, Sequence):
            def command(p: float) -> None:
                for w in window:
                    w.alpha(p)
        else:
            command = window.alpha

        super().__init__(duration, command, controller = controller, end = end, fps = fps, repeat = repeat, repeat_delay = repeat_delay)

class WindowFadeOut(maliang.animation.Animation):
    """
    针对`maliang`的窗口写的渐出动画。
    """

    @override
    def __init__(
        self,
        window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel],
        duration: int,
        *,
        controller: Callable[[float], float] = maliang.animation.controllers.linear,
        end: Callable[[], Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:

        """
        :param self: `WindowFadeOut`类
        :param window: 要渐出的窗口
        :type window: maliang.Tk | maliang.Toplevel | Sequence[maliang.Tk | maliang.Toplevel]
        :param duration: 持续时长
        :type duration: int
        :param controller: 控制函数
        :type controller: Callable[[float], float]
        :param end: 结束函数
        :type end: Callable[[], Any] | None
        :param fps: 每秒帧数
        :type fps: int
        :param repeat: 重复次数
        :type repeat: int
        :param repeat_delay: 重复前的延时
        :type repeat_delay: int
        """

        if isinstance(window, Sequence):
            def command(p: float) -> None:
                for w in window:
                    w.alpha(1 - p)
        else:
            def command(p: float) -> None:
                window.alpha(1 - p)

        super().__init__(duration, command, controller = controller, end = end, fps = fps, repeat = repeat, repeat_delay = repeat_delay)
