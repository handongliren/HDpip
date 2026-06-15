"""
Treeview 控件演示
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))
import HDpip

import maliang
import maliang.theme
import maliang.core.configs
import maliang.standard.dialogs

maliang.core.configs.Env.system = "Windows11"

root = maliang.Tk((1000, 620), title = "Treeview Demo")
root.center()
icon = maliang.PhotoImage(file = str(HDpip.core.base.getBaseDir() / "asset" / "image" / "icon.png"))
root.iconphoto(True, icon)
maliang.theme.customize_window(root, disable_maximize_button = True)

main = maliang.Canvas(root, expand = "xy", auto_zoom = True, auto_update = True)
main.place(width = 1000, height = 620)

title = maliang.Text(main, (500, 20), (400, 36), text = "Treeview 控件演示",
                     fontsize = 24, weight = "bold", anchor = "center")

tv = HDpip.gui.base.Treeview(main, (12, 104), (976, 420), columns = ("package", "version", "status"),
              show = "headings", height = 14, selectmode = "extended")
tv.treeview.heading("package", text = "包名")
tv.treeview.heading("version", text = "版本")
tv.treeview.heading("status", text = "状态")
tv.treeview.column("package", width = 280, minwidth = 80)
tv.treeview.column("version", width = 120, minwidth = 60)
tv.treeview.column("status", width = 100, minwidth = 60)

packages = [
    ("pip", "25.3", "已安装"),
    ("maliang", "3.1.0", "已安装"),
    ("HDpip", "0.0.4", "当前项目"),
    ("setuptools", "80.9.0", "已安装"),
    ("wheel", "0.45.1", "已安装"),
    ("darkdetect", "0.8.0", "已安装"),
    ("pywinstyles", "1.5.0", "已安装"),
    ("hPyT", "1.3.0", "已安装"),
    ("pyyaml", "6.0.3", "已安装"),
    ("pipdeptree", "2.26.2", "已安装"),
    ("requests", "2.32.4", "已安装"),
    ("numpy", "2.3.5", "可升级"),
    ("pandas", "2.3.4", "可升级"),
    ("Pillow", "11.3.0", "已安装"),
    ("flask", "3.2.0", "未安装"),
    ("django", "5.2.0", "未安装"),
    ("fastapi", "0.121.1", "未安装"),
    ("sqlalchemy", "2.0.43", "未安装"),
    ("celery", "5.6.0", "未安装"),
    ("redis", "6.4.0", "未安装"),
    ("pytest", "8.5.0", "未安装"),
    ("black", "25.4.0", "未安装"),
    ("mypy", "1.17.1", "未安装"),
    ("ruff", "0.14.2", "未安装"),
    ("uvicorn", "0.38.0", "未安装"),
]
for name, ver, st in packages:
    tv.treeview.insert("", "end", text = "", values = (name, ver, st))

tv.enableCheckbox(True)

info_bar = maliang.Text(main, (12, 540), (976, 24),
                        text = "提示: 拖拽列分隔线调整列宽 | 滚轮滚动 | Ctrl+点击多选 | Shift+点击范围选择",
                        fontsize = 11, anchor = "w")
info_bar.style.set(fg = HDpip.gui.base.gray_800)

sel_label = maliang.Text(main, (12, 568), (976, 24),
                         text = "当前选中: pip",
                         fontsize = 11, anchor = "w")

counter = len(packages)
show_headings = True

def refresh_selection_info():
    sel = tv.treeview.selection()
    info = f"选中 {len(sel)} 项 | 勾选 {len(sel)} 项: {', '.join(sel)}"
    sel_label.set(info)


def add_package():
    global counter
    counter += 1
    tv.insert("", "end", values = (f"new_pkg_{counter}", f"0.{counter}.0", "新增"))
    tv.treeview.see(tv.treeview.get_children()[-1])


def delete_selected():
    for iid in list(tv.treeview.selection()):
        tv.treeview.delete(iid)
    refresh_selection_info()


def toggle_theme():
    cur = maliang.theme.get_color_mode()
    maliang.theme.set_color_mode("light" if cur == "dark" else "dark")


def toggle_headings():
    global show_headings
    show_headings = not show_headings
    if show_headings:
        tv.treeview.configure(show = "tree headings")
        btn_hide_head.set("隐藏标题")
    else:
        tv.treeview.configure(show = "tree")
        btn_hide_head.set("显示标题")


def scroll_bottom():
    tv.treeview.yview_moveto(1.0)


def show_selection_info():
    sel = tv.getSelectedValues()
    if sel:
        lines = [f"共选中 {len(sel)} 项:"]
        for vals in sel[:5]:
            lines.append(f"  {vals[0]}")
        if len(sel) > 5:
            lines.append(f"  ... 等 {len(sel)} 项")
        info = "\n".join(lines)
    else:
        info = "无选中项"
    maliang.standard.dialogs.TkMessage(message = info, title = "选中项信息",
                                       icon = "info", option = "ok", master = root)


def on_select(_event):
    refresh_selection_info()


tv.treeview.bind("<<TreeviewSelect>>", on_select)

toolbar = maliang.Canvas(main, expand = "", auto_update = True)
toolbar.place(x = 12, y = 60, width = 976, height = 36)

btn_add = HDpip.gui.base.Button(toolbar, (0, 0), (80, 30), text = "添加", theme = "primary",
                 command = add_package)
btn_del = HDpip.gui.base.Button(toolbar, (90, 0), (80, 30), text = "删除选中", theme = "danger",
                 command = delete_selected)
btn_theme = HDpip.gui.base.Button(toolbar, (180, 0), (80, 30), text = "切换主题", theme = "secondary",
                   command = toggle_theme)
btn_hide_head = HDpip.gui.base.Button(toolbar, (270, 0), (100, 30), text = "隐藏标题",
                       theme = "outline-secondary", command = toggle_headings)
btn_scroll = HDpip.gui.base.Button(toolbar, (380, 0), (80, 30), text = "滚到底",
                    theme = "outline-warning", command = scroll_bottom)
btn_info = HDpip.gui.base.Button(toolbar, (470, 0), (80, 30), text = "查看选中",
                  theme = "outline-primary", command = show_selection_info)

refresh_selection_info()
root.mainloop()
