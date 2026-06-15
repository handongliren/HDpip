from typing import *

import maliang

from HDpip import core

class ForkCanvas(maliang.Canvas):
    """
    画布。
    """

    def renderLanguage(self) -> None:
        """
        渲染语言。

        :param self: `ForkCanvas`类
        """

    def onLanguageChange(self, event_type: str, event_data: dict[str, Any]) -> None:
        """
        语言更改的回调函数。

        :param self: `ForkCanvas`类
        :param event_type: 事件类型
        :type event_type: str
        :param event_data: 事件数据
        :type event_data: dict[str, Any]
        """

        if event_type == "load":
            self.renderLanguage()

    def destroy(self) -> None:
        """
        销毁控件。

        :param self: `ForkCanvas`类
        """

        self.data_manager.language.unregisterEvent(self.onLanguageChange)
        super().destroy()

    def __init__(self, master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel, data_manager: core.base.DataManager = core.base.DataManager()):
        """
        :param master: 父控件
        :type master: maliang.containers.Canvas | maliang.core.virtual.Widget | maliang.Tk | maliang.Toplevel
        :param data_manager: 数据管理器
        :type data_manager: core.base.DataManager
        """

        super().__init__(master, expand = "xy", auto_zoom = True, auto_update = True)
        self.data_manager = data_manager
        self.data_manager.language.registerEvent(self.onLanguageChange)

        self.renderLanguage()
