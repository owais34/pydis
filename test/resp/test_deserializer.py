from src.resp.deserializer import Deserializer

deserializer_instance = Deserializer()

def test_simple_string():
    assert deserializer_instance.deserialize("+OK\r\n") == "OK"

# def test_simple_error():
#     error_message ="Error"
#     with pytest.raises(Exception,match=error_message):
#         deserialize("-"+error_message+"\r\n")

def test_simple_error():
    error_message ="Error"
    assert isinstance(deserializer_instance.deserialize("-"+error_message+"\r\n"),Exception)
def test_integegers():
    assert deserializer_instance.deserialize(":1000\r\n") == 1000

def test_bulk_string():
    assert deserializer_instance.deserialize("$5\r\nhello\r\n") == "hello"

def test_bulk_string_null():
    assert deserializer_instance.deserialize("$-1\r\n") == None

def test_bulk_string_1():
    assert deserializer_instance.deserialize("$0\r\n\r\n") == ""

def test_array():
    assert deserializer_instance.deserialize("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n") == ["hello","world"]

def test_boolean():
    assert deserializer_instance.deserialize("#t\r\n") == True

def test_boolean2():
    assert deserializer_instance.deserialize("#f\r\n") == False

def test_doubles():
    assert deserializer_instance.deserialize(",1.23\r\n") == 1.23

def test_doubles2():
    assert deserializer_instance.deserialize(",-1111.78\r\n") == -1111.78

def test_doubles3():
    assert deserializer_instance.deserialize(",-inf\r\n") == float("-inf")

def test_doubles4():
    assert str(deserializer_instance.deserialize(",nan\r\n")) == str(float("nan"))

def test_bignumber():
    assert deserializer_instance.deserialize("(3492890328409238509324850943850943825024385\r\n") == int("3492890328409238509324850943850943825024385")

def test_bulkerror():
    assert isinstance(deserializer_instance.deserialize("!21\r\nSYNTAX invalid syntax\r\n"),Exception)

def test_verbatim_string():
    test_str= "txt:Some string"
    resp_str = "="+str(len(test_str))+"\r\n"+test_str+"\r\n"

    expected_dict={'format':'txt','bytes':bytes(test_str.split(":")[1], "utf-8")}
    assert deserializer_instance.deserialize(resp_str) == expected_dict

def test_map():
    resp_str ="%2\r\n+first\r\n:1\r\n+second\r\n:2\r\n"
    output_dict = {}
    output_dict["first"] = 1
    output_dict["second"] = 2
    assert deserializer_instance.deserialize(resp_str) == output_dict

def test_set():
    resp_str ="~2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
    output_set = set(["hello","world"])
    assert deserializer_instance.deserialize(resp_str) == output_set

def test_aggregate():
    string_sample = "*6\r\n$5\r\nHMSET\r\n$4\r\nkey3\r\n$4\r\ncol1\r\n$1\r\n1\r\n$4\r\ncol2\r\n$1\r\n2\r\n"
    print(deserializer_instance.deserialize(string_sample))
    assert True