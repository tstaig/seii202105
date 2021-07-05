import threading

class RecurrentJob(threading.Thread):
    def __init__(self, interval, execute):
        threading.Thread.__init__(self)
        self._stopped = threading.Event()
        self._interval = interval
        self._execute = execute
        
    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute()
