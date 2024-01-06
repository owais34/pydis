from time import time,strftime,gmtime,sleep,asctime,localtime
import threading
import os
import json
import glob
from ..utils.util_classes import singleton

@singleton
class StorageService():
    def __init__(self) -> None:
        self.run_storage_service = True
    
    def stop(self):
        self.run_storage_service = False


STORAGE_SERVICE = StorageService()

@singleton
class LocalStorage():
    def __init__(self) -> None:
        self.path=os.path.join(os.getcwd(),"DATA_STORE")
        try:
            os.mkdir(self.path)
        except:
            print("Persist Directory already exists")
        pass

    def save(self, filename: str, content: any):
        print("Started Save job for file "+filename+" at "+asctime())
        binary_content = json.dumps(content).encode("utf-8")
        fullpath = os.path.join(self.path, filename+".dat")
        with open(fullpath, "wb") as file:
            file.write(binary_content)
        mbs = len(binary_content)/1000000
        print("Finished Writing %f mb at %s"  %(mbs,asctime()))
        with open(os.path.join(self.path,"saved_at.txt"),"w") as timefile:
            timefile.write(str(time()))

    def load(self, filenamePrefix: str="shard"):
        content_list = []
        for filename in glob.glob(os.path.join(self.path, filenamePrefix + '*.dat')):
            with open(os.path.join(self.path, filename), 'rb') as f:
                content_list.append(json.load(f))
        
        return content_list
    
    def get_last_saved_time(self)-> float:
        try:
            with open(os.path.join(self.path, "saved_at.txt"), "r") as f:
                last_saved_time = float(f.read())
            return last_saved_time
        except:
            return 0


@singleton
class PersistAtTimeBehaviour():
    def __init__(self,datastore, storage: LocalStorage, start_at_time: str = "02:00:00", interval_in_seconds: int = 86400, filename_prefix: str = "shard") -> None:
        self.start_time = 0
        self.start_at_time = start_at_time
        self.interval_in_seconds = interval_in_seconds
        self.started_storing = False
        self.datastore = datastore
        self.storage = storage
        self.filename_prefix = filename_prefix
        self.t1 = threading.Thread(target=self.run)
        self.t1.start()
        pass


    def run(self):
        while STORAGE_SERVICE.run_storage_service:
            current_time = time()
            if self.start_time == 0 and strftime("%H:%M:%S", localtime(current_time)) == self.start_at_time:
                self.start_time = current_time
            if (int(current_time)-int(self.start_time))%self.interval_in_seconds == 0 and self.started_storing==False:
                self.started_storing=True
                i=1
                for shard in self.datastore.shard_list:
                    self.storage.save(self.filename_prefix+str(i), shard)
                sleep(1)
                self.started_storing = False










