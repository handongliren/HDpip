---
name: core-modules
description: core/base.py 已拆分到 util.py / system.py / data.py，_BaseProxy 兼容旧引用
metadata:
  type: project
---

`HDpip/core/base.py` 已从 git 历史中完全删除。内容拆分为：

- **`util.py`** — HDpipError, unfinished, Version, multipleSpilt
- **`system.py`** — shellDecode, shell, getBaseDir, getPythonPath, Version(import), getPythonVersion, getPipVersion, getVersion, getSystemVersion, openInExplorer, isDev
- **`data.py`** — Data, DataManager, isBelongedToHDpip

兼容方案：`core/__init__.py` 中的 `_BaseProxy` 类透明代理 `core.base.X` → util/system/data，并注入 `sys.modules["HDpip.core.base"]` 使 `import HDpip.core.base` 仍然有效。

**Why:** 原 base.py 过于臃肿，按职责拆分。_BaseProxy 保证外部代码零改动。

**How to apply:** 新代码应直接从子模块导入：`from HDpip.core.util import Version`、`from HDpip.core.data import Data, DataManager` 等，而非继续使用 `core.base.X`。
