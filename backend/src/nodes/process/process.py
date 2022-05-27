from ast import Try
import imp
import threading
from time import sleep
from bson import ObjectId
from src.nodes.node_manager import NodeManager
from src.nodes.timer.timer import Chronometer
from src.nodes.alerts.alert_obj import Alert
from api import logger, exception
from api.decorators import for_all_methods
from src.loader import load as load_conf
from src.nodes.base_node import event_list

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
        self.reboot = threading.Event()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while not self.stopped.is_set():
            self.reboot.clear()
            while self.paused.is_set():
                logger.info("Process Paused - loop_info")
                self.resumed.wait()
                logger.info("Process Resumed - loop_info")
                self.resumed.clear()
        # for i in range(2):
            if not self.stopped.is_set() and not self.paused.is_set():
                self.target(*self.args, **self.kwargs)
                self.verify()
                logger.info("Wait for reboot - loop_info")
                self.reboot.wait()
                logger.info("Process END [reseting] - loop_info")
        logger.info("Process Thread Stopped - Normally")


    def verify(self, l=0):
        logger.info("Process Verifying")
        sleep(0.1)
        for key, val in list(event_list.items()):
            val.wait(5)
            event_list.pop(key)

        if len(event_list) != l:
            self.verify(len(event_list))
        self.reboot.set()
        logger.info("Process Verified")
        
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


@for_all_methods(exception(logger))
class sample_process:
    def __init__(self, *args, **kwargs) -> None:
        self.loaded_id = None
        self.st = NodeManager.start
        self.args = args
        self.kwargs = kwargs
        self.status = Process.STOPPED
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.daemon = True

    def load(self, _id=None):
        if self.status == Process.STOPPED:
            self.unload()
            a = load_conf(_id)
            if a:
                self.loaded_id = _id
            else:
                self.loaded_id = None
                self.unload()
            return a
        return False

    def unload(self):
        if self.loaded_id is not None:
            NodeManager.stop()
            NodeManager.clear()
            self.loaded_id = None
            return True
        return False

    def getLoadedId(self):
        return self.loaded_id

    def start(self):
        if self.loaded_id is None:
            self.load()
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.start()
        #Alert("INFO", "Process Started", str(self.process.getStatus()))


    def pause(self):
        NodeManager.pause()
        self.process.pause()
        #Alert("INFO", "Process Paused", str(self.process.getStatus()))

    def resume(self):
        NodeManager.resume()
        self.process.resume()
        #Alert("INFO", "Process Resumed", str(self.process.getStatus()))

    def stop(self, wait=True):
        NodeManager.stop()
        self.process.stop(wait)
        #Alert("INFO", "Process Stopped", str(self.process.getStatus()))

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
