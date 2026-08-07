# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 概述

HDpip 是一个基于 maliang UI 框架（tkinter 基础）的图形化 pip 包管理器。它提供了一个 GUI 界面，用于管理多个 Python 安装环境中的包，支持镜像源、包操作（安装/卸载/升级）和多语言界面。

该项目发布为 PyPI 可安装包 (`HDpip`)，包含入口点 `HDpip` 和 `hdpip`。仓库中还有一个独立的基于 PyQt6 的 GUI (`pipgui.py`)，但它不是主包的一部分。

## 项目结构

```txt
HDpip/                 # 主包
├── core/              # 核心逻辑
│   ├── util.py        # HDpipError, unfinished, Version, multipleSpilt
│   ├── system.py      # shell, shellDecode, getBaseDir, getPythonPath,
│   │                  #   get*Version, getSystemVersion, openInExplorer, isDev
│   ├── data.py        # Data, DataManager, isBelongedToHDpip
│   ├── pip_api.py     # Pip 命令包装器和包操作
│   └── __init__.py    # 导出 data/pip_api/system/util 子模块
├── gui/               # 基于 Maliang 的 GUI 组件
│   ├── base.py        # Button(主题), ScrolledText, RoundedRectangle, Line,
│   │                  #   WindowFadeIn/Out, smartScale/ss, getDpi/pxToPt/ptToPx
│   ├── welcome.py     # 欢迎/向导窗口（Canvas 序列）
│   ├── dialog.py      # DialogCanvas / DialogToplevel / DialogTk
│   ├── error_dialog.py # 错误捕捉对话框
│   └── error_catcher.py # @catch 装饰器
├── setting/           # 默认 JSON 设置（global.json, auto.*.json）
├── language/          # i18n JSON 文件
├── asset/             # 图片/图标
└── main.py            # 入口点（AboutCanvas, ControlCanvas, Main）
```

顶层文件：

- `setup.py` – 包配置（从 `HDpip` 模块导入版本号）
- `dist.py` – 构建脚本，清理目录并运行 `python setup.py sdist`
- `local_install.py` – 开发安装脚本（清除缓存、卸载旧版本、从 `dist/` 安装）
- `pipgui.py` – 独立的 PyQt6 GUI（不是 HDpip 包的一部分）
- `dev` – 空文件，启用开发模式（`HDpip.core.system.isDev()`）

**注意：** 包 README (`HDpip/README.md`) 用于 PyPI 分发，与仓库级别的 README 是分开的。

## 开发命令

| 用途 | 命令 |
| ---- | ---- |
| 运行主 GUI（开发） | `python -m HDpip.main` |
| 运行主 GUI（安装后） | `HDpip` 或 `hdpip` |
| 运行独立的 PyQt6 GUI | `python pipgui.py` |
| 构建分发压缩包 | `python dist.py` |
| 本地安装测试 | `python local_install.py` |
| 检查 Python/pip 版本 | `python -c "from HDpip.core.system import getPythonVersion, getPipVersion; print(getPythonVersion(), getPipVersion())"` |
| 列出已安装包 | `python -c "import HDpip.core.pip_api; print(HDpip.core.pip_api.list_())"` |
| 打开包目录 | `python -c "from HDpip.core.system import openInExplorer; openInExplorer('HDpip')"` |
| 运行测试 | `python -m pytest`（仅在用户明确要求时运行） |

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

**版本单一来源：`HDpip/__init__.py` 中的 `version` 变量。** 升版本只改这一处：

1. `pyproject.toml` 用 `dynamic = ["version"]` + `[tool.setuptools.dynamic]` 从 `HDpip.version` 自动读取（无 `setup.py`）。
2. `dist.py` 清理构建目录并运行 `python -m build` / `setup.py sdist`。
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
- **`@override` / `@overload`** — 覆写父类方法用 `@override`，多形态输入用 `@overload`；从 `typing_extensions` 导入（Python 3.10 的 `typing` 没有 `override`）
- **参数列表** — 每个参数末尾加逗号（包括最后一个），`self` 后也加
- **`super().__init__`** — 单行传全部参数，不换行
- **不写 `**kwargs`** — 显式列出所有参数，不用通配
- **相对导入** — 必须 `try/except ImportError` 包裹，fallback 用 `sys.path` 追加 + 绝对导入

