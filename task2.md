# 任务：移除 try/except ImportError，改用 __package__ 修复，统一直接跑 .py

## 背景

HDpip 项目每个文件顶部都有：

```python
try:
    from .. import core
except ImportError:
    sys.path.append(str(base_dir))
    import core
```

问题：fallback 创建的模块身份和成功路径不同（`core` vs `HDpip.core`），`DataManager` 会变成两个单例，设置和语言状态不同步。`sys.path.append` 加在末尾，还可能命中同名第三方模块。

不用 `-m`，不用 Scripts 入口，全部改成就直接 `python xxx.py` 跑，靠 `__package__` 修复让相对导入正常工作。

## 统一修复块

每个需要直接跑的文件，顶部、所有 import 之前插入：

```python
if __name__ == "__main__" and __package__ is None:
    import sys
    import pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[N]))
    __package__ = "包名"
```

`N` 和 `包名`：

| 文件 | `parents[N]` | `__package__` |
|---|---|---|
| `HDpip/main.py` | `parents[1]` | `"HDpip"` |
| `HDpip/gui/upgrade.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/welcome.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/main.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/error_dialog.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/dialog.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/error_catcher.py` | `parents[2]` | `"HDpip.gui"` |
| `HDpip/gui/custom/containers.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/widgets.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/media.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/util.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/shapes.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/texts.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/gui/custom/animations.py` | `parents[3]` | `"HDpip.gui.custom"` |
| `HDpip/core/data.py` | `parents[2]` | `"HDpip.core"` |
| `HDpip/core/pip_api.py` | `parents[2]` | `"HDpip.core"` |
| `HDpip/core/system.py` | `parents[2]` | `"HDpip.core"` |
| `HDpip/core/util.py` | `parents[2]` | `"HDpip.core"` |
| `HDpip/core/pyi.py` | `parents[2]` | `"HDpip.core"` |

然后删掉所有 `try/except ImportError`，导入只写一套：

```python
from .. import core

from . import custom
from .custom.util import ss
from .custom.media import bi
```

`base_dir` 保留，放在修复块之后、包内导入之前。

## 为什么直接跑 .py 能正确

以 `python Python310/HDpip/copy/HDpip/gui/upgrade.py` 为例：

- `__file__` 是 `.../copy/HDpip/gui/upgrade.py`
- `parents[2]` 是 `.../copy`
- `sys.path.insert(0, ".../copy")`
- `__package__ = "HDpip.gui"`
- `from .. import core` 解析为 `HDpip.core`，`import HDpip` 命中 `.../copy/HDpip/`，不是 `site-packages`

以 `python site-packages/HDpip/main.py` 为例：

- `parents[1]` 是 `site-packages`
- `sys.path.insert(0, "site-packages")`
- `__package__ = "HDpip"`
- `from . import core` 命中 `site-packages/HDpip/core`

路径自洽，不需要 `-m`，不需要 `PYTHONPATH`，不需要 Scripts 入口。

## 具体文件改法

### 1. `HDpip/main.py`

顶部：

```python
from typing import *

import pathlib

if __name__ == "__main__" and __package__ is None:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    __package__ = "HDpip"

import maliang.theme
import maliang.core.configs

from . import core
from . import gui
```

删掉 `try/except ImportError`。`if __name__ == "__main__"` 块改成直接调 `main()`，不启动子进程：

```python
if __name__ == "__main__":
    main()
```

### 2. `HDpip/gui/welcome.py`

顶部：

```python
from typing import *
from typing_extensions import override

import pathlib

if __name__ == "__main__" and __package__ is None:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    __package__ = "HDpip.gui"

import difflib
import locale
import tkinter.filedialog
import json

import maliang
import maliang.core.configs
import maliang.theme
import maliang.animation
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

from .. import core

from . import custom
from .custom.util import ss
from .custom.media import bi
```

`EndCanvas.command` 里的重启，保持直接跑 `main.py`：

```python
subprocess.Popen(
    [sys.executable, str(base_dir / "main.py")],
    stdin = subprocess.DEVNULL,
    stdout = subprocess.DEVNULL,
    stderr = subprocess.DEVNULL,
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
)
```

