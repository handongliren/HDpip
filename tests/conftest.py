import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parents[1].resolve()))


@pytest.fixture(scope = "session")
def tk_root():
    """创建 Tk 窗口和 Canvas，所有测试结束后自动销毁。"""
    import maliang

    root = maliang.Tk((800, 400))
    canvas = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
    canvas.place(width = 800, height = 400)
    yield root, canvas
    root.destroy()
