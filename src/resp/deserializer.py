from collections import deque
from ..utils.util_classes import singleton

# implement serializer and deserializer compatible for both RESP2 & RESP3

# Below are sample resp types
# 1)Simple strings -> +OK\r\n
# 2)Simple errors -> -Error message\r\n
# 3)Integers -> :[<+|->]<value>\r\n , :1000\r\n
# 4)Bulk strings -> $<length>\r\n<data>\r\n , $5\r\nhello\r\n , $0\r\n\r\n (empty string)
# 5)Null bulk strings -> $-1\r\n
# 6)Arrays -> *<number-of-elements>\r\n<element-1>...<element-n> , *0\r\n (empty array) , *2\r\n$5\r\nhello\r\n$5\r\nworld\r\n 
# 7)Null arrays -> *-1\r\n
# 8)Null elements in arrays -> $-1\r\n (null bulk string) , other null types
# 9)Dedicated Null (RESP3) -> _\r\n
# 10)Booleans -> #<t|f>\r\n
# 11)Doubles -> ,[<+|->]<integral>[.<fractional>][<E|e>[sign]<exponent>]\r\n ,1.23\r\n
# 12)Doubles -> ,inf\r\n (+infinity) > ,-inf\r\n (-infinity) > ,nan\r\n (NaN)
# 13)Big numbers -> ([+|-]<number>\r\n , (3492890328409238509324850943850943825024385\r\n
# 14)Bulk errors -> !<length>\r\n<error>\r\n , !21\r\nSYNTAX invalid syntax\r\n
# 15)Verbatim strings -> =<length>\r\n<encoding>:<data>\r\n , =15\r\ntxt:Some string\r\n
# 16)Maps -> %<number-of-entries>\r\n<key-1><value-1>...<key-n><value-n> , %2\r\n+first\r\n:1\r\n+second\r\n:2\r\n
# 17)Sets -> ~<number-of-elements>\r\n<element-1>...<element-n> , 

BULK_STRING_LIMIT = 512000000
SIMPLE_STRING_LIMIT = 100000

@singleton
class Deserializer:


    def deserialize(self, serialized_input: str):
        # Implement this function
        # parse above string and return a python data type as output ( it should be a one-to-one translation )
        # Example : +OK\r\n => "OK" , 
        #  *2\r\n$5\r\nhello\r\n$5\r\nworld\r\n  -> ["hello","world"]
        # ["*2","$5","hello","$5","world"]
        token_queue = deque(serialized_input.split("\r\n"))
        return self.deserialize_helper(token_queue)

    def deserialize_helper(self, token_queue: deque):
        current_element = token_queue.popleft()
        
        match current_element[0]:
            case "+":
                # handle simple string
                if len(current_element[1:])>SIMPLE_STRING_LIMIT:
                    raise Exception("Max string length exceeded for Simple String")
                elif current_element[1:].find("\r") != -1 or current_element[1:].find("\n")!= -1:
                    raise Exception("Simple string should not have escape sequences")
                return current_element[1:]
            case "-":
                # Error handling to be implemented below placeholder for now
                exception = Exception(current_element[1:])
                return exception
            case ":":
                return self.get_int(current_element)
            case "$":
                string_length = int(current_element[1:])
                if string_length>BULK_STRING_LIMIT:
                    raise Exception("Max string length exceeded for Bulk String")
                return self.get_bulk_string(token_queue, string_length)
            case "*":
                array_length = int(current_element[1:])
                return self.get_array(token_queue,array_length)
            case "_":
                return None
            case "#":
                return self.get_boolean(current_element)
            case ",":
                return self.get_double(current_element)
            case "(":
                return self.get_int(current_element)
            case "!":
                string_length = int(current_element[1:])
                return self.get_bulk_error(token_queue,string_length)
            case "=":
                string_length = int(current_element[1:])
                return self.get_verbatim_string(token_queue,string_length)
            case "%":
                map_length = int(current_element[1:])
                return self.get_map(token_queue, map_length=map_length)
            case "~":
                set_length = int(current_element[1:])
                return self.get_set(token_queue, set_length=set_length)

    def get_int(self, current_element: str) -> int:
        return int(current_element[1:])

    def get_bulk_string(self, token_queue: deque, string_length: int) -> str:
        if string_length == -1:
            return None
        
        bulk_string = token_queue.popleft()
        byte_array_len = len(bytes(bulk_string,"utf-8"))
        if byte_array_len != string_length:
            raise Exception("ERROR bulk string length doesnt match expected %d got %d, |%s|" %(string_length,byte_array_len, bulk_string))
        return bulk_string

    def get_array(self, token_queue: deque, array_length: int) -> list:
        if array_length == -1:
            return None
        array = []
        for iterator in range(array_length):
            array.append(self.deserialize_helper(token_queue))
            # Add better error handling
            # except Exception as e:
            #     if str(e).startswith("IndexError: pop from an empty deque"):
            #         raise Exception("ERROR while parsing array , expected "+array_length+" found "+iterator)
            #     else:
            #         raise e
        return array
            
    def get_boolean(self, current_element: str)->bool:
        if current_element[1:] == "t":
            return True
        elif current_element[1:] == "f":
            return False
        else:
            raise Exception("Invalid boolean type expected t/f found " + current_element[1:])

    def get_double(self, current_element: str) -> float:
        return float(current_element[1:])

    def get_bulk_error(self, token_queue: deque, string_length: int) -> str:
        if string_length == -1:
            return None
        
        bulk_string = token_queue.popleft()

        if len(bulk_string) != string_length:
            raise Exception("ERROR bulk string length doesnt match")
        return Exception(bulk_string)

    def get_verbatim_string(self, token_queue: deque, string_length: int) -> dict:
        raw_string = self.get_bulk_string(token_queue,string_length)
        components = raw_string.split(":")
        file_format = components[0]
        output_dict = {}
        output_dict["format"]=file_format
        output_dict["bytes"]=bytes(components[1], "utf-8")
        return output_dict

    def get_map(self, token_queue: deque, map_length: int) -> dict:
        output_dictionary = {}

        for iterator in range(map_length):
            current_key = self.deserialize_helper(token_queue)
            if isinstance(current_key,str) == False:
                raise Exception("Invalid Key Type expected str found "+str(current_key.__class__))
            current_value = self.deserialize_helper(token_queue)
            output_dictionary[current_key]=current_value

        return output_dictionary

    def get_set(self, token_queue: deque, set_length: int) -> set:
        output_set = set()
        for iterator in range(set_length):
            output_set.add(self.deserialize_helper(token_queue))

        return output_set

