from concurrent.futures import thread
import threading
import krpc

class Connect:

    def __init__(self, Target, Args):
        self.RootThread = threading.Thread(target=Target, args = Args)
    def Run(self):
        self.RootThread.start()

    def Stop(self):
        print("NOT STOPED")