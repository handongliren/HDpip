import decimal
import pytest
import HDpip
from HDpip.gui.custom import utility


class TestGuiBase:
    """GUI 基础函数测试。"""

    def test_get_system_dpi_from_tk(self, monkeypatch):
        import HDpip.gui.custom as gui_custom

        class DummyTk:
            def withdraw(self):
                pass

            def update_idletasks(self):
                pass

            def winfo_fpixels(self, _):
                return 100.0

            def destroy(self):
                pass

        utility._dpi_cache = None
        monkeypatch.setattr(utility.tkinter, "Tk", lambda: DummyTk())

        assert utility.getDpi() == 100.0

    def test_get_system_dpi_fallback(self, monkeypatch):
        import HDpip.gui.custom as gui_custom

        def raise_tk(*args, **kwargs):
            raise RuntimeError("tk fail")

        utility._dpi_cache = None
        monkeypatch.setattr(utility.tkinter, "Tk", raise_tk)

        assert utility.getDpi() == 96.0

    def test_smart_scale_int(self, ):
        import HDpip.gui.custom as gui_custom

        utility._dpi_cache = None
        utility._smart_cache.clear()
        val = utility.ss(100, base_size=(1920, 1080), screen_size=(1920, 1080))
        assert isinstance(val, int)

    def test_smart_scale_tuple(self, ):
        import HDpip.gui.custom as gui_custom

        utility._smart_cache.clear()
        result = utility.ss((100, 200), base_size=(1200, 800), screen_size=(1200, 800))
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(v, int) for v in result)

    def test_smart_scale_identity(self, ):
        """1280x720 屏幕下默认基准(1200,800)严格模式缩放。"""
        import HDpip.gui.custom as gui_custom

        utility._smart_cache.clear()
        utility._dpi_cache = None
        val = utility.ss(100, base_size=(1200, 800), screen_size=(1280, 720))
        assert isinstance(val, int)

    def test_smart_scale_zero(self, ):
        import HDpip.gui.custom as gui_custom

        utility._smart_cache.clear()
        val = utility.ss(0)
        assert val == 0

    def test_px_to_pt(self, ):
        import HDpip.gui.custom as gui_custom

        utility._dpi_cache = None
        pt = utility.pxToPt(96, dpi=96)
        assert pt == 72

    def test_pt_to_px(self, ):
        import HDpip.gui.custom as gui_custom

        utility._dpi_cache = None
        px = utility.ptToPx(72, dpi=96)
        assert px == 96

    def test_get_smart_scale_value(self, ):
        import HDpip.gui.custom as gui_custom

        utility._smart_cache.clear()
        val = utility.getSmartScaleValue(base_size=(1200, 800), screen_size=(1200, 800), use_cache=False)
        assert isinstance(val, decimal.Decimal)

    def test_get_screen_size(self, ):
        import HDpip.gui.custom as gui_custom

        utility._dpi_cache = None
        w, h = utility.getScreenSize()
        assert w > 0
        assert h > 0
