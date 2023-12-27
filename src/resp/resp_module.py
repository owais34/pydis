# implement serializer and deserializer compatible for both RESP2 & RESP3

# Below are sample resp types
# Simple strings -> +OK\r\n
# Simple errors -> -Error message\r\n
# Integers -> :[<+|->]<value>\r\n , :1000\r\n
# Bulk strings -> $<length>\r\n<data>\r\n , $5\r\nhello\r\n , $0\r\n\r\n (empty string)
# Null bulk strings -> $-1\r\n
# Arrays -> *<number-of-elements>\r\n<element-1>...<element-n> , *0\r\n (empty array) , *2\r\n$5\r\nhello\r\n$5\r\nworld\r\n 
# Null arrays -> *-1\r\n
# Null elements in arrays -> $-1\r\n (null bulk string) , other null types
# Dedicated Null (RESP3) -> _\r\n
# Booleans -> #<t|f>\r\n
# Doubles -> ,[<+|->]<integral>[.<fractional>][<E|e>[sign]<exponent>]\r\n ,1.23\r\n
#  ,inf\r\n (+infinity) > ,-inf\r\n (-infinity) > ,nan\r\n (NaN)
# Big numbers -> ([+|-]<number>\r\n , (3492890328409238509324850943850943825024385\r\n
# Bulk errors -> !<length>\r\n<error>\r\n , !21\r\nSYNTAX invalid syntax\r\n
# Verbatim strings -> =<length>\r\n<encoding>:<data>\r\n , =15\r\ntxt:Some string\r\n
# Maps -> %<number-of-entries>\r\n<key-1><value-1>...<key-n><value-n> , %2\r\n+first\r\n:1\r\n+second\r\n:2\r\n
# Sets -> ~<number-of-elements>\r\n<element-1>...<element-n> , 

string_sample = "*6\r\n$5\r\nHMSET\r\n$4\r\nkey3\r\n$4\r\ncol1\r\n$1\r\n1\r\n$4\r\ncol2\r\n$1\r\n2\r\n"

def deserialize(serializedInput: str):
    # Implement this function
    # parse above string and return a python data typpe as output
    return None