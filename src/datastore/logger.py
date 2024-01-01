from ..utils.util_classes import singleton
from time import strftime,gmtime,time
import os

@singleton
class Logger():
    def __init__(self) -> None:
        self.path=os.path.join(os.path.curdir,"LOGS")
        try:
            os.mkdir(self.path)
        except:
            print("Directory already exists")
        pass

    def capture(self, command: str) -> None:
        filename = "LOG-"+strftime("%d-%b-%Y.txt", 
             gmtime(time()))
        fullpath = os.path.join(self.path,filename)
        with open(fullpath, "a") as file:
            file.write(str(time())+">"+command+"\r\n")

    