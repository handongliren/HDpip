# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 概述

HDpip 是一个基于 maliang UI 框架（tkinter 基础）的图形化 pip 包管理器。它提供了一个 GUI 界面，用于管理多个 Python 安装环境中的包，支持镜像源、包操作（安装/卸载/升级）和多语言界面。

该项目发布为 PyPI 可安装包 (`HDpip`)，包含入口点 `HDpip` 和 `hdpip`。仓库中还有一个独立的基于 PyQt6 的 GUI (`pipgui.py`)，但它不是主包的一部分。

## 项目结构

```txt
HDpip/                 # 主包
├── core/              # 核心逻辑
│   ├── base.py        # 数据管理器、Version 类、shell 工具、错误类型
│   ├── pip.py         # Pip 命令包装器和包操作
│   └── pyi.py         # （可能是类型存根生成）
├── gui/               # 基于 Maliang 的 GUI 组件
│   ├── base.py        # Bootstrap 风格按钮、滚动文本框、动画
│   ├── welcome.py     # 欢迎/向导窗口
│   ├── buttons.py     # （额外的按钮变体）
│   ├── treeview_.py   # 树形视图组件
│   ├── new.py         # （新的 GUI 面板）
│   └── old.py         # （旧版 GUI 面板）
├── setting/           # 默认 JSON 设置（global.json, auto.*.json）
├── language/          # i18n JSON 文件
├── asset/             # 图片/图标
└── main.py            # 入口点（检测首次运行 → 欢迎界面）
```

顶层文件：

- `setup.py` – 包配置（从 `HDpip` 模块导入版本号）
- `dist.py` – 构建脚本，清理目录并运行 `python setup.py sdist`
- `local_install.py` – 开发安装脚本（清除缓存、卸载旧版本、从 `dist/` 安装）
- `pipgui.py` – 独立的 PyQt6 GUI（不是 HDpip 包的一部分）
- `test.py` – 核心功能的临时测试
- `dev` – 空文件，启用开发模式（`HDpip.core.base.isDev()`）

**注意：** 包 README (`HDpip/README.md`) 用于 PyPI 分发，与仓库级别的 README 是分开的。

## 开发命令

| 用途 | 命令 |
| ---- | ---- |
| 运行主 GUI（开发） | `python -m HDpip.main` |
| 运行主 GUI（安装后） | `HDpip` 或 `hdpip` |
| 运行独立的 PyQt6 GUI | `python pipgui.py` |
| 构建分发压缩包 | `python dist.py` |
| 本地安装测试 | `python local_install.py` |
| 运行临时测试 | `python test.py` |
| 检查 Python/pip 版本 | `python -c "from HDpip.core.base import getPythonVersion, getPipVersion; print(getPythonVersion(), getPipVersion())"` |
| 列出已安装包 | `python -c "import HDpip.core.pip; print(HDpip.core.pip.list())"` |
| 打开包目录 | `python -c "import HDpip.core.base; HDpip.core.base.openInExplorer('HDpip')"` |

**注意：** 没有正式的测试套件或代码检查配置。`test.py` 文件包含核心功能的临时测试。

## 开发设置

1. **安装依赖**（参见 `setup.py`）：

   ```bash
   pip install "pip>=25.2" "maliang[opt]>=3.1.0" pyyaml "pipdeptree>=2.0.0"
   ```

2. **启用开发模式** – 在仓库根目录（或父目录）创建一个空的 `dev` 文件以触发仅开发行为。

3. **运行 GUI**（开发期间）：

   ```bash
   python -m HDpip.main
   ```

   或安装后：

   ```bash
   HDpip
   ```

4. **测试 PyQt6 GUI**（可选）：

   ```bash
   python pipgui.py
   ```

## 构建和分发

构建过程使用 `HDpip.main.version` 中的版本号：

1. `setup.py` 从 `HDpip` 模块导入 `version`（该模块重新导出 `HDpip.main.version`）。
2. `dist.py` 清理构建目录并运行 `python setup.py sdist`。
3. 生成的压缩包重命名为小写（`hdpip-{version}.tar.gz`）。
4. **本地安装**（用于测试）通过 `local_install.py` 完成，它会清除 pip 缓存、卸载现有的 HDpip，并从 `dist/` 安装新构建的包。

