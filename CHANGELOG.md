# Changelog / 更新日志

> [!TIP]  
> This changelog has the following 7 types of updates, each of which is represented by 7 different colors  
> 此更新日志有以下 7 种类型的更新内容，分别用 7 种不同颜色来表示
>
> - 🟢 **Added / 新增**
> - 🔴 **Removed / 移除**
> - 🟡 **Changed / 变更**
> - 🔵 **Optimized / 优化**
> - 🟣 **Fixed / 修复**
> - 🟠 **Deprecated / 弃用**
> - 🟤 **Refactored / 重构**

## 🔖 `0.0.6.post1`

🕓 *Release Date / 发布日期 : 2026-9-7*

🟣 **Fixed / 修复**

- Make `main.py` runnable as a bare script without relying on the installed `HDpip` distribution (all fallback imports now point to the local modules); this also fixes the EndCanvas relaunch and the error-dialog startup.

- 修复直接以脚本方式运行 `main.py` 依赖已安装 `HDpip` 包的问题（兜底导入现指向本地模块），同步修复欢迎页结束后的进程重启与错误对话框启动。

- Fix the error dialog that referenced the removed `gui/base.py` module.

- 修复错误对话框引用已删除的 `gui/base.py` 模块的问题。

- Fix duplicated top-level `core` and `HDpip.core` module loading inside `gui/custom/containers.py`.

- 修复 `gui/custom/containers.py` 中顶层 `core` 与 `HDpip.core` 两份模块同时加载的问题。

- Restore language-change notifications for canvases created earlier, which were lost whenever a later container rebuilt the `language` data object.

- 修复后创建的容器重建 `language` 数据对象导致先前画布收不到语言变更事件的问题。

🟤 **Refactored / 重构**

- Move package metadata (`version` / `author` / `copyright`) out of `HDpip/__init__.py` into the dedicated `HDpip/info.py` module.

- 将包元数据（`version` / `author` / `copyright`）从 `HDpip/__init__.py` 抽离至独立的 `HDpip/info.py` 模块。

- All canvases and windows now share one `core.data.data_manager` instance by default, and `DataManager.init()` no longer rebuilds in-memory data on re-entry.

- 所有画布与窗口默认共用同一个 `core.data.data_manager` 实例，且 `DataManager.init()` 重复调用不再重建内存数据。

---

## 🔖 `0.0.6`

🕓 *Release Date / 发布日期 : 2026-8-24*

> [!CAUTION]  
> `HDpip/gui` has been **fully restructured** into the `gui/custom` subpackage, please pay attention to the changes in function calls.  
> 我们已对 `HDpip/gui` 进行了**全面重构**，拆分为 `gui/custom` 子包，请注意调用变动。  
> `HDpip/gui/custom/utility` has been **renamed** to `HDpip/gui/custom/util`, the old import is **no longer available**.  
> `HDpip/gui/custom/utility` 已**重命名**为 `HDpip/gui/custom/util`，旧引用**已不可用**。  

---

🟢 **Added / 新增**

- Add the abstract container classes `Tk` / `Toplevel` / `Canvas` under `gui/custom/containers`.

- 新增 `gui/custom/containers` 抽象容器类（`Tk` / `Toplevel` / `Canvas`）。

- Add the `enableTempTk` decorator in `core/util.py`.

- 新增 `core/util.py` 中的 `enableTempTk` 装饰器。

🟤 **Refactored / 重构**

- Split `gui/base.py` into the `gui/custom` subpackage with the `color` / `util` / `widgets` / `texts` / `animations` / `shapes` / `media` / `containers` modules.

- 将 `gui/base.py` 拆分为 `gui/custom` 子包，包含 `color`、`util`、`widgets`、`texts`、`animations`、`shapes`、`media`、`containers` 模块。

- All canvases and windows in `welcome.py` / `main.py` now inherit from the `gui/custom/containers` classes, unifying language events and window customization.

- `welcome.py` 与 `main.py` 的所有画布与窗口全面继承 `gui/custom/containers` 容器类，统一语言事件与窗口定制。

