"""
Error Catcher 演示
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))
import HDpip

import maliang
import maliang.core.configs

from HDpip.gui.error_catcher import catch

maliang.core.configs.Env.system = "Windows11"

@catch
def raise_value_error():
    raise ValueError("这是一个测试错误！")


@catch
def divide_by_zero():
    return 1 / 0


@catch
def key_error():
    d = {}
    return d["missing"]


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
