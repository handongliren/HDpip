"""
Dialog 控件演示
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))
import HDpip

import maliang
import maliang.core.configs
import maliang.theme

maliang.core.configs.Env.system = "Windows11"
maliang.theme.set_color_mode("dark")

root = maliang.Tk((800, 600), title = "Dialog Demo")
root.center()

canvas = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
canvas.place(width = 800, height = 600)

dialog = HDpip.gui.dialog.DialogCanvas(canvas, (400, 300), (600, 400), title = "提示", text = "hello", anchor = "center")

root.mainloop()
