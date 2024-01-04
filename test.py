import requests
import threading
import string
import random
import time

class Test():
    def __init__(self) -> None:
        self.t1 = threading.Thread(target=self.run)
        self.counter = 1
        self.t1.start()
        

    def run(self):
        while True:
            key = "word"+str(self.counter)
            bytes_input = b"*3\r\n+" + bytes(key, "utf-8") + b"\r\n+" + bytes( ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10)), "utf-8") + b"\r\n"
            requests.post("http://127.0.0.1:8000/", data=bytes_input)
            self.counter+=1
            time.sleep(0.02)


test = Test()