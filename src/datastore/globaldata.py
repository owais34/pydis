from .logger import Logger
from .shard import Shard
from ..utils.util_classes import singleton
from collections import deque

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
            self.run(command)

    
        

