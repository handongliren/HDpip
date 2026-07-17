"""
演示 ptToPx 的字体大小换算效果。
"""

import pathlib
import sys

base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))

import maliang
import maliang.core.configs

from HDpip.gui import base


def main() -> None:
    """显示一个带有 HDpip 字体示例的 maliang 窗口。"""

    maliang.core.configs.Env.system = "Windows11"

    root = maliang.Tk((800, 400), title = "ptToPx 字体演示")
    root.center()

    canvas = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
    canvas.place(width = 800, height = 400)

    font_size = int(round(base.pxToPt(30)))
    maliang.Text(
        canvas,
        (400, 200),
        None,
        text = "HDpip",
        fontsize = font_size,
        anchor = "center",
        auto_update = True
    )

    root.mainloop()


if __name__ == "__main__":
    main()
