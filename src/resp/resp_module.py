from collections import deque

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

string_sample = "*6\r\n$5\r\nHMSET\r\n$4\r\nkey3\r\n$4\r\ncol1\r\n$1\r\n1\r\n$4\r\ncol2\r\n$1\r\n2\r\n"

def deserialize(serialized_input: str):
    # Implement this function
    # parse above string and return a python data type as output ( it should be a one-to-one translation )
    # Example : +OK\r\n => "OK" , 
    #  *2\r\n$5\r\nhello\r\n$5\r\nworld\r\n  -> ["hello","world"]
    token_queue = deque(serialized_input.split("\r\n"))
    return deserialize_helper(token_queue=token_queue)

def deserialize_helper(token_queue: deque):
    current_element = token_queue.popleft()
    
    match current_element[0]:
        case "+":
            # handle simple string
            return current_element[1:]
        case "-":
            # Error handling to be implemented below placeholder for now
            exception = Exception(current_element[1:])
            return exception
        case ":":
            return int(current_element[1:])
        case "$":
            string_length = int(current_element[1:])
            return get_bulk_string(token_queue=token_queue, string_length=string_length)
        case "*":
            array_length = int(current_element[1:])
            return get_array(token_queue=token_queue,array_length=array_length)
        case "_":
            return None
        case "#":
            return #define a function to process and return a boolean value given current_element as input
        case ",":
            return #define a function to process and return a double value given current_element as input (handle inf and NaN as well)
        case "(":
            return #define a function to process and return a big integer (Hint: just handle it like an int )
        case "!":
            return #define a function to process and handle bulk errors
        case "=":
            return #define a function to process and return Verbatim strings
        case "%":
            return #define a function to process and return maps
        case "~":
            return #define a function to process and return sets (Hint: handle like an array but return a set instead of list)
        
        
            



def get_bulk_string(token_queue: deque, string_length: int) -> str:
    if string_length == -1:
        return None
    
    bulk_string = token_queue.popleft()

    if len(bulk_string) != string_length:
        raise Exception("ERROR bulk string length doesnt match")
    return bulk_string

def get_array(token_queue: deque, array_length: int) -> list:
    if array_length == -1:
        return None
    array = []
    for iterator in range(array_length):
        array.append(deserialize_helper(token_queue))
        # Add better error handling
        # except Exception as e:
        #     if str(e).startswith("IndexError: pop from an empty deque"):
        #         raise Exception("ERROR while parsing array , expected "+array_length+" found "+iterator)
        #     else:
        #         raise e
    return array
        



