from .datastore.globaldata import GlobalDataStore,CommandRunner
from .datastore.persist import PersistAtTimeBehaviour, LocalStorage
from .datastore.logger import Logger
from .resp.deserializer import Deserializer
from .utils.util_classes import singleton


start_at_time = "14:45:00" # get this from conf file

@singleton
class Pydis():
    def __init__(self) -> None:
        self.global_data_store = GlobalDataStore()
        self.filename_prefix = "shard"
        self.command_runner = CommandRunner(self.global_data_store)
        self.local_storage = LocalStorage()
        self.logger_instance = Logger()
        # recover data from hard storage
        self.global_data_store.set_shard_list_if_not_empty(self.local_storage.load(self.filename_prefix))
        last_saved_time = self.local_storage.get_last_saved_time()
        command_list = self.logger_instance.get_commands_after_time(last_saved_time)
        self.command_runner.execute_all(command_list)
        self.persistBehaviour = PersistAtTimeBehaviour(self.global_data_store,self.local_storage,start_at_time,interval_in_seconds=30,filename_prefix=self.filename_prefix)
        pass

    def process_serialized(self, bytes_form: bytes):
        deserialized = Deserializer().deserialize(bytes_form.decode("utf-8"))
        return self.command_runner.run(deserialized)

