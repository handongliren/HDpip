---
name: changelog-conventions
description: CHANGELOG.md 格式约定与 release 同步 workflow 的行为
metadata:
  type: project
---

`CHANGELOG.md` 格式约定：

- **倒序**：最新版本条目在最上面
- 版本标题：`## 🔖 \`0.0.5.post1\`` —— 必须与 `HDpip/__init__.py` 的 `version` **完全一致**（含 post 后缀）
- 条目结构：发布日期行 → 提示块（IMPORTANT/CAUTION）→ 7 色分类（🟢Added / 🔴Removed / 🟡Changed / 🔵Optimized / 🟣Fixed / 🟠Deprecated / 🟤Refactored），每条英文+中文对照
- 分类间用 `---` 分隔，版本条目间也用 `---` 分隔

`.github/workflows/sync-changelog.yml`：

- 触发：`release: types: [published]`（正式版和预览版发布都触发；draft 创建不触发是 GitHub 平台限制，需要手动 `workflow_dispatch`）
- awk 提取正则支持 post 版本：`[0-9]+\.[0-9]+\.[0-9]+(\.post[0-9]+)?`（不带这个后缀会把 `0.0.5.post1` 截断成 `0.0.5` 导致找不到条目）

**Why:** 用户要求版本条目与代码版本严格对齐，且 workflow 提取依赖标题格式。

**How to apply:** 写 CHANGELOG 时用当前 `HDpip/__init__.py` 的版本号作为标题，新条目插到最上方，保持中英双语和 7 色分类。
