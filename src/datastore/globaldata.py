from .logger import Logger
from .shard import Shard
from .persist import PersistAtTimeBehaviour, LocalStorage
from ..utils.util_classes import singleton
from ..resp.serializer import Serializer

@singleton
class GlobalDataStore():
    def __init__(self) -> None:
        self.shard_list = []
        self.current_shard = Shard()
        self.shard_list.append(self.current_shard)
        self.logger_instance = Logger()
        self.persistBehaviour = PersistAtTimeBehaviour(self,LocalStorage(),start_at_time="14:45:00")
        self.command_runner = CommandRunner(self)
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
    
    
    def process_command(self, deserialized_command) -> any:
        # on execution of command
        response = self.command_runner.run(deserialized_command)
        if isinstance(deserialized_command, list):
            self.logger_instance.capture(" ".join(deserialized_command))
        else:
            self.logger_instance.capture(deserialized_command)
        return Serializer().serialize(response)
            

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

