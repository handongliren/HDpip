import pytest
import HDpip

class TestVersion:
    """Version 类单元测试。"""

    def test_construct_str(self, ):
        v = HDpip.core.util.Version("0.1.0")
        assert str(v) == "0.1.0"

    def test_construct_short(self, ):
        v = HDpip.core.util.Version("1")
        assert str(v) == "1"

    def test_construct_invalid(self, ):
        with pytest.raises(Exception):
            HDpip.core.util.Version({})

    def test_compare(self, ):
        a = HDpip.core.util.Version("0.1.0")
        b = HDpip.core.util.Version("1")
        assert a < b
        assert b > a
        assert a <= b
        assert b >= a
        assert a != b

    def test_eq(self, ):
        d = HDpip.core.util.Version("2.0.0")
        assert d == HDpip.core.util.Version("2.0.0")
        assert d == HDpip.core.util.Version("2")

    def test_multiple_compare(self, ):
        e = HDpip.core.util.Version("2.0.1")
        assert e.multipleCompare("~=2.0,2.0.1")

    def test_iter(self, ):
        v = HDpip.core.util.Version("0.1.0")
        parts = list(v)
        assert parts == [0, 1, 0]

    def test_len(self, ):
        v = HDpip.core.util.Version("0.1.0")
        assert len(v) == 3

    def test_getitem(self, ):
        v = HDpip.core.util.Version("0.1.0")
        assert v[0] == 0
        assert v[1] == 1

    def test_delitem_raises(self, ):
        v = HDpip.core.util.Version("0.1.0")
        with pytest.raises(TypeError):
            del v[0]

    def test_is_close_to(self, ):
        v = HDpip.core.util.Version("0.1.0")
        assert v.isCloseTo("0.1.1")
        assert v.isCloseTo("0.1.99")

    def test_is_close_to_false(self, ):
        v = HDpip.core.util.Version("0.1.0")
        assert not v.isCloseTo("0.2.0")

    def test_multiple_compare_complex(self, ):
        v = HDpip.core.util.Version("2.0.0")
        assert v.multipleCompare(">1.0.0,<3.0.0,!=2.5.0,>=2.0.0,<=2.0.0")

    def test_multiple_compare_list(self, ):
        v = HDpip.core.util.Version("2.0.0")
        assert v.multipleCompare([">1.0.0", "<3.0.0", "~=2.0"])

    def test_multiple_compare_fail(self, ):
        v = HDpip.core.util.Version("1.0.0")
        assert not v.multipleCompare(">2.0.0")

    def test_construct_from_tuple(self, ):
        v = HDpip.core.util.Version(("0", "1", "0"))
        assert str(v) == "0.1.0"
