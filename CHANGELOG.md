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

## 🔖 `0.0.5`

🕓 *Release Date / 发布日期 : 2026-8-6*

> [!IMPORTANT]  
> We will **refactor** `HDpip/gui` in the next version, please pay attention to the changes in function calls.  
> 我们将在下一个版本**全面重构**`HDpip/gui`，请注意调用变动。  

> [!CAUTION]  
> We have **completely refactored** `HDpip/base.py`, and the call to `HDpip.base` is **no longer available**, please import from `HDpip.core.util`, `HDpip.core.system`, and `HDpip.core.data` instead.  
> 我们对`HDpip/base.py`进行了**全面重构**，`HDpip.base`的调用**已不可用**，请改为从`HDpip.core.util`、`HDpip.core.system`、`HDpip.core.data`中导入。  

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
