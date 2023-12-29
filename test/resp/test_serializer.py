from src.resp.serializer import Serializer

serializer_instance = Serializer()

def test_None():
    assert "_\r\n" == serializer_instance.serialize(None)

def test_exception():
    assert "-Error\r\n" == serializer_instance.serialize(Exception("Error"))
    
def test_integers():
    assert ":1000\r\n" == serializer_instance.serialize(1000)

def test_bool():
    assert "#t\r\n" == serializer_instance.serialize(True)

def test_bool_2():
    assert "#f\r\n" == serializer_instance.serialize(False)

def test_float():
    assert ",1.23\r\n" == serializer_instance.serialize(1.23)

def test_bignum():
    assert "(3492890328409238509324850943850943825024385122323232323232323434343434343434343\r\n" == \
          serializer_instance.serialize(int('3492890328409238509324850943850943825024385122323232323232323434343434343434343'))

def test_verbatim_string():
    test_str= "txt:Some string"
    resp_str = "="+str(len(test_str))+"\r\n"+test_str+"\r\n"
    verbatim_dict={'format':'txt','bytes':bytes(test_str.split(":")[1], "utf-8")}
    assert resp_str == serializer_instance.serialize(verbatim_dict)

def test_map():
    resp_str ="%2\r\n+first\r\n:1\r\n+second\r\n:2\r\n"
    input_dict = {}
    input_dict["first"] = 1
    input_dict["second"] = 2
    assert resp_str == serializer_instance.serialize(input_dict)

def test_set():
    resp_str ="~2\r\n+world\r\n+hello\r\n"
    resp_str2 ="~2\r\n+hello\r\n+world\r\n"
    input_set = set(["hello","world"])
    assert (resp_str == serializer_instance.serialize(input_set) 
    or resp_str2 == serializer_instance.serialize(input_set))