要构建并本地安装：

```bash
python dist.py
python local_install.py
```

## 代码规范

规则定义在 `.clinerules/code.md` 中：

- **文件/变量名**：小写英文下划线分隔（`test_connect.py`, `connect_ip`）
- **函数名**：小驼峰命名（`connect_init`）
- **类名**：大驼峰命名（`ConnectPool`）
- **导入**：按顺序分组：标准库、第三方包、本地模块。组之间用空行分隔。本地模块必须相对导入
- **文档字符串**：用中文（或英文）编写，文档字符串和代码之间空一行
- **注释**：避免使用 `#` 注释；在文档字符串中解释意图
- **不要重复造轮子** – 除非现有抽象已损坏，否则使用代码库中的现有抽象
- **`key = value` 传参** — 等号左右必须有空格；逗号后加空格（`"a", "b"`）
- **`from typing import *`** — 允许使用，不需要显式导入
- **参数列表** — 每个参数末尾加逗号（包括最后一个），`self` 后也加
- **`super().__init__`** — 单行传全部参数，不换行
- **不写 `**kwargs`** — 显式列出所有参数，不用通配
- **相对导入** — 必须 `try/except ImportError` 包裹，fallback 用 `sys.path` 追加 + 绝对导入

- **`widget.set(str)`** — maliang 控件改文本统一用 `widget.set()`
- **Canvas 子画布** — 方法顺序严格：`renderLanguage` → `onLanguageChange` → `destroy` → `__init__`
- **语言事件** — `data_manager.language.registerEvent(self.onLanguageChange)` 注册，`destroy` 中 `unregisterEvent`

`.clinerules/role.md` 包含额外的项目特定指导。

## 测试

仓库包含 `test.py` 用于核心功能的临时测试。运行：

```bash
python test.py
```

没有正式的测试套件（pytest, unittest）。`test.py` 中的测试演示了 `HDpip.core.base.Version`、`HDpip.core.base.Data`、`HDpip.core.pip` 和其他工具的使用。

## 架构亮点

### 数据管理

- `HDpip.core.base.Data` – JSON 文件包装器，带有事件系统（`open`、`load`、`save`、`__getitem__` 等）。支持通过元组进行嵌套键访问。
- `HDpip.core.base.DataManager` – 管理用户设置和语言文件。首次运行时初始化默认配置。设置更改时自动重新加载语言。

### 版本处理

- `HDpip.core.base.Version` – 语义版本类，具有丰富的比较、格式化和多条件匹配（`multipleCompare`）。用于 Python/pip 版本检测。

### Pip 集成

- `HDpip.core.pip` – 包装 `pip list`、`pip show`、`pip install`、`pip uninstall`，支持实时输出捕获和镜像源。

### GUI 框架

- 基于 **maliang**（一个 tkinter 基础的 UI 库）。`gui.base` 模块提供 Bootstrap 风格的组件（`Button`、`ScrolledText`），支持浅色/深色主题。
- 窗口使用淡入/淡出动画（`WindowFadeIn`、`WindowFadeOut`）。
- 欢迎流程（`gui.welcome.Welcome`）在首次启动或未接受许可证时运行。

### 国际化

- 语言文件是 JSON 字典，存储在 `HDpip/language/`（默认）和 `$PYTHONPATH/HDpip/language/`（自定义）中。`language_code_dict` 将区域代码映射到显示名称。

### 仅开发行为

- 当 `dev` 文件存在时，`HDpip.core.base.isDev()` 返回 `True`。可用于启用调试功能或备用路径。

### 类型存根生成

- `HDpip.core.pyi` 包含从 Python 源代码生成 `.pyi` 类型存根文件的工具。内部用于开发。

## 注意事项

- PyQt6 GUI (`pipgui.py`) 是一个独立的工具，**不**构建到 HDpip 包中。
- `HDpip.core.base.HDpipError` 异常用于内部错误；`unfinished()` 为未实现的功能引发错误。
- 镜像源定义在 `HDpip/setting/auto.*.json` 中，可以在运行时选择。
- 项目使用 GPL-3.0 许可证（参见 `setup.py` 分类器）。
