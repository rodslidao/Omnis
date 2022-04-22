import threading
from bson import ObjectId
from src.nodes.node_manager import NodeManager
from src.nodes.timer.timer import Chronometer
from src.nodes.alerts.alert_obj import Alert
from api import logger, exception, for_all_methods


@for_all_methods(exception(logger))
class Process(threading.Thread):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    ERROR = "ERROR"

    def __init__(self, target, *args, **kwargs) -> None:
        threading.Thread.__init__(self)
        self._id = ObjectId()
        self.status = Process.STOPPED
        self.errors = []
        self.format = "%m/%d/%y %H:%M:%S"
        self.endTiming, self.startTiming = 0.0, 0.0
        self.stopped = threading.Event()
        self.paused = threading.Event()
        self.resumed = threading.Event()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while not self.stopped.is_set():
            while self.paused.is_set():
                self.resumed.wait()
                self.resumed.clear()
            if not self.stopped.is_set() and not self.paused.is_set():
                self.target(*self.args, **self.kwargs)
        logger.info("Process Thread Stopped")

    def start(self):
        logger.info("Process Started")
        self.status = Process.RUNNING
        self.Chronometer = Chronometer()
        self.startTiming = self.Chronometer.start().timestamp()
        super().start()

    def runningTime(self):
        try:
            return float(self.Chronometer.trigger().total_seconds())
        except AttributeError:
            return 0.0

    def resume(self):
        self.paused.clear()
        self.resumed.set()
        logger.info("Process Resumed")
        self.status = Process.RUNNING
        self.Chronometer.resume()

    def pause(self):
        self.paused.set()
        logger.info("Process Paused")
        self.status = Process.PAUSED
        self.Chronometer.pause()

    def stop(self, wait=True):
        self.stopped.set()
        self.resume()
        logger.info("Process Stopped")
        self.status = Process.STOPPED
        self.Chronometer.stop()
        self.endTiming = self.Chronometer.cron_End.timestamp()
        if wait:
            self.join()
            print(1/0)
        # Alert("INFO", "Process Stopped", str(self.getStatus()))

    def getStatus(self):
        return {
            "_id": str(self._id),
            "status": self.status,
            "errors": self.errors,
            "startTiming": self.startTiming,
            "endTiming": self.endTiming,
            "runningTime": self.runningTime(),
        }


from src.loader import load

@for_all_methods(exception(logger))
class sample_process():
    def __init__(self, *args, **kwargs) -> None:
        self.loaded_id = None
        self.st = NodeManager.start
        self.args = args
        self.kwargs = kwargs
        self.status = Process.STOPPED
        self.process = Process(self.st, *self.args, **self.kwargs)
        # print(1/0)

    def load(self, _id=None):
        if self.status == Process.STOPPED:
            load(_id)
            self.loaded_id = _id
            return True
        return False

    def getLoadedId(self):
        return self.loaded_id

    def start(self):
        if self.loaded_id is None:
            self.load()
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.start()
    
    def pause(self):
        NodeManager.pause()
        self.process.pause()

    def resume(self):
        NodeManager.resume()
        self.process.resume()

    def stop(self, wait=True):
        NodeManager.stop()
        self.process.stop(wait)

    def dict(self):
        return self.process.getStatus()

process = sample_process()

if __name__ == "__main__":

    import math

    def fatorial_calculator(n):
        return math.factorial(n)
    example = Process(fatorial_calculator, 399999)
    example.start()
    example.stop()