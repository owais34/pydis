from ..utils.util_classes import singleton
from time import strftime,localtime,time
import os
import glob
from collections import deque
import threading
import json

@singleton
class LoggerService():
    def __init__(self) -> None:
        self.run_logger_service = True
    
    def stop(self):
        self.run_logger_service = False

LOGGER_SERVICE = LoggerService()

@singleton
class Logger():
    def __init__(self) -> None:
        self.path=os.path.join(os.getcwd(),"LOGS")
        try:
            os.mkdir(self.path)
        except:
            print("Logger Directory already exists")
        self.command_queue = deque()
        self.t1 = threading.Thread(target=self.run)
        self.t1.start()

    def run(self):
        while True and LOGGER_SERVICE.run_logger_service:
            if len(self.command_queue)>0:
                command = self.command_queue.popleft()
                filename = "LOG-"+strftime("%Y-%b-%d.dat", localtime(time()))
                fullpath = os.path.join(self.path,filename)
                with open(fullpath, "ab") as file:
                    file.write(bytes(str(command["time"])+">"+command["cmd"]+"\r\n","utf-8"))



    def capture(self, command: str, time_in_s : time) -> None:
        self.command_queue.append({"cmd": command,"time":time_in_s})

    def get_commands_after_time(self, time : float):
        log_files_list = []
        command_list = []
        input_date = strftime("%Y-%b-%d.dat", localtime(time))
        for filename in glob.glob(os.path.join(self.path, 'LOG-*.dat')):
            log_files_list.append(os.path.join(self.path,filename))
        log_files_list = sorted(log_files_list)
        for filename in log_files_list:
            with open(filename,"r",encoding="utf-8",newline="\r\n") as logfile:
                date_of_file = filename.split("-")[-1][:-4]
                if date_of_file>=input_date:
                    for line in logfile:
                        time_cmd = line.split(">",1)
                        if float(time_cmd[0])>time:
                                command_list.append(json.load(time_cmd[1]))        
        return command_list

