"""
Error Catcher 演示与测试
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))

import pytest
from HDpip.gui.error_catcher import catch


@catch(auto_close = 500)
def raise_value_error():
    raise ValueError("这是一个测试错误！")


@catch(auto_close = 500)
def divide_by_zero():
    return 1 / 0


@catch(auto_close = 500)
def key_error():
    d = {}
    return d["missing"]


@catch(auto_close = 500)
def normal_return():
    return 42


class TestErrorCatcher:
    """@catch 装饰器单元测试。"""

    def test_catches_value_error(self, ):
        assert raise_value_error() is None

    def test_catches_zero_division(self, ):
        assert divide_by_zero() is None

    def test_catches_key_error(self, ):
        assert key_error() is None

    def test_passes_through_normal(self, ):
        assert normal_return() == 42


if __name__ == "__main__":
    import maliang
    import maliang.core.configs
    import HDpip

    maliang.core.configs.Env.system = "Windows11"

    root = maliang.Tk((400, 300), title = "Error Catcher Demo")
    root.center()

    canvas = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
    canvas.place(width = 400, height = 300)

    btn1 = HDpip.gui.base.Button(canvas, (50, 50), (300, 50), text = "触发 ValueError",
                                  theme = "danger", command = raise_value_error)
    btn2 = HDpip.gui.base.Button(canvas, (50, 120), (300, 50), text = "触发 ZeroDivisionError",
                                  theme = "warning", command = divide_by_zero)
    btn3 = HDpip.gui.base.Button(canvas, (50, 190), (300, 50), text = "触发 KeyError",
                                  theme = "info", command = key_error)

    root.mainloop()
