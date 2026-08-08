---
name: version-before-import
description: HDpip/__init__.py 的 version 必须定义在 import core/gui 之前（顺序敏感）
metadata:
  type: project
---

`HDpip/__init__.py` 的导入顺序是**刻意的**：`version` 变量必须先定义，之后才是 `from . import core, gui`。

**Why:** `core/system.py` 有 `from .. import version`（导入顶层 HDpip 包）。如果 `version` 定义在 `from . import core, gui` 之后，导入链 `HDpip/__init__ → core → system → HDpip(部分初始化)` 会抛 `ImportError: cannot import name 'version' from partially initialized module`。当前顺序让 `system` 能取到已定义的 `version` 属性。

**How to apply:** 重构 `HDpip/__init__.py` 时保持 `version = "..."` 在 import 语句之前。`HDpip` 包内无真正的循环导入（core 不依赖 gui，custom 单向依赖），但此点是唯一"顺序敏感"设计，不要"优化"掉。
