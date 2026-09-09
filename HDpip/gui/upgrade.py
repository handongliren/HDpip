"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是更新器。
"""

from typing import *
from typing_extensions import override
import pathlib

import maliang.theme
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

def checkUpdate(data_manager: core.data.DataManager = core.data.data_manager) -> bool:
    """
    检查是否有更新。

    :param data_manager: 数据管理器
    :type data_manager: core.data.DataManager
    :return: 是否有更新
    :rtype: bool
    """

    data_manager.init()
    mirror = data_manager.setting[
        "pip", 
        "mirrors", 
        data_manager.setting["pip", "mirror_index"], 
        "url"
    ]
    current_version = core.system.getVersion()
    latest_version = core.pip_api.getLatestVersion("hdpip", mirror)

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
            current_version = core.system.getVersion(), 
            latest_version = core.pip_api.getLatestVersion("hdpip", self.data_manager.setting[
                "pip", 
                "mirrors", 
                self.data_manager.setting["pip", "mirror_index"], 
                "url"
            ])
        ))
        self.confirm_button.text.set(self.data_manager.language["upgrade", "confirm_button"])
        self.delay_next_button.text.set(self.data_manager.language["upgrade", "delay_next_button"])
        self.delay_week_button.text.set(self.data_manager.language["upgrade", "delay_week_button"])