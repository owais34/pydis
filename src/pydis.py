from .datastore.globaldata import GlobalDataStore,CommandRunner
from .datastore.persist import PersistAtTimeBehaviour, LocalStorage
from .utils.util_classes import singleton


start_at_time = "14:45:00" # get this from conf file

@singleton
class Pydis():
    def __init__(self) -> None:
        self.global_data_store = GlobalDataStore()
        self.filename_prefix = "shard"
        self.command_runner = CommandRunner(self.global_data_store)
        self.local_storage = LocalStorage()
        # recover data from hard storage
        self.global_data_store.set_shard_list_if_not_empty(self.local_storage.load(self.filename_prefix))
        self.last_saved_time = self.local_storage.get_last_saved_time()
        
        self.persistBehaviour = PersistAtTimeBehaviour(self.global_data_store,self.local_storage,start_at_time,self.filename_prefix)

        pass

