import pytest
import HDpip

class TestPipApi:
    """pip API 测试（非破坏性）。"""

    def test_pip_head(self, ):
        head = HDpip.core.pip_api.pip_head
        assert "-m pip" in head

    def test_version(self, ):
        v = HDpip.core.pip_api.version()
        assert "pip_version" in v
        assert isinstance(v["pip_version"], HDpip.core.base.Version)
        assert "python_version" in v

    def test_list(self, ):
        pkgs = HDpip.core.pip_api.list_()
        assert isinstance(pkgs, list)
        assert any(p["name"] == "pip" for p in pkgs)

    def test_show(self, ):
        info = HDpip.core.pip_api.show("pip")
        assert info is not None
        assert info["Name"] == "pip"
        assert "Version" in info
