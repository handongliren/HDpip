import pathlib

import pytest
import HDpip

class TestData:
    """Data 类单元测试。"""

    @pytest.fixture
    def data_file(self, ):
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

    def test_iadd_merge(self, data_file, ):
        d = HDpip.core.base.Data()
        d.open(str(data_file))
        d.load()
        d += {"note": "inplace"}
        assert d["note"] == "inplace"

    def test_nested_tuple_getitem(self, data_file, ):
        d = HDpip.core.base.Data()
        d.open(str(data_file))
        d.load()
        result = d["pip", "mirror"]
        assert isinstance(result, list)

    def test_events(self, data_file, ):
        d = HDpip.core.base.Data()
        events = []

        def callback(event_type, event_data):
            events.append(event_type)

        d.registerEvent(callback)
        d.open(str(data_file))
        d.load()
        assert "open" in events
        assert "load" in events

    def test_unregister_event(self, data_file, ):
        d = HDpip.core.base.Data()
        calls = []

        def cb(et, ed):
            calls.append(et)

        d.registerEvent(cb)
        d.unregisterEvent(cb)
        d.open(str(data_file))
        d.load()
        assert len(calls) == 0
