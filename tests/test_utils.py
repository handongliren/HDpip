import pytest
import HDpip

class TestUtils:
    """工具函数测试。"""

    def test_get_base_dir(self, ):
        p = HDpip.core.system.getBaseDir()
        assert p.is_dir()

    def test_get_python_path(self, ):
        p = HDpip.core.system.getPythonPath()
        assert p.is_file()

    def test_get_pip_version(self, ):
        v = HDpip.core.system.getPipVersion()
        assert isinstance(v, HDpip.core.util.Version)

    def test_is_dev(self, ):
        assert isinstance(HDpip.core.system.isDev(), bool)

    def test_hdpip_error(self, ):
        err = HDpip.core.util.HDpipError("test error")
        assert err.message == "test error"
        assert str(err) == "test error"

    def test_multiple_spilt(self, ):
        result = HDpip.core.util.multipleSpilt("a|b.c|d", "|,.")
        assert result == ["a", "b", "c", "d"]

    def test_multiple_spilt_single(self, ):
        result = HDpip.core.util.multipleSpilt("a,b,c", [","])
        assert result == ["a", "b", "c"]

    def test_shell_decode_bytes(self, ):
        result = HDpip.core.system.shellDecode(b"hello")
        assert result == "hello"

    def test_shell_decode_str(self, ):
        result = HDpip.core.system.shellDecode("hello")
        assert result == "hello"

    def test_get_system_version(self, ):
        ver = HDpip.core.system.getSystemVersion()
        assert isinstance(ver, str)
        assert len(ver) > 0
