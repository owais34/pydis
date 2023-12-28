import subprocess
import sys

# command_option = sys.argv[1]

# def createVirtualEnvironment():
#     try:
#         subprocess.run("python3 -m venv venv")
#     except Exception as e:
#         print(e)
#         print("trying with python version < 3")
#         try:
#             subprocess.run("python -m venv venv")
#             return True
#         except Exception as e2:
#             print(e2)
#             return False
#     return True

# def activateVirtualEnvironment():
#     try:
#         if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
#             subprocess.run("source env/bin/activate")
#         elif sys.platform.startswith("win32"):
#             subprocess.run(".\venv\Scripts\Activate.ps1")
#     except Exception as e:
#         print(e)
#         return False
#     return True


# def installDependencies():
#     subprocess.run("pip install -r requirements.txt")
#     return True


# def runTests():
#     subprocess.run("pytest")
#     return True



# if command_option == "install":
#     result = installDependencies() and runTests()
# elif command_option == "test":
#     runTests()
# else:
#     print("please use option install or test >> py pipeline.py install or py pieline.py test")
    

if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    subprocess.run("bash pipeline.sh")
elif sys.platform.startswith("win32"):
    p = subprocess.Popen(["powershell.exe","-ExecutionPolicy", "RemoteSigned", "-file",
              sys.path[0] +"\\pipeline.ps1"], 
              stdout=sys.stdout)
    p.communicate()
