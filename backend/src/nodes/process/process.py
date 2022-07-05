from datetime import datetime
import threading
from bson import ObjectId
from src.nodes.node_manager import NodeManager
from src.nodes.alerts.alert_obj import Alert
from api import logger, exception
from api.decorators import for_all_methods
from src.loader import load as load_conf
from src.nodes.base_node import event_list
from codetiming import Timer
from src.end_points import Process as WebProcess
from threading import Thread
import asyncio
from .target import targets, target

class Process(threading.Thread):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    LOADING = "LOADING"
    LOADED = "LOADED"

    def __init__(self, target, *args, **kwargs) -> None:
        threading.Thread.__init__(self)
        self._id = ObjectId()
        self.status = Process.STOPPED
        self.errors = []
        self.format = "%m/%d/%y %H:%M:%S"
        Timer.timers.clear()
        self.start_time = None
        self.stop_time = None
        self.runningTimer = Timer("Running")
        self.pausedTimer = Timer("Paused")
        self.stopped = threading.Event()
        self.paused = threading.Event()
        self.resumed = threading.Event()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.__status = {
            "_id": str(self._id),
            "status": self.status,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "run_time": Timer.timers.get("Running", 0),
            "pause_time": Timer.timers.get("Paused", 0),
            "total_time": Timer.timers.get("Running", 0) + Timer.timers.get("Paused", 0),
        }

    def run(self):
        while not self.stopped.is_set():
            while self.paused.is_set():
                logger.info("Process Paused - loop_info")
                self.resumed.wait()
                logger.info("Process Resumed - loop_info")
                self.resumed.clear()
            if not self.stopped.is_set() and not self.paused.is_set():
                self.target(*self.args, **self.kwargs)
                event_list.join()
                logger.info("Process END [reseting] - loop_info")
        logger.info("Process Thread Stopped - Normally")

    def start(self):
        logger.info("Process Started")
        self.status = Process.RUNNING
        self.runningTimer.start()
        self.start_time = datetime.now()
        super().start()

    def resume(self):
        self.paused.clear()
        self.resumed.set()
        self.pausedTimer.stop()
        logger.info("Process Resumed")
        self.status = Process.RUNNING

    def pause(self):
        self.paused.set()
        self.pausedTimer.start()
        logger.info("Process Paused")
        self.status = Process.PAUSED

    def stop(self, wait=True):
        self.stopped.set()
        self.resume()
        logger.info("Process Stopped")
        self.status = Process.STOPPED
        if wait:
            self.join(5)
        try:
            self.runningTimer.stop()
        except Exception:
            pass
        self.stop_time = datetime.now()

    def is_paused(self):
        return self.paused.is_set()

    def is_stopped(self):
        return self.stopped.is_set()

    def is_running(self):
        return not (self.is_stopped() or self.is_paused())

    @property
    def status_rtc(self):
        self.__status["_id"]=str(self._id)
        self.__status["status"]=self.status
        self.__status["start_time"]=self.start_time
        self.__status["stop_time"]=self.stop_time
        self.__status["run_time"]=Timer.timers.get("Running", 0)
        self.__status["pause_time"]=Timer.timers.get("Paused", 0)
        self.__status["total_time"]=Timer.timers.get("Running", 0) + Timer.timers.get("Paused", 0)
        return self.__status


@for_all_methods(exception(logger))
class sample_process():
    def __init__(self, *args, **kwargs) -> None:
        self.loaded_id = None
        self.st = NodeManager.start
        self.args = args
        self.kwargs = kwargs
        self._id = ObjectId("62b225701766eeeff3966337")
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.daemon = True
        self.websocket = WebProcess(self._id, self.status)
        Thread(
            target=self.auto_update, name=f"{self._id}_auto_update", daemon=True
        ).start()
        self.targets = targets.values

    @property
    def status(self):
        return self.process.status_rtc

    def auto_update(self):
        asyncio.run(self.websocket.broadcast_on_change(self.status))

    def load(self, _id=None):
        if self.status.get("status", False):
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

    def start(self, _id=None, internal=False):
        self.load(_id)
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.start()
        if internal:
            Alert(
                "INFO", "Processo iniciado", "O processo foi iniciado automaticamente"
            )

    def pause(self, internal=False):
        NodeManager.pause()
        self.process.pause()
        if internal:
            Alert("INFO", "Processo em pausa", "O processo foi parado automaticamente")

    def resume(self, internal=False):
        NodeManager.resume()
        self.process.resume()
        if internal:
            Alert(
                "INFO",
                "Processo em execução",
                "O processo foi retomado automaticamente",
            )

    def stop(self, wait=True, internal=False):
        NodeManager.stop()
        self.process.stop(wait)
        if internal:
            Alert("INFO", "Processo parado", "O processo foi parado automaticamente")

    def is_paused(self):
        return self.process.is_paused()

    def is_running(self):
        return self.process.is_running()

    def is_stopped(self):
        return self.process.is_stopped()


process = sample_process()

if __name__ == "__main__":
    import math

    def fatorial_calculator(n):
        return math.factorial(n)

    example = Process(fatorial_calculator, 399999)
    example.start()
    example.stop()
