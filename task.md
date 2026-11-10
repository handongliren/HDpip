# HDpip 自更新补完任务 Prompt

## 背景

项目是 HDpip，一个基于 maliang 的 pip GUI。当前 `gui/upgrade.py` 只有检测更新和安装画布，`main.py` 有正常 GUI 入口，`core/data.py` 有 `Data`、`Cache`、`DataManager`。

现在要实现完整的自更新流程，核心约束是：**主进程必须 `os._exit(0)` 释放 `site-packages/HDpip` 的文件锁，更新由复制到包外的 copy 进程执行。**

## 目录约定

```
site-packages/HDpip/                    ← 被更新的包，主进程从这里运行
Python310/HDpip/                        ← 用户数据目录，已有 setting.json、language/
Python310/HDpip/copy/                   ← 更新副本目录
Python310/HDpip/copy/HDpip/             ← 副本的包内容，结构同 site-packages/HDpip
Python310/HDpip/copy/state.json         ← 更新状态
```

`state.json` 字段：

```json
{
  "from_version": "0.0.7",
  "to_version": "0.0.8",
  "attempts": 0
}
```

`from_version` 是复制时 `site-packages/HDpip` 的版本，`to_version` 是目标版本，`attempts` 是失败重试次数。

## 三个 mode 的语义

| mode | 检测到新版本后 | 用户交互 | 进度窗口 |
|---|---|---|---|
| `notify` | 复制到 copy，弹 `ConfirmCanvas` | 安装 / 下次再说 / 一周内不再提醒 / 取消 | 选“安装”后由 copy 进程显示 |
| `notify&install` | 复制到 copy，弹通知框告知后自动继续 | 无（或仅“知道了”） | 由 copy 进程显示 |
| `silent` | 复制到 copy，不弹框 | 无 | 不显示 |

### `notify` 的按钮语义

- **安装**：启动 copy 进程，主进程 `os._exit(0)`。
- **下次再说**：`setting["upgrade"]["last_check"] = now`，`setting.save()`，关闭窗口，正常启动 GUI。
- **一周内不再提醒**：`last_check = now + 7 * 86400`，`setting.save()`，关闭窗口，正常启动 GUI。
- **取消**：不改变 `last_check`，关闭窗口，正常启动 GUI。下次启动可能再次弹窗。

## 需要实现的内容

### 1. `gui/upgrade.py`

- `ConfirmCanvas` 的四个按钮绑定回调：
  - `confirm_button` → 启动 copy 进程更新
  - `delay_next_button` → `last_check = now`
  - `delay_week_button` → `last_check = now + 7 * 86400`
  - `note_button` → 不改 `last_check`
- 新增 `copy_to_target()`：把 `site-packages/HDpip` 复制到 `Python310/HDpip/copy/HDpip/`，忽略 `__pycache__` 和 `.pyc`，写 `state.json`。如果 copy 已存在且 `from_version` 等于当前版本、`to_version` 等于目标版本，跳过复制。
- 新增 `launch_updater(silent: bool)`：
  ```python
  subprocess.Popen(
      [sys.executable, str(copy_dir / "HDpip" / "main.py"), "--updater"] + (["--silent"] if silent else []),
      cwd=tempfile.gettempdir(),
      creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
      close_fds=True,
  )
  os._exit(0)
  ```
- 新增 `check_and_update(data_manager)`：统一入口。
  1. 读 `setting["upgrade"]`，判断 `now - last_check < interval` 则跳过。
  2. 检测 `latest`，失败则正常启动，**不**更新 `last_check`。
  3. 检测成功写 `last_check = now`，`setting.save()`。
  4. 如果 `latest <= current`，正常启动。
  5. 按 mode 分发：
     - `notify`：复制到 copy，弹 `ConfirmCanvas`。
     - `notify&install`：复制到 copy，弹通知框，短暂延时后自动 `launch_updater(False)`。
     - `silent`：复制到 copy，直接 `launch_updater(True)`。
- 新增 `cleanup_copy()`：启动时调用。读 `state.json`：
  - `current >= to_version` → 删 copy。
  - `current != from_version` → 删 copy（copy 已过期）。
  - `state.json` 读失败或字段缺失 → 删 copy。
  - 删 copy 失败时重试 10 次，每次间隔 500ms。

### 2. `main.py`（入口文件）

- 顶部加 `sys.path` 修复：从 copy 目录启动时，`sys.path.insert(0, copy_parent)`，`__package__ = "HDpip"`。
- 检测 `--updater` 参数：
  - 有 `--silent`：不加载 GUI，直接
    ```python
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", f"hdpip=={to_version}"])
    ```
    成功后 `subprocess.Popen([sys.executable, "-m", "HDpip"])`，失败写日志并递增 `attempts`。
  - 无 `--silent`：加载 `InstallCanvas`，pip 输出通过 queue 实时显示，成功后启动新主体。
- 正常启动时调用 `cleanup_copy()`，然后走现有 `needWelcome` 逻辑。

### 3. `DataManager.init()`

- 新增 `self.custom_cache` 路径和 `Cache` 实例，注册兜底刷新规则：
  ```python
  self.cache.registerRefresh(None, lambda pkg: str(pip_api.getLatestVersion(pkg)), ttl=6 * 3600)
  ```
- `setting["upgrade"]` 增加 `last_check` 字段，默认 `0`。

### 4. 失败重试

- copy 进程 pip 失败时递增 `state.json` 的 `attempts`。
- `attempts >= 3` 时，`silent` 和 `notify&install` 降级为 `notify`，只弹一次通知，不再自动安装。
- 日志写到 `Python310/HDpip/copy/error.log`，便于诊断。

## 关键约束

- 主进程在启动 copy 进程后必须 `os._exit(0)`，不能用 `sys.exit()`。
- copy 进程的 `cwd` 必须是 `%TEMP%` 或 `Python310/HDpip/`，不能是 `site-packages/HDpip`。
- pip 命令用 `sys.executable -m pip install --upgrade hdpip=={to_version}`，锁定版本。
- 新主体启动用 `sys.executable -m HDpip`，不要直接跑 `main.py`。
- 删 copy 失败时重试 10 次，每次间隔 500ms，仍失败留到下次启动。
- `last_check` 只在检测成功后更新，失败不更新。
- 所有新增函数和类补 Sphinx 风格 docstring，包含 `:param:`、`:type:`、`:return:`、`:rtype:`、`:raises:`。
- 不修改 `Data`、`Cache`、`DataManager` 的现有公开方法签名，只新增。
- 保持现有空行风格：顶层定义之间一个空行，方法之间一个空行，docstring 与代码之间一个空行。

## 输出要求

1. 给出修改后的 `gui/upgrade.py` 完整代码。
2. 给出修改后的 `main.py` 完整代码。
3. 给出 `DataManager.init()` 的 diff 或完整 `data.py` 相关片段。
4. 列出所有新增的语言键（如 `upgrade.install_success`、`upgrade.error`、`upgrade.checking`），并说明加在 `language/*.json` 的哪个位置。
5. 给出一个测试步骤清单，覆盖三个 mode 的成功路径和失败路径，包括：
   - `notify` 选安装、选延期、选取消。
   - `notify&install` 自动安装成功。
   - `silent` 自动安装成功。
   - pip 失败后的重试和降级。
   - 更新成功后 copy 被删除。
   - 更新期间主进程文件锁被释放（用 `handle.exe` 或 `Process Explorer` 验证 `site-packages/HDpip` 无句柄）。