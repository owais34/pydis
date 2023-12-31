from sys import getsizeof
from ..utils.util_classes import singleton

BULK_STRING_LIMIT = 512000000
SIMPLE_STRING_LIMIT = 10

DELIMITER = "\r\n"

@singleton
class Serializer:

    def serialize(self, deserialized_input: any) -> str:
        if deserialized_input == None:
            return "_"+DELIMITER
        elif isinstance(deserialized_input, str):
            return self.encode_string(deserialized_input)
        elif isinstance(deserialized_input, Exception):
            return self.encode_exception(deserialized_input)
        elif isinstance(deserialized_input, bool):
            return self.encode_boolean(deserialized_input)
        elif isinstance(deserialized_input, int):
            return self.encode_int(deserialized_input)
        elif isinstance(deserialized_input, list):
            return self.encode_list(deserialized_input)
        elif isinstance(deserialized_input, float):
            return self.encode_float(deserialized_input)
        elif self.is_verbatim_string(deserialized_input):
            return self.encode_bytes(deserialized_input)
        elif isinstance(deserialized_input, dict):
            return self.encode_map(deserialized_input)
        elif isinstance(deserialized_input, set):
            return self.encode_set(deserialized_input)
        
    
    def is_verbatim_string(self, deserialized_input) -> bool:
        return isinstance(deserialized_input, dict) and \
            "bytes" in deserialized_input and \
            "format" in deserialized_input and \
            len(deserialized_input) == 2 and \
            isinstance(deserialized_input.get("bytes"),bytes) 
            

    def encode_string(self, deserialized_input: str) -> str:
        if len(deserialized_input)<=SIMPLE_STRING_LIMIT:
            return "+"+deserialized_input+DELIMITER
        else:
            return self.encode_bulk_string(deserialized_input)

    def encode_bulk_string(self, deserialized_input: str) -> str:
        byte_array_len = len(bytes(deserialized_input,"utf-8"))
        if byte_array_len<=BULK_STRING_LIMIT:
            string_len = "$"+str(byte_array_len)
            components = [string_len,deserialized_input,""]
            return DELIMITER.join(components)
        else:
            raise Exception("max length exceeded")

    def encode_exception(self, deserialized_input: Exception) -> str:
        error_len = len(str(deserialized_input))
        if error_len<=10:
            return "-"+str(deserialized_input)+DELIMITER
        else:
            components = ["!"+str(error_len),str(deserialized_input),""]
            return DELIMITER.join(components)


    def encode_int(self, deserialized_input: int) -> str:
        if getsizeof(deserialized_input) <= getsizeof(0):
            return ":"+str(deserialized_input)+DELIMITER
        else:
            return "("+str(deserialized_input)+DELIMITER

    def encode_list(self, deserialized_input: list) -> str:
        components = []
        list_len = len(deserialized_input)
        components.append("*"+str(list_len)+DELIMITER)
        for iterator in range(list_len):
            components.append(self.serialize(deserialized_input[iterator]))
        
        return "".join(components)

    def encode_boolean(self, deserialized_input: bool) -> str:
        if deserialized_input:
            return "#t"+DELIMITER
        else:
            return "#f"+DELIMITER
        
    def encode_float(self, deserialized_input: float) -> str:
        return ","+str(deserialized_input)+DELIMITER

    def encode_bytes(self, deserialized_input: dict) -> str:
        component_2 = deserialized_input["format"]+":"+deserialized_input["bytes"].decode("utf-8")
        component_1 = "="+str(len(bytes(component_2,"utf-8")))
        return DELIMITER.join([component_1,component_2,""])
    
    def encode_map(self, deserialized_input: dict) -> str:
        map_length = len(deserialized_input)
        components = ["%"+str(map_length)+DELIMITER]
        for key in deserialized_input:
            components.append(self.encode_string(key))
            components.append(self.serialize(deserialized_input.get(key)))
        
        return "".join(components)
    
    def encode_set(self, deserialized_input: set) -> str:
        set_length = len(deserialized_input)
        components = ["~"+str(set_length)+DELIMITER]
        for element in deserialized_input:
            components.append(self.serialize(element))
        
        return "".join(components)






