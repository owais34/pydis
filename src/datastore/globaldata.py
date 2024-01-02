from .logger import Logger
from .shard import Shard
from ..utils.util_classes import singleton

@singleton
class GlobalDataStore():
    def __init__(self) -> None:
        self.shard_list = []
        self.current_shard = Shard()
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
        if self.current_shard.is_full():
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
            match deserialized_command[0]:
                case "PING":
                    return "PONG"
                case "GET":
                    return self.datastore.get(deserialized_command[1])
                case "SET":
                    return self.datastore.put(deserialized_command[1], deserialized_command[2])

