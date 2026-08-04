"""
Table 控件演示与测试（基于 maliang.table.TkTable / tksheet）
"""

import sys
import pathlib
base_dir = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(base_dir))

import maliang
import maliang.table

def _make_table(master, columns, height=8, selectmode="extended", width=780, height_px=300):
    """创建 TkTable 的工厂函数。"""
    t = maliang.table.TkTable(
        master,
        header=list(columns),
        total_rows=0,
        total_columns=len(columns),
        show_vertical_grid=True,
        show_horizontal_grid=True,
    )
    t.place(x=10, y=10, width=width, height=height_px)
    t.enable_bindings(
        "single_select" if selectmode == "browse" else "toggle_select",
        "drag_select", "column_select", "row_select",
        "column_width_resize", "double_click_column_resize", "copy",
    )
    return t

class TestTable:
    """Table 控件测试。"""

    PACKAGES = [
        ("pip", "25.3", "已安装"),
        ("maliang", "3.1.0", "已安装"),
        ("HDpip", "0.0.4", "当前项目"),
    ]

    def test_create_table(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("package", "version", "status"))
        assert t is not None

    def test_headers_and_columns(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("pkg", "ver"))
        t.headers(["包名", "版本"])
        t.set_column_widths([280, 120])
        assert t.headers() == ["包名", "版本"]

    def test_insert_and_row_count(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("package", "version", "status"))

        for name, ver, st in self.PACKAGES:
            t.insert_row([name, ver, st])

        assert t.get_total_rows() == len(self.PACKAGES)

    def test_selection(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("package", "version", "status"))

        for name, ver, st in self.PACKAGES:
            t.insert_row([name, ver, st])

        t.select_row(0)
        assert 0 in t.get_selected_rows()

    def test_get_cell_data(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("package", "version", "status"))
        t.insert_row(["pip", "25.3", "已安装"])
        t.set_cell_data(0, 2, "已更新")
        assert t.get_cell_data(0, 2) == "已更新"

    def test_delete_row(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("package", "version", "status"))

        for name, ver, st in self.PACKAGES:
            t.insert_row([name, ver, st])

        t.delete_row(0)
        assert t.get_total_rows() == len(self.PACKAGES) - 1

    def test_see_and_scroll(self, tk_root, ):
        root, canvas = tk_root
        t = _make_table(canvas, ("pkg", "ver"))

        for i in range(20):
            t.insert_row([f"pkg_{i}", f"0.{i}.0"])

        t.see(19)
        t.yview_moveto(1.0)

if __name__ == "__main__":
    import maliang.theme
    import maliang.core.configs
    import maliang.standard.dialogs
    import HDpip

    maliang.core.configs.Env.system = "Windows11"

    root = maliang.Tk((1000, 620), title="Table Demo (tksheet)")
    root.center()
    icon = maliang.PhotoImage(file=str(HDpip.core.system.getBaseDir() / "asset" / "image" / "icon.png"))
    root.iconphoto(True, icon)
    maliang.theme.customize_window(root, disable_maximize_button=True)

    main = maliang.Canvas(root, expand="xy", auto_zoom=True, auto_update=True)
    main.place(width=1000, height=620)

    maliang.Text(main, (500, 20), (400, 36), text="Table 控件演示 (tksheet)",
                 fontsize=24, weight="bold", anchor="center")

    tv = maliang.table.TkTable(
        main,
        header=["包名", "版本", "状态"],
        total_rows=0,
        total_columns=3,
        show_vertical_grid=True,
        show_horizontal_grid=True,
    )
    tv.place(x=12, y=68, width=976, height=460)
    tv.set_column_widths([280, 120, 100])
    tv.enable_bindings(
        "toggle_select", "drag_select", "column_select", "row_select",
        "column_width_resize", "double_click_column_resize", "copy",
    )

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
    ]
    for name, ver, st in packages:
        tv.insert_row([name, ver, st])

    info_bar = maliang.Text(main, (12, 540), (976, 24),
                            text="提示: 拖拽列分隔线调整列宽 | Ctrl+点击多选 | 滚轮滚动",
                            fontsize=11, anchor="w")
    info_bar.style.set(fg=HDpip.gui.base.gray_800)

    sel_label = maliang.Text(main, (12, 568), (976, 24),
                             text="当前选中: 无", fontsize=11, anchor="w")
    counter = len(packages)

    def refresh_selection_info():
        sel = tv.get_selected_rows()
        info = f"选中 {len(sel)} 项: {', '.join(str(s) for s in sorted(sel))}"
        sel_label.set(info)

    def add_package():
        global counter
        counter += 1
        tv.insert_row([f"new_pkg_{counter}", f"0.{counter}.0", "新增"])
        tv.see(tv.get_total_rows() - 1)

    def delete_selected():
        for row in sorted(tv.get_selected_rows(), reverse=True):
            tv.delete_row(row)
        refresh_selection_info()

    def scroll_bottom():
        tv.yview_moveto(1.0)

    def show_selection_info():
        sel = tv.get_selected_rows()
        if sel:
            info = f"共选中 {len(sel)} 项: {', '.join(str(s) for s in sorted(sel))}"
        else:
            info = "无选中项"
        maliang.standard.dialogs.TkMessage(message=info, title="选中项信息",
                                           icon="info", option="ok", master=root)

    tv.bind("<<SheetSelect>>", lambda e: refresh_selection_info())

    toolbar = maliang.Canvas(main, expand="", auto_update=True)
    toolbar.place(x=12, y=28, width=976, height=36)

    HDpip.gui.base.Button(toolbar, (0, 0), (80, 30), text="添加", theme="primary",
                           command=add_package)
    HDpip.gui.base.Button(toolbar, (90, 0), (80, 30), text="删除选中", theme="danger",
                           command=delete_selected)
    HDpip.gui.base.Button(toolbar, (180, 0), (80, 30), text="滚到底",
                           theme="outline-warning", command=scroll_bottom)
    HDpip.gui.base.Button(toolbar, (270, 0), (80, 30), text="查看选中",
                           theme="outline-primary", command=show_selection_info)

    refresh_selection_info()
    root.mainloop()
