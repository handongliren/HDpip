import sys
import os
import subprocess
import json
import shutil
from datetime import datetime

# PyQt6模块导入
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QMessageBox, QTextEdit, QRadioButton, QButtonGroup,
    QStatusBar, QSplitter, QTabWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QAction


class PipManager(QMainWindow):
    """PIP图形化管理工具主窗口类"""

    def __init__(self):
        super().__init__()

        # 窗口基本设置
        self.setWindowTitle('Python PIP图形化管理工具')
        self.setGeometry(100, 100, 800, 600)

        # 初始化成员变量
        self.python_installations = []  # 存储Python安装信息
        self.current_python = None      # 当前选中的Python
        self.installed_packages = []    # 当前Python已安装的包
        self.current_mirror = None      # 当前使用的镜像源

        # 初始化镜像源配置
        self.mirrors = {
            "官方": "https://pypi.org/simple/",
            "官方测试": "https://test.pypi.org/simple/",
            "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "阿里云（推荐）": "https://mirrors.aliyun.com/pypi/simple/",
            "网易": "https://mirrors.163.com/pypi/simple/",
            "豆瓣": "https://pypi.douban.com/simple/",
            "百度云": "https://mirror.baidu.com/pypi/simple/",
            "中国科技大学（推荐）": "https://pypi.mirrors.ustc.edu.cn/simple/",
            "华为云": "https://mirrors.huaweicloud.com/repository/pypi/simple/",
            "腾讯云": "https://mirrors.cloud.tencent.com/pypi/simple/",
        }

        # 初始化UI
        self.init_ui()

        # 加载配置
        self.load_config()

        # 显示欢迎信息
        self.info_text.setText("欢迎使用Python PIP图形化管理工具\n\n"
                             "请点击「列出Python」按钮扫描系统中的Python安装\n"
                             "或者直接选择上方列表中的Python版本开始管理")

        # 加载Python安装列表
        self.find_python_installations()

    def init_ui(self):
        """初始化用户界面组件"""
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建菜单栏
        self.init_menu_bar()

        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 上方部分 - Python版本列表
        python_group = QWidget()
        python_layout = QVBoxLayout()
        python_group.setLayout(python_layout)

        python_label = QLabel('已安装的Python列表')
        python_layout.addWidget(python_label)

        self.python_list = QListWidget()
        self.python_list.setMinimumHeight(140)  # 设置最小高度
        self.python_list.setMaximumHeight(200)  # 设置最大高度
        self.python_list.itemClicked.connect(self.on_python_selected)
        python_layout.addWidget(self.python_list)

        main_layout.addWidget(python_group)

        # 按钮工具栏
        button_layout = QHBoxLayout()

        self.list_python_btn = QPushButton('列出Python')
        self.list_python_btn.clicked.connect(self.find_python_installations)
        button_layout.addWidget(self.list_python_btn)

        self.install_pkg_btn = QPushButton('安装包')
        self.install_pkg_btn.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_pkg_btn)

        self.uninstall_pkg_btn = QPushButton('卸载包')
        self.uninstall_pkg_btn.clicked.connect(self.uninstall_package)
        button_layout.addWidget(self.uninstall_pkg_btn)

        self.upgrade_pkg_btn = QPushButton('升级包')
        self.upgrade_pkg_btn.clicked.connect(self.upgrade_package)
        button_layout.addWidget(self.upgrade_pkg_btn)

        self.mirror_btn = QPushButton('设置镜像源')
        self.mirror_btn.clicked.connect(self.show_mirror_dialog)
        button_layout.addWidget(self.mirror_btn)

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self.refresh_package_list)
        button_layout.addWidget(self.refresh_btn)

        # 添加帮助按钮
        self.help_btn = QPushButton('帮助')
        self.help_btn.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_btn)

        main_layout.addLayout(button_layout)

        # 下方分割区域：包列表和信息显示
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧 - 已安装包列表
        package_group = QWidget()
        package_layout = QVBoxLayout()
        package_group.setLayout(package_layout)

        package_label = QLabel('已安装的包列表')
        package_layout.addWidget(package_label)

        self.package_list = QListWidget()
        self.package_list.setMinimumHeight(260)  # 设置最小高度
        self.package_list.itemClicked.connect(self.show_package_info)
        package_layout.addWidget(self.package_list)

        splitter.addWidget(package_group)

        # 右侧 - 信息日志
        info_group = QWidget()
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        info_label = QLabel('信息日志')
        info_layout.addWidget(info_label)

        self.info_text = QTextEdit()
        self.info_text.setMinimumHeight(260)  # 设置最小高度
        self.info_text.setReadOnly(True)
        info_layout.addWidget(self.info_text)

        splitter.addWidget(info_group)

        # 设置分割区域的初始大小比例
        splitter.setSizes([300, 300])  # 左右两部分初始宽度比例

        # 将分割区域添加到主布局，并设置拉伸因子
        main_layout.addWidget(splitter, stretch=1)  # stretch=1表示该部分会占用更多可用空间

        # 调整整体窗口大小策略
        main_layout.setStretchFactor(python_group, 1)  # Python列表部分
        main_layout.setStretchFactor(splitter, 3)      # 下半部分（包列表和信息日志）

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 显示当前镜像源
        self.mirror_label = QLabel('镜像源: 未设置')
        self.status_bar.addPermanentWidget(self.mirror_label)

        # 显示当前Python版本
        self.python_label = QLabel('Python: 未选择')
        self.status_bar.addPermanentWidget(self.python_label)

        # 初始状态
        self.status_bar.showMessage('准备就绪', 3000)

    def init_menu_bar(self):
        """初始化菜单栏"""
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu('文件(&F)')

        refresh_action = QAction('刷新包列表', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_package_list)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 工具菜单
        tools_menu = menu_bar.addMenu('工具(&T)')

        list_python_action = QAction('列出Python版本', self)
        list_python_action.triggered.connect(self.find_python_installations)
        tools_menu.addAction(list_python_action)

        mirror_action = QAction('设置镜像源', self)
        mirror_action.triggered.connect(self.show_mirror_dialog)
        tools_menu.addAction(mirror_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu('帮助(&H)')

        help_action = QAction('使用帮助', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_help(self):
        """显示帮助对话框"""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle('使用帮助')
        help_dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        # 创建选项卡
        tab_widget = QTabWidget()

        # 基本使用选项卡
        basic_tab = QWidget()
        basic_layout = QVBoxLayout()
        basic_tab.setLayout(basic_layout)

        basic_help = QTextEdit()
        basic_help.setReadOnly(True)
        basic_help.setHtml("""
        <h2>基本使用</h2>
        <p>Python PIP图形化管理工具让您可以轻松管理多个Python环境的包。</p>

        <h3>快速入门</h3>
        <ol>
            <li><b>选择Python版本</b>: 启动时工具会自动扫描系统中的Python安装。点击上方列表中的某个Python版本进行选择。</li>
            <li><b>查看已安装的包</b>: 选择Python版本后，下方列表会显示该版本已安装的所有包。</li>
            <li><b>安装新包</b>: 点击"安装包"按钮，输入包名和可选的版本号。</li>
            <li><b>升级或卸载</b>: 在包列表中选择一个包，然后点击相应的按钮。</li>
        </ol>

        <h3>按钮功能说明</h3>
        <ul>
            <li><b>列出Python</b>: 扫描系统中所有安装的Python版本</li>
            <li><b>安装包</b>: 安装新的Python包</li>
            <li><b>卸载包</b>: 卸载选中的包</li>
            <li><b>升级包</b>: 将选中的包升级到最新版本</li>
            <li><b>设置镜像源</b>: 选择或自定义PyPI镜像源</li>
            <li><b>刷新</b>: 刷新当前Python环境的包列表</li>
        </ul>
        """)
        basic_layout.addWidget(basic_help)

        # 镜像源选项卡
        mirror_tab = QWidget()
        mirror_layout = QVBoxLayout()
        mirror_tab.setLayout(mirror_layout)

        mirror_help = QTextEdit()
        mirror_help.setReadOnly(True)
        mirror_help.setHtml("""
        <h2>镜像源设置</h2>
        <p>使用国内镜像源可以大幅提高包的下载速度。本工具内置了以下常用镜像源：</p>

        <ul>
            <li><b>官方</b>: https://pypi.org/simple/（国内访问较慢！）,
            <li><b>官方测试</b>: https://test.pypi.org/simple/（国内访问较慢，<b>并且这不是一个正式源！</b>）,
            <li><b>清华大学</b>: https://pypi.tuna.tsinghua.edu.cn/simple/,
            <li><b>阿里云</b>: https://mirrors.aliyun.com/pypi/simple/（推荐）,
            <li><b>网易</b>: https://mirrors.163.com/pypi/simple/,
            <li><b>豆瓣</b>: https://pypi.douban.com/simple/,
            <li><b>百度云</b>: https://mirror.baidu.com/pypi/simple/,
            <li><b>中国科技大学</b>: https://pypi.mirrors.ustc.edu.cn/simple/（推荐）,
            <li><b>华为云</b>: https://mirrors.huaweicloud.com/repository/pypi/simple/,
            <li><b>腾讯云</b>: https://mirrors.cloud.tencent.com/pypi/simple/,
        </ul>

        <h3>如何设置镜像源</h3>
        <ol>
            <li>点击"设置镜像源"按钮或从"工具"菜单选择"设置镜像源"</li>
            <li>在弹出的对话框中选择预设镜像源，或选择"自定义"并输入镜像源URL</li>
            <li>点击"确定"保存设置</li>
        </ol>

        <p>镜像源设置会被保存，下次启动程序时自动加载。</p>
        """)
        mirror_layout.addWidget(mirror_help)

        # 常见问题选项卡
        faq_tab = QWidget()
        faq_layout = QVBoxLayout()
        faq_tab.setLayout(faq_layout)

        faq_help = QTextEdit()
        faq_help.setReadOnly(True)
        faq_help.setHtml("""
        <h2>常见问题</h2>

        <h3>Q: 为什么我的Python版本没有被检测到？</h3>
        <p>A: 工具会尝试检测常见位置的Python安装。如果您的Python安装在非标准位置，可能需要手动添加。</p>

        <h3>Q: 安装包时出现权限错误怎么办？</h3>
        <p>A: 在Windows上，您可能需要以管理员身份运行此工具。在Linux/Mac上，可以尝试使用用户目录下的Python环境或者使用虚拟环境。</p>

        <h3>Q: 如何处理版本冲突？</h3>
        <p>A: 建议使用虚拟环境(venv)来隔离不同项目的依赖。可以使用不同的Python解释器创建多个虚拟环境。</p>

        <h3>Q: 镜像源设置后没有生效？</h3>
        <p>A: 请确保镜像源URL格式正确，并且该镜像站点可以访问。可以尝试重新设置镜像源或选择其他镜像站点。</p>

        <h3>Q: 为什么有些包无法安装？</h3>
        <p>A: 可能是因为该包不支持您的Python版本，或者依赖了一些系统级库。请查看错误信息了解详情。</p>
        """)
        faq_layout.addWidget(faq_help)

        # 将选项卡添加到窗口
        tab_widget.addTab(basic_tab, "基本使用")
        tab_widget.addTab(mirror_tab, "镜像源设置")
        tab_widget.addTab(faq_tab, "常见问题")

        layout.addWidget(tab_widget)

        # 添加关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(help_dialog.accept)
        layout.addWidget(close_button)

        help_dialog.setLayout(layout)
        help_dialog.exec()

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于 Python PIP 图形化管理工具",
            """<h3>Python PIP 图形化管理工具 v1.1.0</h3>
            <p>一个用于管理多个Python版本包的图形界面工具</p>
            <p>主要功能:</p>
            <ul>
                <li>扫描和管理多个Python安装</li>
                <li>安装、卸载和升级包</li>
                <li>支持多种镜像源切换</li>
                <li>查看包详细信息</li>
            </ul>
            <p>Copyright &copy; 2025 寒冬利刃.All Rights Reserved.</p>"""
        )

    def load_config(self):
        """加载配置文件"""
        config_path = os.path.expanduser('~/.pip-multi-gui-config')

        try:
            # 尝试加载配置文件
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_mirror = config.get('current_mirror')
                    if self.current_mirror:
                        self.mirror_label.setText(f'镜像源: {self.get_mirror_name(self.current_mirror)}')
        except Exception as e:
            QMessageBox.warning(self, '配置错误', f'加载配置文件失败: {str(e)}')

    def save_config(self):
        """保存配置文件"""
        config_path = os.path.expanduser('~/.pip-multi-gui-config')
        config = {
            'current_mirror': self.current_mirror
        }

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, '配置错误', f'保存配置文件失败: {str(e)}')

    def get_mirror_name(self, url):
        """根据URL获取镜像源名称"""
        for name, mirror_url in self.mirrors.items():
            if mirror_url == url:
                return name
        return '自定义源'

    def _get_startupinfo(self):
        """获取隐藏命令窗口的startupinfo对象"""
        if sys.platform.startswith('win'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None

    def find_python_installations(self):
        """查找系统中安装的所有Python版本"""
        self.python_installations = []
        self.python_list.clear()

        # 添加日志提示
        self.info_text.clear()
        self.info_text.append("正在扫描系统中的Python安装，请稍候...\n")
        QApplication.processEvents()  # 立即更新UI

        try:
            # 在Windows系统上查找Python安装
            if sys.platform == 'win32':
                self._find_windows_pythons()
            # 在Unix/Linux/Mac系统上查找Python安装
            else:
                self._find_unix_pythons()

            # 更新UI
            for python in self.python_installations:
                item = QListWidgetItem(f"{python['version']} ({python['path']})")
                self.python_list.addItem(item)

            # 添加结果日志
            self.info_text.append(f"扫描完成，找到 {len(self.python_installations)} 个Python安装\n")
            for i, python in enumerate(self.python_installations, 1):
                self.info_text.append(f"{i}. {python['version']} - {python['path']}")

            # 如果有Python安装，选择第一个
            if self.python_installations:
                self.python_list.setCurrentRow(0)
                self.on_python_selected(self.python_list.item(0))

            self.status_bar.showMessage(f'找到 {len(self.python_installations)} 个Python安装', 3000)

        except Exception as e:
            self.info_text.append(f"扫描失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'查找Python安装失败: {str(e)}')

    def _find_windows_pythons(self):
        """查找Windows上的Python安装"""
        # 可能的Python安装路径
        possible_paths = []

        # 检查Program Files
        program_files = [
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        ]

        # 添加用户目录下的AppData\Local
        user_profile = os.environ.get('USERPROFILE', '')
        if user_profile:
            program_files.append(os.path.join(user_profile, 'AppData', 'Local'))

        # 查找Python目录
        for base_dir in program_files:
            if os.path.exists(base_dir):
                for item in os.listdir(base_dir):
                    if item.lower().startswith('python'):
                        python_dir = os.path.join(base_dir, item)
                        possible_paths.append(python_dir)

        # 添加系统PATH中的Python
        for path in os.environ.get('PATH', '').split(os.pathsep):
            if 'python' in path.lower():
                possible_paths.append(path)

        # 检查每个可能的路径
        for path in possible_paths:
            python_exe = os.path.join(path, 'python.exe')
            if os.path.exists(python_exe):
                self._add_python_installation(python_exe)

    def _find_unix_pythons(self):
        """查找Unix/Linux/Mac上的Python安装"""
        # 常见的Python可执行文件名
        python_executables = ['python', 'python3', 'python2']

        # 使用which命令查找Python
        for exe in python_executables:
            try:
                result = subprocess.run(['which', exe],
                                      capture_output=True, text=True, check=False)
                if result.returncode == 0 and result.stdout.strip():
                    self._add_python_installation(result.stdout.strip())
            except Exception:
                pass

        # 检查常见安装位置
        common_paths = [
            '/usr/bin', '/usr/local/bin', '/opt/local/bin',
            '/Library/Frameworks/Python.framework/Versions'
        ]

        for base_path in common_paths:
            if os.path.exists(base_path):
                for item in os.listdir(base_path):
                    if any(item.startswith(exe) for exe in python_executables):
                        python_path = os.path.join(base_path, item)
                        if os.path.isfile(python_path) and os.access(python_path, os.X_OK):
                            self._add_python_installation(python_path)

    def _add_python_installation(self, python_path):
        """添加Python安装到列表"""
        try:
            # 获取Python版本
            result = subprocess.run(
                [python_path, '--version'],
                capture_output=True, text=True, check=False,
                startupinfo=self._get_startupinfo()
            )

            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()

                # 检查是否已存在相同路径
                for existing in self.python_installations:
                    if existing['path'] == python_path:
                        return

                self.python_installations.append({
                    'path': python_path,
                    'version': version
                })
        except Exception:
            pass

    def on_python_selected(self, item):
        """处理Python选择事件"""
        if not item:
            return

        index = self.python_list.row(item)
        if 0 <= index < len(self.python_installations):
            self.current_python = self.python_installations[index]
            self.python_label.setText(f"Python: {self.current_python['version']}")
            self.refresh_package_list()

    def refresh_package_list(self):
        """刷新当前Python的已安装包列表"""
        if not self.current_python:
            QMessageBox.warning(self, '警告', '请先选择一个Python版本')
            return

        # 添加日志提示
        self.info_text.clear()
        self.info_text.append(f"正在获取 {self.current_python['version']} 的已安装包列表...\n")
        QApplication.processEvents()  # 立即更新UI

        try:
            # 执行pip list命令获取已安装包
            result = subprocess.run(
                [self.current_python['path'], '-m', 'pip', 'list', '--format=json'],
                capture_output=True, text=True, check=False,
                startupinfo=self._get_startupinfo()
            )

            if result.returncode == 0:
                # 解析JSON结果
                self.installed_packages = json.loads(result.stdout)
                self.update_package_list_display()

                # 更新日志
                self.info_text.append(f"成功获取 {len(self.installed_packages)} 个已安装的包\n")
                self.info_text.append("选择左侧列表中的包可查看详细信息")

                self.status_bar.showMessage('包列表刷新成功', 3000)
            else:
                error_msg = result.stderr.strip() or '未知错误'
                raise Exception(error_msg)
        except Exception as e:
            self.info_text.append(f"获取包列表失败: {str(e)}")
            QMessageBox.critical(self, '错误', f'获取包列表失败: {str(e)}')
            self.status_bar.showMessage('获取包列表失败', 3000)

    def update_package_list_display(self):
        """更新包列表显示"""
        self.package_list.clear()

        # 按名称排序
        sorted_packages = sorted(self.installed_packages, key=lambda x: x['name'].lower())

        # 添加到列表控件
        for pkg in sorted_packages:
            item = QListWidgetItem(f"{pkg['name']}=={pkg['version']}")
            self.package_list.addItem(item)

    def show_package_info(self, item):
        """显示选中包的详细信息"""
        if not item:
            return

        pkg_name = item.text().split('==')[0]

        # 添加日志提示
        self.info_text.clear()
        self.info_text.append(f"正在获取 {pkg_name} 的详细信息...\n")
        QApplication.processEvents()  # 立即更新UI

        try:
            # 执行pip show命令获取包详情
            result = subprocess.run(
                [self.current_python['path'], '-m', 'pip', 'show', pkg_name],
                capture_output=True, text=True, check=False,
                startupinfo=self._get_startupinfo()
            )

            if result.returncode == 0:
                self.info_text.clear()
                self.info_text.append(f"== {pkg_name} 详细信息 ==\n")
                self.info_text.append(result.stdout)
            else:
                raise Exception(result.stderr.strip() or '未知错误')
        except Exception as e:
            self.info_text.append(f"获取包信息失败: {str(e)}")

    def install_package(self):
        """安装Python包"""
        if not self.current_python:
            QMessageBox.warning(self, '警告', '请先选择一个Python版本')
            return

        # 创建自定义对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('安装包')
        layout = QFormLayout()

        # 包名输入框
        pkg_name_edit = QLineEdit()
        layout.addRow('包名:', pkg_name_edit)

        # 版本号输入框
        version_edit = QLineEdit()
        version_edit.setPlaceholderText('可选，如: 1.0.0')
        layout.addRow('版本号:', version_edit)

        # 确定和取消按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        layout.addRow(btn_box)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            pkg_name = pkg_name_edit.text().strip()
            version = version_edit.text().strip()

            if not pkg_name:
                QMessageBox.warning(self, '警告', '包名不能为空')
                return

            # 显示使用的镜像源信息
            mirror_info = ""
            if self.current_mirror:
                mirror_info = f"\n镜像源: {self.get_mirror_name(self.current_mirror)}"

            # 确认安装
            confirm = QMessageBox.question(
                self, '确认安装',
                f'确定要安装 {pkg_name}{"=="+version if version else ""} 吗?{mirror_info}',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                self.run_pip_command('install', pkg_name, version=version)

    def uninstall_package(self):
        """卸载Python包"""
        if not self.current_python:
            QMessageBox.warning(self, '警告', '请先选择一个Python版本')
            return

        selected_item = self.package_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, '警告', '请先选择一个包')
            return

        pkg_name = selected_item.text().split('==')[0]

        # 确认卸载
        confirm = QMessageBox.question(
            self, '确认卸载',
            f'确定要卸载 {pkg_name} 吗?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.run_pip_command('uninstall', pkg_name)

    def upgrade_package(self):
        """升级Python包"""
        if not self.current_python:
            QMessageBox.warning(self, '警告', '请先选择一个Python版本')
            return

        selected_item = self.package_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, '警告', '请先选择一个包')
            return

        pkg_name = selected_item.text().split('==')[0]

        # 确认升级
        confirm = QMessageBox.question(
            self, '确认升级',
            f'确定要升级 {pkg_name} 吗?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.run_pip_command('install', pkg_name, upgrade=True)

    def run_pip_command(self, command, pkg_name, version=None, upgrade=False):
        """执行pip命令的通用方法"""
        if not self.current_python:
            QMessageBox.warning(self, '警告', '请先选择一个Python版本')
            return

        # 构建命令
        cmd = [self.current_python['path'], '-m', 'pip', command, pkg_name]

        # 卸载时自动确认
        if command == 'uninstall':
            cmd.append('--yes')

        # 添加版本号
        if version:
            cmd[-1] = f"{pkg_name}=={version}"

        # 添加升级标志
        if upgrade:
            cmd.append('--upgrade')

        # 添加镜像源(卸载操作不需要)
        if self.current_mirror and command != 'uninstall':
            cmd.extend(['-i', self.current_mirror])
            host = self.current_mirror.split('//')[1].split('/')[0]
            cmd.extend(['--trusted-host', host])

        # 清空并准备显示输出
        self.info_text.clear()
        self.info_text.append(f"执行命令: {' '.join(cmd)}\n")
        self.info_text.append("正在处理，请稍候...\n")
        QApplication.processEvents()  # 立即更新UI

        try:
            # 创建隐藏窗口的startupinfo对象(仅Windows系统)
            startupinfo = self._get_startupinfo()

            # 执行命令并实时输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                startupinfo=startupinfo  # 添加这个参数来隐藏窗口
            )

            # 实时读取输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.info_text.append(output.strip())
                    QApplication.processEvents()  # 更新UI

            # 获取最终返回码
            return_code = process.wait()

            # 显示结果
            if return_code == 0:
                operation_name = {
                    'install': '安装',
                    'uninstall': '卸载',
                }

                op_name = operation_name.get(command, command)
                if upgrade:
                    op_name = '升级'

                success_msg = f"\n{op_name}操作成功完成!"
                self.info_text.append(success_msg)
                self.status_bar.showMessage(f"{op_name} {pkg_name} 成功", 5000)
                self.refresh_package_list()
            else:
                error_output = process.stderr.read()
                self.info_text.append(f"\n错误信息:\n{error_output}")
                raise Exception(error_output)

        except Exception as e:
            self.status_bar.showMessage(f"操作失败", 5000)
            QMessageBox.critical(
                self, '操作失败',
                f'操作执行失败:\n{str(e)}'
            )
            self.info_text.append(f"\n错误信息:\n{str(e)}")

    def show_mirror_dialog(self):
        """显示镜像源设置对话框"""
        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('设置镜像源')
        layout = QVBoxLayout()

        # 添加说明
        layout.addWidget(QLabel("选择或输入要使用的PyPI镜像源:"))

        # 添加镜像源选项
        mirror_group = QButtonGroup()
        for i, (name, url) in enumerate(self.mirrors.items()):
            radio = QRadioButton(f"{name} ({url})")
            radio.setProperty('url', url)
            if url == self.current_mirror:
                radio.setChecked(True)
            mirror_group.addButton(radio, i)
            layout.addWidget(radio)

        # 自定义镜像源输入
        custom_radio = QRadioButton('自定义')
        mirror_group.addButton(custom_radio, len(self.mirrors))
        layout.addWidget(custom_radio)

        custom_edit = QLineEdit()
        if self.current_mirror and self.get_mirror_name(self.current_mirror) == '自定义源':
            custom_edit.setText(self.current_mirror)
            custom_radio.setChecked(True)
        else:
            custom_edit.setPlaceholderText('输入镜像源URL，例如: https://pypi.org/simple')
        layout.addWidget(custom_edit)

        # 添加单选按钮点击事件
        def on_radio_clicked(button):
            if button != custom_radio:
                url = button.property('url')
                if url:
                    custom_edit.setText(url)

        # 连接信号
        for i in range(mirror_group.buttons().__len__()):
            button = mirror_group.button(i)
            if button:
                button.clicked.connect(lambda checked, btn=button: on_radio_clicked(btn))

        # 确定和取消按钮
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        layout.addWidget(btn_box)

        dialog.setLayout(layout)

        # 处理对话框结果
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = mirror_group.checkedButton()
            if selected == custom_radio and custom_edit.text():
                self.current_mirror = custom_edit.text()
            elif selected != custom_radio:
                self.current_mirror = selected.property('url')

            # 更新UI和配置
            self.mirror_label.setText(f'镜像源: {self.get_mirror_name(self.current_mirror)}')
            self.save_config()

            # 更新日志
            self.info_text.clear()
            self.info_text.append(f"已设置镜像源: {self.get_mirror_name(self.current_mirror)}")
            self.info_text.append(f"镜像源URL: {self.current_mirror}")

            self.status_bar.showMessage('镜像源设置成功', 3000)

    def closeEvent(self, event):
        """重写关闭事件，保存配置"""
        self.save_config()
        event.accept()


def main():
    """主程序入口"""
    app = QApplication(sys.argv)
    window = PipManager()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
