import pytest
import HDpip


class TestVersion:
    """Version 类单元测试。"""

    def test_construct_str(self, ):
        v = HDpip.core.base.Version("0.1.0")
        assert str(v) == "0.1.0"

    def test_construct_short(self, ):
        v = HDpip.core.base.Version("1")
        assert str(v) == "1"

    def test_construct_invalid(self, ):
        with pytest.raises(Exception):
            HDpip.core.base.Version({})

    def test_compare(self, ):
        a = HDpip.core.base.Version("0.1.0")
        b = HDpip.core.base.Version("1")
        assert a < b
        assert b > a
        assert a <= b
        assert b >= a
        assert a != b

    def test_eq(self, ):
        d = HDpip.core.base.Version("2.0.0")
        assert d == HDpip.core.base.Version("2.0.0")
        assert d == HDpip.core.base.Version("2")

    def test_multiple_compare(self, ):
        e = HDpip.core.base.Version("2.0.1")
        assert e.multipleCompare("~=2.0,2.0.1")

    def test_iter(self, ):
        v = HDpip.core.base.Version("0.1.0")
        parts = list(v)
        assert parts == [0, 1, 0]

    def test_len(self, ):
        v = HDpip.core.base.Version("0.1.0")
        assert len(v) == 3

    def test_getitem(self, ):
        v = HDpip.core.base.Version("0.1.0")
        assert v[0] == 0
        assert v[1] == 1

    def test_delitem_raises(self, ):
        v = HDpip.core.base.Version("0.1.0")
        with pytest.raises(TypeError):
            del v[0]


class TestData:
    """Data 类单元测试。"""

    @pytest.fixture
    def data_file(self, ):
        import pathlib
        return pathlib.Path(__file__).parents[1] / "HDpip" / "setting" / "auto.zh-CN.json"

    def test_open_load_getitem(self, data_file, ):
        d = HDpip.core.base.Data()
        d.open(str(data_file))
        d.load()
        assert isinstance(d["pip"]["mirror"], list)
        assert len(d["pip"]["mirror"]) > 0
        assert "name" in d["pip"]["mirror"][0]

    def test_add_merge(self, data_file, ):
        d = HDpip.core.base.Data()
        d.open(str(data_file))
        d.load()
        merged = (d + {"note": "test"}).data
        assert merged["note"] == "test"


class TestUtils:
    """工具函数测试。"""

    def test_get_base_dir(self, ):
        p = HDpip.core.base.getBaseDir()
        assert p.is_dir()

    def test_get_python_path(self, ):
        p = HDpip.core.base.getPythonPath()
        assert p.is_file()

    def test_get_pip_version(self, ):
        v = HDpip.core.base.getPipVersion()
        assert isinstance(v, HDpip.core.base.Version)

    def test_is_dev(self, ):
        assert isinstance(HDpip.core.base.isDev(), bool)


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