- **`widget.set(str)`** — maliang 控件改文本统一用 `widget.set()`
- **Canvas 子画布** — 方法顺序严格：`renderLanguage` → `onLanguageChange` → `destroy` → `__init__`
- **语言事件** — `data_manager.language.registerEvent(self.onLanguageChange)` 注册，`destroy` 中 `unregisterEvent`

`.clinerules/role.md` 包含额外的项目特定指导。

## 测试

正式测试套件在 `tests/`，使用 pytest（pyproject.toml 已配置）。运行：

```bash
python -m pytest
```

测试文件按职责拆分：`test_version.py`（Version）、`test_data.py`（Data）、`test_utils.py`（工具函数）、`test_gui_base.py`（DPI/缩放）、`test_pip_api.py`（pip API）、`test_buttons.py`、`test_dialog.py`、`test_error.py`、`test_treeview.py`（TkTable）。共享 fixture（Tk 窗口）在 `conftest.py`。

## 架构亮点

### 数据管理

- `HDpip.core.data.Data` – JSON 文件包装器，带有事件系统。支持元组嵌套键访问 `d["a", 0]`。
- `HDpip.core.data.DataManager` – 管理用户设置和语言文件。`init()` 首次运行时创建默认配置。

### 版本处理

- `HDpip.core.util.Version` – 继承 pip 的 Version，支持 PEP 440。`isCloseTo()` 约等于，`multipleCompare()` 多重富比较。

### Pip 集成

- `HDpip.core.pip_api` – 包装 `pip list`、`pip show`、`pip install`、`pip uninstall`。`pip_head` 为全局执行头。

### GUI 框架

- 基于 **maliang**（tkinter 基础）。`gui.base` 提供 Bootstrap 风格 `Button`（`theme` 参数）、`ScrolledText`、`RoundedRectangle`、`WindowFadeIn`/`WindowFadeOut`。
- **表格控件**：直接用 `maliang.table.TkTable`（tksheet），不封装。`headers()`/`insert_row()`/`set_column_widths()`/`get_selected_rows()` 等原生 API。
- **智能缩放**：`smartScale(value)` / `ss(value)` 按屏幕分辨率缩放 pos/size/fontsize/height/width。
- 欢迎流程（`gui.welcome.Welcome`）在首次启动或未接受许可证时运行。

### 国际化

- 语言文件是 JSON 字典，存储在 `HDpip/language/`（默认）和 `$PYTHONPATH/HDpip/language/`（自定义）中。`language_code_dict` 将区域代码映射到显示名称。

### 仅开发行为

- 当 `dev` 文件存在时，`HDpip.core.system.isDev()` 返回 `True`。可用于启用调试功能或备用路径。

### 类型存根生成

- `HDpip.core.pyi` 包含从 Python 源代码生成 `.pyi` 类型存根文件的工具。内部用于开发。

## CHANGELOG 约定

- **倒序**：最新版本条目在最上方。
- 版本标题（`## 🔖 \`0.0.5.post1\``）必须与 `HDpip/__init__.py` 的 `version` **完全一致**（含 post 后缀）。
- 条目结构：发布日期 → 提示块 → 7 色分类（🟢Added / 🔴Removed / 🟡Changed / 🔵Optimized / 🟣Fixed / 🟠Deprecated / 🟤Refactored），每条英文 + 中文对照。
- `.github/workflows/sync-changelog.yml` 在 release `published`（正式/预览版发布）后自动把对应条目写入 release body；draft 阶段需手动 `workflow_dispatch`。

## 注意事项

- PyQt6 GUI (`pipgui.py`) 是独立工具，**不**构建到 HDpip 包中。
- `HDpip.core.util.HDpipError` 用于内部错误；`unfinished()` 为未实现功能抛错。
- `core/base.py` 已删除，`_BaseProxy` 兼容代理也已移除，直接从 `core.util` / `core.system` / `core.data` 导入。
- 表格控件直接使用 `maliang.table.TkTable`（tksheet），不使用 ttk.Treeview。
- 所有 UI 尺寸（pos/size/fontsize/height/width）必须用 `ss()` 缩放，在 `gui.base` 中已定义 `ss = smartScale`。
- 分隔线用 `create_line` 画在对应子 canvas 上（被 widget 遮挡的部分画在子 canvas 自身，无遮挡的留在父 canvas）。
- **不要在没有明确要求时运行 pytest。**
- 镜像源定义在 `HDpip/setting/auto.*.json` 中，运行时可选。
- 项目使用 GPL-3.0 许可证。
