---
name: version-single-source
description: 版本号唯一来源是 HDpip/__init__.py 的 version 变量
metadata:
  type: project
---

版本号唯一来源：`HDpip/__init__.py` 中的 `version = "0.0.5.post1"`。

- `pyproject.toml` 用 `dynamic = ["version"]` + `[tool.setuptools.dynamic] version = {attr = "HDpip.version"}` 自动读取
- 原 `setup.py` 已不存在，构建完全走 pyproject.toml
- 升版本只改 `HDpip/__init__.py` 一处，sdist / PyPI 元数据自动同步

**Why:** 之前 pyproject.toml 硬编码 0.0.4 与包内 0.0.5.post1 双源不同步。

**How to apply:** 发布新版本时只改 `HDpip/__init__.py` 的 `version`，并同步更新 CHANGELOG（见 [[changelog-conventions]]）。
