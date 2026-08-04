---
name: core-modules
description: core/base.py 已拆分到 util.py / system.py / data.py，兼容代理已移除
metadata:
  type: project
---

`HDpip/core/base.py` 已从 git 历史中完全删除。内容拆分为：

- **`util.py`** — HDpipError, unfinished, Version, multipleSpilt
- **`system.py`** — shellDecode, shell, getBaseDir, getPythonPath, Version(import), getPythonVersion, getPipVersion, getVersion, getSystemVersion, openInExplorer, isDev
- **`data.py`** — Data, DataManager, isBelongedToHDpip

`core/__init__.py` 只做简单导出：`from . import data, pip_api, system, util`。`_BaseProxy` 兼容代理和 `sys.modules["HDpip.core.base"]` 注入已移除，`import HDpip.core.base` 会报 ModuleNotFoundError。

**Why:** 原 base.py 过于臃肿，按职责拆分。过渡期用 _BaseProxy 保证零改动，现已收尾移除，代码全部直接引用具体子模块。

**How to apply:** 从具体子模块导入：`from HDpip.core.util import Version`、`from HDpip.core.data import Data, DataManager`、`from HDpip.core.system import shell, getBaseDir`。不要使用 `core.base.X`。
