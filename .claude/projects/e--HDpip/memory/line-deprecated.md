---
name: line-deprecated
description: gui.base.Line 准备废弃，分隔线用 create_line
metadata:
  type: project
---

`gui.base.Line` widget 准备废弃，分隔线改用 `create_line`。

**Why:** Line 作为 virtual widget 有 z-order 问题（虚拟 widget 永远在 embedded widget 下方），`create_line` 直接画在对应 canvas 上更简单可靠。

**How to apply:** 被 widget 遮挡的分隔线画在子 canvas 自身（内部坐标系），无遮挡的留在父 canvas。不要用 `gui.base.Line`。
