from .logger import Logger
from .shard import Shard
from ..utils.util_classes import singleton
from collections import deque
from ..resp.deserializer import Deserializer
from ..resp.serializer import Serializer
from time import time
import json

@singleton
class GlobalDataStore():
    def __init__(self) -> None:
        self.shard_list = []
        self.current_shard = Shard()
        self.shard_max_keys = 10**9
        self.shard_list.append(self.current_shard)
        pass

    def get(self, key: str) -> any:
        for s in self.shard_list:
            if key in s:
                return s.get(key)
        
        return None
    
    def put(self, key: str, value: any):
        for shard in self.shard_list:
            if key in shard:
                shard[key] = value
                return "OK"
        
        current_shard = self.get_current_shard()
        current_shard[key]= value
        return "OK"

    def get_current_shard(self):
        if len(self.current_shard)>=self.shard_max_keys:
            new_shard = Shard()
            self.shard_list.append(new_shard)
            self.current_shard = new_shard
        
        return self.current_shard
    
    def set_shard_list_if_not_empty(self, shard_list: list):
        if shard_list != None and len(shard_list)>0:
            self.shard_list = shard_list
            self.current_shard = shard_list[-1]

    
    

@singleton
class CommandRunner():
    def __init__(self, datastore: GlobalDataStore) -> None:
        self.datastore = datastore

    def run(self, deserialized_command):
        if deserialized_command == "PING":
            return "PONG"
        elif isinstance(deserialized_command, list):
            current_queue = deque(deserialized_command) 
            output = []
            while current_queue.__len__()>0:
                command = current_queue.popleft()
                match command:
                    case "PING":
                        output.append("PONG")
                    case "GET":
                        output.append(self.datastore.get(current_queue.popleft()))
                    case "SET":
                        output.append(self.datastore.put(current_queue.popleft(), current_queue.popleft()))
            return output
                
    def execute_all(self, command_list: list):
        for command in command_list:
            self.run_json_command(command)

    def run_serialized(self, command):
        deserialized_cmd = Deserializer().deserialize(command)
        final_output = None
        match deserialized_cmd[0]:
            case "PING":
                final_output = "PONG"
            case "GET":
                try:
                    final_output=self.datastore.get(deserialized_cmd[1])
                except Exception as e:
                    final_output = e
            case "SET":
                try:
                    final_output = self.datastore.put(deserialized_cmd[1],deserialized_cmd[2])
                    Logger().capture(deserialized_cmd,time())
                except Exception as e:
                    final_output = e
        ser_output = Serializer().serialize(final_output)

        return ser_output
    
    def run_json_command(self, command):
        decoded_json = json.loads(command)
        final_output = None
        match decoded_json[0]:
            case "PING":
                final_output = "PONG"
            case "GET":
                try:
                    final_output=self.datastore.get(decoded_json[1])
                except Exception as e:
                    final_output = e
            case "SET":
                try:
                    final_output = self.datastore.put(decoded_json[1],decoded_json[2])
                    Logger().capture(command,time())
                except Exception as e:
                    final_output = e
        return final_output


    
        

