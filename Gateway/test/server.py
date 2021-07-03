import sys
import time
import signal
import threading

from threading import Thread
from jsonrpcserver import methods

class KThread(Thread):
    def __init__(self, *args, **keywords):
        super(KThread, self).__init__(*args, **keywords)
        self.killed = False

    def start(self):
        self.__brun = self.run
        self.run = self.__run # Force the Thread to install our trace.
        Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__brun()
        self.run = self.__brun

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        return None

    def localtrace(self, frame, why, arg):
        if self.killed and why == 'line':
            raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

class Test(object):
    def __init__(self):
        methods.add(self.ping)
        methods.add(self.getNextProjects)
        methods.add(self.getProjects)
        methods.add(self.getProject)

    def ping(self):
        return "pong"

    def getNextProjects(self, num):
        prjs = []
        for i in range(1, num+1):
            prjs.append({"uid":i, "name":"test1", "duration":10000, "state":"READY", "rank":i%3+1})
        return prjs

    def getProjects(self):
        prj1 = {"uid":1, "name":"test1", "duration":10000, "state":"READY", "rank":1}
        prj2 = {"uid":2, "name":"test1", "duration":60000, "state":"READY", "rank":3}
        return [prj1, prj2]

    def getProject(self, uid):
        prj1 = {"uid":uid, "name":"test1", "duration":10000, "state":"READY", "rank":1}
        return prj1

def start():
    methods.serve_forever()

if __name__ == "__main__":
    t = Test()
    x = KThread(target=start)
    x.start()
    def signal_handler(sig, frame):
        x.kill()
    signal.signal(signal.SIGINT, signal_handler)
    x.join()