- Integrate `Button` and `IconButton` with icon placement, theme coloring and disabled variants.

- 整合 `Button` 与 `IconButton`，支持图标放置、主题着色与禁用变体。

- Remove all `:param self:` annotations from docstrings.

- 清理了所有文档字符串中的 `:param self:` 注释。

🟡 **Changed / 变更**

- Rename `gui/custom/utility.py` to `util.py` and unify all text files to CRLF line endings.

- 将 `gui/custom/utility.py` 重命名为 `util.py`，并统一所有文本文件为 CRLF 行尾。

🟣 **Fixed / 修复**

- Fix the container icon loading timing and the button icon color after disabling.

- 修复容器图标加载时序与按钮禁用后图标颜色。

- Fix the undefined `_Wrapped` type annotation in `gui/error_catcher.py`.

- 修复 `gui/error_catcher.py` 中未定义的 `_Wrapped` 类型注解。

## 🔖 `0.0.5.post1`

🕓 *Release Date / 发布日期 : 2026-8-7*

🟢 **Added / 新增**

- Add `darkdetect` as an explicit dependency.

- 将 `darkdetect` 添加为显式依赖。

🟡 **Changed / 变更**

- Read the package version dynamically from `HDpip.version` in `pyproject.toml`, keeping a single source of truth.

- `pyproject.toml` 中的版本号改为从 `HDpip.version` 动态读取，保持单一版本来源。

## 🔖 `0.0.5`

🕓 *Release Date / 发布日期 : 2026-8-7*

> [!IMPORTANT]  
> We will **refactor** `HDpip/gui` in the next version, please pay attention to the changes in function calls.  
> 我们将在下一个版本**全面重构**`HDpip/gui`，请注意调用变动。  

---

> [!CAUTION]  
> We have **completely refactored** `HDpip/base.py`, and the call to `HDpip.base` is **no longer available**, please import from `HDpip.core.util`, `HDpip.core.system`, and `HDpip.core.data` instead.  
> 我们对`HDpip/base.py`进行了**全面重构**，`HDpip.base`的调用**已不可用**，请改为从`HDpip.core.util`、`HDpip.core.system`、`HDpip.core.data`中导入。  

---

🟢 **Added / 新增**

- Add the documentation site: <https://handongliren.github.io/HDpip/>

- 新增了文档站：<https://handongliren.github.io/HDpip/>

- Add smart scale function, which can automatically scale the size of the interface according to the screen resolution.

- 新增了智能缩放功能，可以根据屏幕分辨率自动缩放界面大小。

- Add the formal pytest test suite and `@override` / `@overload` decorators across the codebase.

- 新增了正式的 pytest 测试套件，并在全项目使用 `@override` / `@overload` 装饰器。

🟤 **Refactored / 重构**

- Split `core/base.py` into `core/util.py`, `core/system.py` and `core/data.py`, and remove the `_BaseProxy` compatibility layer.

- 将 `core/base.py` 拆分为 `core/util.py`、`core/system.py` 和 `core/data.py` 三个模块，并移除了 `_BaseProxy` 兼容代理。

- Switch the table widget from the self-wrapped `Treeview` to `maliang.table.TkTable` (tksheet).

- 表格控件由自封装的 `Treeview` 切换为 `maliang.table.TkTable`（tksheet）。

🟡 **Changed / 变更**

- Apply `smartScale` (`ss`) to all UI dimensions across all interfaces, and update module attribution of `shell` / `Version`.

- 在所有界面全面运用 `smartScale`（`ss`）缩放，并调整了 `shell` / `Version` 的模块归属。

🔵 **Optimized / 优化**

- Clean trailing whitespace and consecutive blank lines across the repository.

- 清理了全仓库的行尾空格和连续空行。

🟣 **Fixed / 修复**

- Fix the DPI test failure caused by the module-level cache bypassing `monkeypatch`, and a pre-existing `SyntaxError` in `gui/base.py`.

- 修复了 DPI 测试因模块级缓存绕过 `monkeypatch` 而失败的问题，以及 `gui/base.py` 中预存的语法错误。
