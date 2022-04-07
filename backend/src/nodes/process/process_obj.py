from src.loader import loadConfig, LoadingMode
from src.nodes.node_manager import NodeManager
from src.loader import load
from src.nodes.timer.timer import Chronometer
from bson.objectid import ObjectId
from api import logger, exception
from api import dbo
from enum import Enum
from api.models import NodeSheet
from threading import Event
import threading
from time import sleep
from os import popen

external_stop_event = Event()

class Process:
    class StatusCode(Enum):
        RUNNING = "RUNNING"
        STOPPED = "STOPPED"
        PAUSED = "PAUSED"
        ERROR = "ERROR"

    @exception(logger)
    def __init__(self) -> None:
        self._id = ObjectId()
        self.status = Process.StatusCode.STOPPED
        self.errors = []
        self.format = "%m/%d/%y %H:%M:%S"
        self.endTiming, self.startTiming = 0.0, 0.0

    @exception(logger)
    def start(self):
        print("Process Started")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer = Chronometer()
        self.startTiming = self.Chronometer.start().timestamp()
        external_stop_event.clear()

    @exception(logger)
    def runningTime(self):
        #if self.status == Process.StatusCode.RUNNING or self.status == Process.StatusCode.PAUSED:
        try:
            return float(self.Chronometer.trigger().total_seconds())
        except AttributeError:
            return 0.0
            
        #else:

    @exception(logger)
    def stop(self):
        print("Process Stopped")
        self.status = Process.StatusCode.STOPPED
        self.Chronometer.stop()
        self.endTiming = self.Chronometer.cron_End.timestamp()
        external_stop_event.set()

    @exception(logger)
    def resume(self):
        print("Process Resumed")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer.resume()

    @exception(logger)
    def pause(self):
        print("Process Paused")
        self.status = Process.StatusCode.PAUSED
        self.Chronometer.pause()

    @exception(logger)
    def __call__(self):
        return {
            "_id": str(self._id),
            "running_seconds": self.runningTime(),
            "end_at": float(self.endTiming),
            "start_at": float(self.startTiming),
            "status": self.status.value,
        }

class ProcessManager(Process):
    @exception(logger)
    def __init__(self, differ=None) -> None:
        super().__init__()
        self.lt = None
        self.config_loaded = False

    @exception(logger)
    def isAnyOfStatus(self, *status):
        return any([self.status == st for st in status])

    @exception(logger)
    def loadingProcess(self, load_id=None):
        if self.isAnyOfStatus(Process.StatusCode.STOPPED):
            NodeManager.clear()
            load(load_id)
            self.config_loaded = True
            return True
        return False

    def keep_running(self):
        while not external_stop_event.isSet():
            th = threading.Thread(name="StartProcess", target=NodeManager.start)
            th.start()
            print("NEW CICLE STARTED...")
            th.join()

    @exception(logger)
    def startProcess(self):
        if not self.config_loaded:
            self.loadingProcess()

        if self.isAnyOfStatus(Process.StatusCode.STOPPED):
            threading.Thread(name="KeepRunning", target=self.keep_running).start()
            super().start()
            return True
        return False
        
    @exception(logger)
    def stopProcess(self):
        if self.isAnyOfStatus(Process.StatusCode.RUNNING, Process.StatusCode.PAUSED):
            NodeManager.stop()
            super().stop()
            return True
        return False

    @exception(logger)
    def pauseProcess(self):
        if self.isAnyOfStatus(Process.StatusCode.RUNNING):
            NodeManager.pause()
            super().pause()
            return True
        return False

    @exception(logger)
    def resumeProcess(self):
        if self.isAnyOfStatus(Process.StatusCode.PAUSED):
            NodeManager.resume()
            super().resume()
            return True
        return 
        

    @exception(logger)
    def verifyChange(self):
        lt = dbo.find_one("last-values", {"description":"current-config-loaded-id"})
        if lt["sheet-id"] != self.lt:
            print(lt["sheet-id"])
            self.lt = lt["sheet-id"]
        return NodeSheet().getNodeSheetById(self.lt)["content"]

    @exception(logger)
    def dict(self):
        return super().__call__()

process = ProcessManager()
