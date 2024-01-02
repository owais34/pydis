from ..utils.util_classes import singleton
from time import strftime,localtime,time
import os
import glob

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
        filename = "LOG-"+strftime("%Y-%b-%d.dat", 
             localtime(time()))
        fullpath = os.path.join(self.path,filename)
        with open(fullpath, "a") as file:
            file.write(bytes(str(time())+">"+command+"\r\n","utf-8"))

    def get_commands_after_time(self, time : float):
        log_files_list = []
        command_list = []
        input_date = strftime("%Y-%b-%d.dat", localtime(time))
        for filename in glob.glob(os.path.join(self.path, 'LOG-*.dat')):
            log_files_list.append(os.path.join(self.path,filename))
        log_files_list = sorted(log_files_list)
        for filename in log_files_list:
            with open(filename,"r","utf-8",newline="\r\n") as logfile:
                date_of_file = filename.split("-")[-1][:-4]
                if date_of_file>=input_date:
                    for line in logfile:
                        line_components = str(line).split(">",1)
                        if float(line_components[0])>time:
                            command_list.append(line_components[1])
        
        return command_list

