from src.resp.resp_module import deserialize
import pytest

def test_simple_string():
    assert deserialize("+OK\r\n") == "OK"

# def test_simple_error():
#     error_message ="Error"
#     with pytest.raises(Exception,match=error_message):
#         deserialize("-"+error_message+"\r\n")

def test_simple_error():
    error_message ="Error"
    assert isinstance(deserialize("-"+error_message+"\r\n"),Exception)
def test_integegers():
    assert deserialize(":1000\r\n") == 1000

def test_bulk_string():
    assert deserialize("$5\r\nhello\r\n") == "hello"

def test_bulk_string_null():
    assert deserialize("$-1\r\n") == None

def test_bulk_string_1():
    assert deserialize("$0\r\n\r\n") == ""

def test_array():
    assert deserialize("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n") == ["hello","world"]
