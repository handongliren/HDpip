"""
Dialog 控件演示与测试
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))


class TestDialogCanvas:
    """DialogCanvas 创建测试。"""

    def test_create_dialog_canvas(self, tk_root, ):
        import HDpip

        root, canvas = tk_root
        dialog = HDpip.gui.dialog.DialogCanvas(canvas, (200, 150), (300, 200), title = "提示", text = "Hello world!\n你好世界！", anchor = "center")
        assert dialog is not None


if __name__ == "__main__":
    import maliang
    import maliang.core.configs
    import maliang.theme
    import HDpip

    maliang.core.configs.Env.system = "Windows11"
    maliang.theme.set_color_mode("dark")

    root = maliang.Tk((800, 600), title = "Dialog Demo")
    root.center()

    canvas = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
    canvas.place(width = 800, height = 600)

    dialog = HDpip.gui.dialog.DialogCanvas(canvas, (400, 300), (600, 400), title = "提示", text = "Hello world!\n你好世界！", anchor = "center")

    root.mainloop()
