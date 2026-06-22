"""
HDpip/gui/base.py 按钮演示与测试
支持Win11风格和明暗主题。
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))

BUTTON_TYPES = [
    "default", "primary", "secondary", "success",
    "info", "warning", "danger", "light", "dark",
    "outline-default", "outline-primary", "outline-secondary", "outline-success",
    "outline-info", "outline-warning", "outline-danger", "outline-light", "outline-dark",
]


class TestButtonCreation:
    """Button 创建测试。"""

    def test_all_themes_create(self, tk_root, ):
        import HDpip

        root, canvas = tk_root

        for theme in BUTTON_TYPES:
            btn = HDpip.gui.base.Button(canvas, (10, 10), (100, 30), theme = theme, text = theme)
            assert btn is not None


if __name__ == "__main__":
    import maliang
    import maliang.core.configs
    import maliang.theme
    import HDpip

    class ButtonDemo(maliang.Tk):
        """按钮演示窗口。"""

        def __init__(self, ):
            super().__init__((1400, 1000), title = "HDpip 按钮演示 - Button Demo")
            self.icon_ = maliang.PhotoImage(file = str(HDpip.core.base.getBaseDir() / "asset" / "image" / "icon.png"))
            self.iconphoto(True, self.icon_)
            self.wm_iconphoto(True, self.icon_)

            maliang.theme.customize_window(self, disable_maximize_button = True, )
            maliang.core.configs.Env.system = "Windows11"
            self.resizable(False, False)
            self.center()

            self.canvas = maliang.Canvas(self, expand = "xy", auto_zoom = True, auto_update = True, bg = "#f3f3f3")
            self.canvas.place(width = 1400, height = 1000, x = 0, y = 0)

            maliang.theme.register_event(self.update_canvas_theme)

            self.title_text = maliang.Text(self.canvas, (700, 50), (1400, 100),
                                           text = "HDpip 按钮类型演示", fontsize = 32, weight = "bold", anchor = "center")
            self.subtitle_text = maliang.Text(self.canvas, (700, 90), (1400, 50),
                                              text = "左边九个普通按钮，右边九个轮廓按钮", fontsize = 18, anchor = "center")

            self.all_disabled = False
            self.dark_theme = False
            self.all_buttons = []

            self.create_control_switches()
            self.create_buttons()
            self.update_canvas_theme(maliang.theme.get_color_mode())

        def create_control_switches(self, ):
            control_y = 125
            switch_width = 250
            switch_height = 60
            switch_spacing = 50
            total_width = 2 * switch_width + switch_spacing
            start_x = (1400 - total_width) // 2

            self.theme_switch = HDpip.gui.base.Button(self.canvas, (start_x, control_y),
                (switch_width, switch_height), theme = "primary",
                text = "🌓 明暗主题切换", command = self.toggle_theme)
            self.disable_switch = HDpip.gui.base.Button(self.canvas,
                (start_x + switch_width + switch_spacing, control_y),
                (switch_width, switch_height), theme = "warning",
                text = "⏸️ 全体禁用切换", command = self.toggle_all_disabled)

            status_width = 500
            status_x = start_x + (total_width - status_width) // 2
            self.status_text = maliang.Text(self.canvas, (status_x + status_width // 2, control_y + 80),
                (status_width, 40), text = "状态: 所有按钮已启用 | 主题: 系统默认",
                fontsize = 14, anchor = "center")

        def create_buttons(self, ):
            button_width = 180
            button_height = 50
            button_spacing_x = 220
            button_spacing_y = 70
            start_x = 100
            start_y = 280

            regular = BUTTON_TYPES[:9]
            outline = BUTTON_TYPES[9:]

            columns = [
                (regular, 0, 5, 0),
                (regular, 5, 4, 1),
                (outline, 0, 5, 2),
                (outline, 5, 4, 3),
            ]
            for button_list, start_index, count, col in columns:
                for row in range(count):
                    btn_type = button_list[start_index + row]
                    x = start_x + col * (button_width + button_spacing_x)
                    y = start_y + row * button_spacing_y
                    texts = {
                        "default": "默认", "primary": "主要", "secondary": "次要",
                        "success": "成功", "info": "信息", "warning": "警告",
                        "danger": "危险", "light": "浅色", "dark": "深色",
                        "outline-default": "轮廓-默认", "outline-primary": "轮廓-主要",
                        "outline-secondary": "轮廓-次要", "outline-success": "轮廓-成功",
                        "outline-info": "轮廓-信息", "outline-warning": "轮廓-警告",
                        "outline-danger": "轮廓-危险", "outline-light": "轮廓-浅色", "outline-dark": "轮廓-深色",
                    }
                    button = HDpip.gui.base.Button(self.canvas, (x, y),
                        (button_width, button_height), theme = btn_type, text = texts[btn_type],
                        anchor = "center", command = lambda bt = btn_type: self.on_button_click(bt))
                    self.all_buttons.append(button)

            regular_title_x = start_x + (button_width + button_spacing_x) // 2
            self.regular_title = maliang.Text(self.canvas, (regular_title_x, start_y - 40),
                (button_width + button_spacing_x, 30), text = "普通按钮 (9种)",
                fontsize = 16, weight = "bold", anchor = "center")
            outline_title_x = start_x + 2 * (button_width + button_spacing_x) + (button_width + button_spacing_x) // 2
            self.outline_title = maliang.Text(self.canvas, (outline_title_x, start_y - 40),
                (button_width + button_spacing_x, 30), text = "轮廓按钮 (9种)",
                fontsize = 16, weight = "bold", anchor = "center")

        def on_button_click(self, button_type, ):
            print(f"按钮被点击: {button_type}")
            self.status_text.set(
                f"点击了: {button_type} | 主题: {'暗色' if self.dark_theme else '亮色'} | "
                f"状态: {'禁用' if self.all_disabled else '启用'}")

        def toggle_theme(self, ):
            self.dark_theme = not self.dark_theme
            if self.dark_theme:
                maliang.theme.set_color_mode("dark")
                self.theme_switch.text = "🌙 切换到亮色主题"
            else:
                maliang.theme.set_color_mode("light")
                self.theme_switch.text = "☀️ 切换到暗色主题"
            self.update_canvas_theme(maliang.theme.get_color_mode())
            self.update_all_buttons_theme()
            self.update_status()

        def toggle_all_disabled(self, ):
            self.all_disabled = not self.all_disabled
            for button in self.all_buttons:
                button.disable(self.all_disabled)
            if self.all_disabled:
                self.disable_switch.text = "▶️ 启用所有按钮"
            else:
                self.disable_switch.text = "⏸️ 禁用所有按钮"
            self.update_status()

        def update_canvas_theme(self, color_mode, ):
            if color_mode == "dark":
                self.canvas.configure(bg = "#1e1e1e")
            else:
                self.canvas.configure(bg = "#f3f3f3")
            self.canvas.update()

        def update_all_buttons_theme(self, ):
            for button in self.all_buttons:
                current_disabled = getattr(button, "disabled", False)
                button.disable(current_disabled)

        def update_status(self, ):
            theme_text = "暗色" if self.dark_theme else "亮色"
            state_text = "禁用" if self.all_disabled else "启用"
            self.status_text.set(text = f"状态: 所有按钮已{state_text} | 主题: {theme_text}")

    demo = ButtonDemo()
    demo.mainloop()