`base_dir` 是 `HDpip/`，`base_dir / "main.py"` 是 `HDpip/main.py`，直接跑带 `__package__` 修复，正确。

### 3. `HDpip/gui/upgrade.py`

顶部：

```python
from typing import *
from typing_extensions import override

import pathlib

if __name__ == "__main__" and __package__ is None:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    __package__ = "HDpip.gui"

import queue
import threading

import maliang.core.configs
import maliang.core.virtual

base_dir = pathlib.Path(__file__).parents[1].resolve()

from .. import core

from . import custom
from .custom.util import ss
from .custom.media import bi
```

copy 进程启动：

```python
copy_main = copy_dir / "HDpip" / "gui" / "upgrade.py"
subprocess.Popen(
    [sys.executable, str(copy_main), "--updater"] + (["--silent"] if silent else []),
    cwd = tempfile.gettempdir(),
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    close_fds = True,
)
os._exit(0)
```

`copy_main` 是 `Python310/HDpip/copy/HDpip/gui/upgrade.py`，`parents[2]` 是 `Python310/HDpip/copy`，`sys.path.insert(0, copy)`，`import HDpip` 命中 copy 里的包。`cwd` 设 `%TEMP%`，不锁 copy 目录。

新主体启动：

```python
site_main = site_packages / "HDpip" / "main.py"
subprocess.Popen(
    [sys.executable, str(site_main)],
    cwd = tempfile.gettempdir(),
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    close_fds = True,
)
```

`site_main` 是 `site-packages/HDpip/main.py`，`parents[1]` 是 `site-packages`，`import HDpip` 命中新版。`cwd` 设 `%TEMP%`。

### 4. `HDpip/gui/main.py`、`HDpip/gui/error_dialog.py`、`HDpip/gui/dialog.py`、`HDpip/gui/error_catcher.py`

`parents[2]`，`__package__ = "HDpip.gui"`。删 `try/except`。

`gui/main.py` 底部的 `if __name__ == "__main__"` 块，保持直接跑 `main.py`，或者删掉（因为正常入口是 `HDpip/main.py`）。

### 5. `HDpip/gui/custom/*.py`

`parents[3]`，`__package__ = "HDpip.gui.custom"`。原本的 `from ... import core`（三个点）保持不变，因为 `__package__` 是 `HDpip.gui.custom`，`...` 指向 `HDpip`。删 `try/except`。

### 6. `HDpip/core/*.py`

`parents[2]`，`__package__ = "HDpip.core"`。原本的 `from . import system`、`from . import util` 不变。删掉 `except ImportError: import system` 那套。

## 约束

- 不修改任何类的公开方法签名。
- 不修改 `try/except` 以外的逻辑。
- 保持现有空行风格。
- `__package__` 修复块放在标准库导入之后、第三方导入之前，`pathlib` 和 `sys` 在修复块内单独 import。
- `parents[N]` 严格按上表，不要凭感觉写。
- 如果某个文件原本没有 `try/except ImportError`，跳过，不要加修复块。
- 如果某个文件原本的 `base_dir` 在 `try` 块之前，保留 `base_dir`，放在修复块之后、包内导入之前。
- 不引入 `-m`，不引入 Scripts 入口，所有启动都是 `[sys.executable, str(某个.py)]`。

## 输出

1. 列出所有需要修改的文件路径。
2. 每个文件给出 `__package__` 修复块 + 删掉 `try/except` 后的导入区（只给这一段）。
3. 给出 `welcome.py` 的 `EndCanvas.command`、`upgrade.py` 里 copy 进程和新主体启动命令的修改前后对比。
4. 给出验证命令：
   - `python HDpip/main.py`
   - `python HDpip/gui/welcome.py`
   - `python HDpip/gui/upgrade.py`
   - `python -c "import HDpip; import HDpip.gui.welcome; import HDpip.gui.upgrade; print('ok')"`
   - 在 copy 目录下：`python Python310/HDpip/copy/HDpip/gui/upgrade.py --updater`