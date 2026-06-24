"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

本文件是错误捕捉对话框。
"""

import sys
import argparse
import locale
import difflib
import pathlib
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import maliang.core.configs
try:
    from .. import core
except ImportError:
    base_dir = pathlib.Path(__file__).parents[1].resolve()
    sys.path.append(str(base_dir))
    import core

try:
    from . import dialog
except ImportError:
    import dialog


language_dict = {
    "zh-CN": {
        "title": "错误捕捉",
        "ok": "确认",
        "copy": "复制",
        "export": "导出",
        "placeholder": "没有错误，你好啊！",
        "export_title": "导出错误为日志文件",
        "log_file": "日志文件",
        "all_files": "所有文件",
        "warning": "警告",
        "export_reject": "禁止将任何文件保存在HDpip的目录中！"
    },
    "en": {
        "title": "Error Catcher",
        "ok": "OK",
        "copy": "Copy",
        "export": "Export",
        "placeholder": "There isn't any error. Hi!",
        "export_title": "Export Error as a Log File",
        "log_file": "Log file",
        "all_files": "All files",
        "warning": "Warning",
        "export_reject": "You mustn't save any file in HDpip's directory!"
    }
}
local_language = locale.getdefaultlocale()[0]
possible_language = difflib.get_close_matches(local_language, ["zh-CN", "en"], n = 1) or ["en"]
language = language_dict[possible_language[0]]
# Parse command-line arguments. Support:
#   --text "error text"
#   --auto-close N
# or legacy single positional argument (error text).
parser = argparse.ArgumentParser(add_help = False)
parser.add_argument("--text", "-t", dest = "text", help = "Error text", default = language["placeholder"])
parser.add_argument("--auto-close", dest = "auto_close", type = int, help = "Auto close", default = -1)
# allow legacy single positional argument as text
parser.add_argument("positional", nargs = "?", help = argparse.SUPPRESS)
ns, _ = parser.parse_known_args()

error = ns.text if ns.text is not None else (ns.positional or language["placeholder"])
auto_close = ns.auto_close or -1

maliang.core.configs.Env.system = "Windows11"

def copyCommand(*argvs, **kargvs) -> None:
    root.dialog_canvas.scrolled_text.clipboard_clear()
    root.dialog_canvas.scrolled_text.clipboard_append(error)

def exportCommand(*argvs, **kargvs) -> None:
    file = pathlib.Path(tkinter.filedialog.asksaveasfilename(
        filetypes = [(language["log_file"], ".log"), (language["all_files"], ".*")],
        title = language["export_title"],
        initialfile = "error.log",
        initialdir = str(base_dir.parents[-1])
    )).resolve()
    if not file.is_dir():
        if core.base.isBelongedToHDpip(file):
            tkinter.messagebox.showwarning(language["warning"], language["export_reject"])
            exportCommand()
        else:
            file.write_text(error, encoding = "utf-8")

dialog_arguments = {
    "size": (800, 600),
    "position": None,
    "title": language["title"],
    "text": error,
    "theme": "danger",
    "button": [
        {"text": language["copy"], "theme": "outline-danger", "command": copyCommand},
        {"text": language["export"], "theme": "outline-danger", "command": exportCommand},
        {"text": language["ok"], "theme": "danger"}
    ]
}

root = dialog.DialogTk(**dialog_arguments)
if "auto_close" in globals() and isinstance(auto_close, int) and auto_close > =  0:
    root.after(auto_close, root.destroy)
root.mainloop()
