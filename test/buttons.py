"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件展示HDpip/gui/base.py中所有类型的按钮，重新设计布局。
支持Win11风格和明暗主题。
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))
import HDpip

import maliang
import maliang.core.configs
import maliang.theme

class ButtonDemo(maliang.Tk):
    """
    按钮演示窗口，展示所有类型的按钮 - 重新设计布局
    支持Win11风格和明暗主题
    """

    def __init__(self):
        # 使用Win11风格
        super().__init__((1400, 1000), title="HDpip 按钮演示 - Button Demo")
        self.icon_ = maliang.PhotoImage(file = str(HDpip.core.base.getBaseDir() / "asset" / "image" / "icon.png"))
        self.iconphoto(True, self.icon_)
        self.wm_iconphoto(True, self.icon_)

        # 应用Win11风格窗口定制
        maliang.theme.customize_window(
            self,
            disable_maximize_button=True,
        )
        maliang.core.configs.Env.system = "Windows11"
        self.resizable(False, False)
        self.center()

        # 创建主画布，支持明暗主题
        self.canvas = maliang.Canvas(
            self,
            expand="xy",
            auto_zoom=True,
            auto_update=True,
            bg="#f3f3f3"  # Win11亮色背景初始值
        )
        self.canvas.place(width=1400, height=1000, x=0, y=0)

        # 注册主题变化事件，更新canvas背景色
        maliang.theme.register_event(self.update_canvas_theme)

        # 标题
        self.title_text = maliang.Text(
            self.canvas, (700, 50), (1400, 100),
            text="HDpip 按钮类型演示",
            fontsize=32, weight="bold", anchor="center"
        )

        self.subtitle_text = maliang.Text(
            self.canvas, (700, 90), (1400, 50),
            text="左边九个普通按钮，右边九个轮廓按钮",
            fontsize=18, anchor="center"
        )

        # 按钮类型定义
        self.button_types = [
            # 普通按钮
            "default", "primary", "secondary", "success",
            "info", "warning", "danger", "light", "dark",
            # 轮廓按钮
            "outline-default", "outline-primary", "outline-secondary", "outline-success",
            "outline-info", "outline-warning", "outline-danger", "outline-light", "outline-dark"
        ]

        # 按钮显示名称（直接作为按钮文本）
        self.button_texts = {
            "default": "默认",
            "primary": "主要",
            "secondary": "次要",
            "success": "成功",
            "info": "信息",
            "warning": "警告",
            "danger": "危险",
            "light": "浅色",
            "dark": "深色",
            "outline-default": "轮廓-默认",
            "outline-primary": "轮廓-主要",
            "outline-secondary": "轮廓-次要",
            "outline-success": "轮廓-成功",
            "outline-info": "轮廓-信息",
            "outline-warning": "轮廓-警告",
            "outline-danger": "轮廓-危险",
            "outline-light": "轮廓-浅色",
            "outline-dark": "轮廓-深色"
        }

        # 所有按钮列表
        self.all_buttons = []

        # 创建控制开关
        self.create_control_switches()

        # 创建所有按钮
        self.create_buttons()

    def create_control_switches(self):
        """创建控制开关：明暗主题切换和全体禁用切换 - 完美居中"""
        control_y = 125

        # 开关按钮宽度和高度
        switch_width = 250
        switch_height = 60
        switch_spacing = 50  # 减小间距，让两个按钮更紧凑

        # 计算起始位置（完美居中）
        total_width = 2 * switch_width + switch_spacing
        start_x = (1400 - total_width) // 2

        # 明暗主题切换开关
        self.theme_switch = HDpip.gui.base.Button(
            self.canvas,
            (start_x, control_y),
            (switch_width, switch_height),
            theme="primary",
            text="🌓 明暗主题切换",
            command=self.toggle_theme
        )

        # 全体禁用切换开关
        self.disable_switch = HDpip.gui.base.Button(
            self.canvas,
            (start_x + switch_width + switch_spacing, control_y),
            (switch_width, switch_height),
            theme="warning",
            text="⏸️ 全体禁用切换",
            command=self.toggle_all_disabled
        )

        # 状态显示 - 在控制按钮组下方居中
        status_width = 500
        status_x = start_x + (total_width - status_width) // 2
        self.status_text = maliang.Text(
            self.canvas, (status_x + status_width//2, control_y + 80),
            (status_width, 40),
            text="状态: 所有按钮已启用 | 主题: 系统默认",
            fontsize=14,
            anchor="center"
        )

        # 初始化状态
        self.all_disabled = False
        self.dark_theme = False

        # 初始主题设置
        self.update_canvas_theme(maliang.theme.get_color_mode())

    def create_buttons(self):
        """创建所有按钮 - 四列布局：5、4、5、4，左边九个普通按钮，右边九个轮廓按钮"""
        # 按钮参数
        button_width = 180
        button_height = 50
        button_spacing_x = 220  # 按钮水平间距
        button_spacing_y = 70   # 按钮垂直间距

        # 普通按钮和轮廓按钮分开
        regular_buttons = self.button_types[:9]  # 前9个是普通按钮
        outline_buttons = self.button_types[9:]  # 后9个是轮廓按钮

        # 起始位置（按钮区域）
        start_x = 100
        start_y = 280

        # 创建四列
        # 列1: 普通按钮 (显示前5个)
        # 列2: 普通按钮 (显示后4个)
        # 列3: 轮廓按钮 (显示前5个)
        # 列4: 轮廓按钮 (显示后4个)

        # 定义列配置：(按钮列表, 起始索引, 按钮数量, X偏移)
        columns = [
            (regular_buttons, 0, 5, 0),           # 列1: 普通按钮前5个
            (regular_buttons, 5, 4, 1),           # 列2: 普通按钮后4个
            (outline_buttons, 0, 5, 2),           # 列3: 轮廓按钮前5个
            (outline_buttons, 5, 4, 3)            # 列4: 轮廓按钮后4个
        ]

        # 创建所有按钮
        for button_list, start_index, count, column_offset in columns:
            for row in range(count):
                btn_type = button_list[start_index + row]
                x = start_x + column_offset * (button_width + button_spacing_x)
                y = start_y + row * button_spacing_y

                button = HDpip.gui.base.Button(
                    self.canvas,
                    (x, y),
                    (button_width, button_height),
                    theme=btn_type,
                    text=self.button_texts[btn_type],
                    anchor="center",
                    command=lambda bt=btn_type: self.on_button_click(bt)
                )
                self.all_buttons.append(button)

        # 添加列标题
        # 普通按钮标题
        regular_title_x = start_x + (button_width + button_spacing_x) // 2
        self.regular_title = maliang.Text(
            self.canvas, (regular_title_x, start_y - 40),
            (button_width + button_spacing_x, 30),
            text="普通按钮 (9种)",
            fontsize=16, weight="bold", anchor="center"
        )

        # 轮廓按钮标题
        outline_title_x = start_x + 2 * (button_width + button_spacing_x) + (button_width + button_spacing_x) // 2
        self.outline_title = maliang.Text(
            self.canvas, (outline_title_x, start_y - 40),
            (button_width + button_spacing_x, 30),
            text="轮廓按钮 (9种)",
            fontsize=16, weight="bold", anchor="center"
        )

    def on_button_click(self, button_type):
        """按钮点击事件"""
        print(f"按钮被点击: {button_type}")

        # 更新状态显示
        self.status_text.set(f"点击了: {self.button_texts[button_type]} | 主题: {'暗色' if self.dark_theme else '亮色'} | 状态: {'禁用' if self.all_disabled else '启用'}")

    def toggle_theme(self):
        """切换明暗主题"""
        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            maliang.theme.set_color_mode("dark")
            # 直接设置按钮文本属性
            self.theme_switch.text = "🌙 切换到亮色主题"
        else:
            maliang.theme.set_color_mode("light")
            self.theme_switch.text = "☀️ 切换到暗色主题"

        # 更新canvas主题
        self.update_canvas_theme(maliang.theme.get_color_mode())

        # 更新所有按钮的主题
        self.update_all_buttons_theme()

        # 更新状态显示
        self.update_status()

    def toggle_all_disabled(self):
        """切换全体禁用状态"""
        self.all_disabled = not self.all_disabled

        # 切换所有按钮的禁用状态
        for button in self.all_buttons:
            button.disable(self.all_disabled)

        if self.all_disabled:
            self.disable_switch.text = "▶️ 启用所有按钮"
        else:
            self.disable_switch.text = "⏸️ 禁用所有按钮"

        # 更新状态显示
        self.update_status()

    def update_canvas_theme(self, color_mode):
        """更新canvas和文本元素的主题"""
        # 更新canvas背景色
        if color_mode == "dark":
            self.canvas.configure(bg="#1e1e1e")  # Win11暗色背景
        else:
            self.canvas.configure(bg="#f3f3f3")  # Win11亮色背景

        # 强制更新canvas
        self.canvas.update()

    def update_all_buttons_theme(self):
        """更新所有按钮的主题"""
        for button in self.all_buttons:
            # 重新应用禁用状态来触发主题更新
            current_disabled = getattr(button, 'disabled', False)
            button.disable(current_disabled)

    def update_status(self):
        """更新状态显示"""
        theme_text = "暗色" if self.dark_theme else "亮色"
        state_text = "禁用" if self.all_disabled else "启用"
        self.status_text.set(text = f"状态: 所有按钮已{state_text} | 主题: {theme_text}")

def show_button_demo():
    """
    显示按钮演示窗口的便捷函数。

    :return: ButtonDemo实例
    """
    demo = ButtonDemo()
    demo.mainloop()
    return demo

if __name__ == "__main__":
    # 运行按钮演示
    show_button_demo()
