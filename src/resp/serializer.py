from sys import getsizeof

BULK_STRING_LIMIT = 512000000
SIMPLE_STRING_LIMIT = 10

DELIMITER = "\r\n"

def serialize(deserialized_input: any) -> str:
    if deserialized_input == None:
        return "_"+DELIMITER
    elif isinstance(deserialized_input, str):
        return encode_string(deserialized_input)
    elif isinstance(deserialized_input, Exception):
        return encode_exception(deserialized_input)
    elif isinstance(deserialized_input, int):
        return encode_int(deserialized_input)
    elif isinstance(deserialized_input, list):
        return encode_list(deserialized_input)
    elif isinstance(deserialized_input, bool):
        return encode_boolean(deserialized_input)
    elif isinstance(deserialized_input, float):
        return encode_float(deserialized_input)
    

def encode_string(deserialized_input: str) -> str:
    if len(deserialized_input)<=SIMPLE_STRING_LIMIT:
        return "+"+deserialized_input+DELIMITER
    else:
         return encode_bulk_string(deserialized_input)

def encode_bulk_string(deserialized_input: str) -> str:
    if getsizeof(deserialized_input)<=BULK_STRING_LIMIT:
        string_len = "$"+str(len(deserialized_input))
        components = [string_len,deserialized_input,""]
        return DELIMITER.join(components)
    else:
         raise Exception("String length exceeded")

def encode_exception(deserialized_input: Exception) -> str:
    error_len = len(str(deserialized_input))
    if error_len<=10:
        return "-"+str(deserialized_input)+DELIMITER
    else:
        components = ["!"+str(error_len),str(deserialized_input),""]
        return DELIMITER.join(components)


def encode_int(deserialized_input: int) -> str:
    if getsizeof(deserialized_input) <= 64:
        return ":"+str(deserialized_input)+DELIMITER
    else:
        return "("+str(deserialized_input)+DELIMITER

def encode_list(deserialized_input: list) -> str:
    components = []
    list_len = len(deserialized_input)
    components.append("*"+str(list_len)+DELIMITER)
    for iterator in range(list_len):
        components.append(serialize(deserialized_input[iterator]))
    
    return "".join(components)

def encode_boolean(deserialized_input: bool) -> str:
    if deserialized_input:
        return "#t"+DELIMITER
    else:
        return "#f"+DELIMITER
    
def encode_float(deserialized_input: float) -> str:
    return ","+str(deserialized_input)+DELIMITER

def encode_bytes(deserialized_input: dict) -> str:
    component_2 = deserialized_input["format"]+":"+deserialized_input["bytes"].decode("utf-8")
    component_1 = "="+str(len(bytes(component_2,"utf-8")))
    return DELIMITER.join([component_1,component_2,""])






