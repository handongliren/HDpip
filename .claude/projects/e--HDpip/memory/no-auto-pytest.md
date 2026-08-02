---
name: no-auto-pytest
description: 没有明确要求时不要运行 pytest
metadata:
  type: feedback
---

每次修改代码后，除非用户明确要求运行 pytest，否则不要自动运行测试。

**Why:** 用户希望控制测试时机，避免每次编辑都触发测试。仅当用户说了"跑测试"/"pytest"/"验证"等明确指令时才执行。

**How to apply:** 修改代码后直接提交/汇报结果，不附加 `python -m pytest`。
