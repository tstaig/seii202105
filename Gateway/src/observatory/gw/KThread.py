import sys

from threading import Thread

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
