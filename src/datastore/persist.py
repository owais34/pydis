from time import time,strftime,gmtime,sleep,asctime,localtime
import threading
import os
import json


RUN_STORAGE_SERVICE = True

class LocalStorage():
    def __init__(self) -> None:
        self.path=os.path.join(os.path.curdir,"DATA_STORE")
        try:
            os.mkdir(self.path)
        except:
            print("Directory already exists")
        pass

    def save(self, filename: str, content: any):
        print("Stared Save job for file "+filename+" at "+asctime())
        binary_content = json.dumps(content).encode("utf-8")
        fullpath = os.path.join(self.path, filename+".dat")
        with open(fullpath, "wb") as file:
            file.write(binary_content)
        mbs = len(binary_content)/1000000
        print("Finished Writing %f mb at %s"  %(mbs,asctime()))
        



class PersistAtTimeBehaviour():
    def __init__(self,datastore, storage: LocalStorage, start_at_time: str = "02:00:00", interval_in_seconds: int = 86400) -> None:
        self.start_time = 0
        self.start_at_time = start_at_time
        self.interval_in_seconds = interval_in_seconds
        self.started_storing = False
        self.datastore = datastore
        self.storage = storage
        self.t1 = threading.Thread(target=self.run)
        self.t1.start()
        pass


    def run(self):
        while RUN_STORAGE_SERVICE:
            current_time = time()
            if self.start_time == 0 and strftime("%H:%M:%S", localtime(current_time)) == self.start_at_time:
                self.start_time = current_time
            if (int(current_time)-int(self.start_time))%self.interval_in_seconds == 0 and self.started_storing==False:
                self.started_storing=True
                i=1
                for shard in self.datastore.shard_list:
                    self.storage.save("shard"+str(i), shard)
                sleep(1)
                self.started_storing = False










