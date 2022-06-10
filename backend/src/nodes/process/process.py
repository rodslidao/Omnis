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
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while not self.stopped.is_set():
            while self.paused.is_set():
                logger.info("Process Paused - loop_info")
                self.resumed.wait()
                logger.info("Process Resumed - loop_info")
                self.resumed.clear()
        # for i in range(2):
            if not self.stopped.is_set() and not self.paused.is_set():
                self.target(*self.args, **self.kwargs)
                self.wait_process_end()
                logger.info("Process END [reseting] - loop_info")
        logger.info("Process Thread Stopped - Normally")


    def wait_process_end(self):
        while len(event_list) > 0:
            
            item = list(event_list.items())[-1]
            item[1].wait()
            event_list.pop(item[0])
            
            # espere até que todos os eventos sejam executados, e então os remova da lista
            # for event in event_list.values():
            #     event.wait()
            # event_list.clear()



        
    def start(self):
        logger.info("Process Started")
        self.status = Process.RUNNING
        # self.Chronometer = Chronometer()
        # self.startTiming = self.Chronometer.start().timestamp()
        super().start()

    # def runningTime(self):
    #     try:
    #         return float(self.Chronometer.trigger().total_seconds())
    #     except AttributeError:
    #         return 0.0

    def resume(self):
        self.paused.clear()
        self.resumed.set()
        logger.info("Process Resumed")
        self.status = Process.RUNNING
        # getattr(self, "Chronometer", Chronometer()).resume()

    def pause(self):
        self.paused.set()
        logger.info("Process Paused")
        self.status = Process.PAUSED
        # getattr(self, "Chronometer", Chronometer()).pause()

    def stop(self, wait=True):
        self.stopped.set()
        self.resume()
        logger.info("Process Stopped")
        self.status = Process.STOPPED
        # getattr(self, "Chronometer", Chronometer()).stop()
        # self.endTiming = self.Chronometer.cron_End.timestamp()
        if wait: self.join()
        # Alert("INFO", "Process Stopped", str(self.getStatus()))

    def is_paused(self):
        return self.paused.is_set()

    def is_stopped(self):
        return self.stopped.is_set()

    def is_running(self):
        return not (self.is_stopped() or self.is_paused())

    
    
    def getStatus(self):
        return {
            "_id": str(self._id),
            "status": self.status,
            "errors": self.errors,
            "startTiming": 0.0, #self.startTiming,
            "endTiming": 0.0, #self.endTiming,
            "runningTime": 0.0, #self.runningTime(),
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

    def start(self, _id=None, internal=False):
        # if self.loaded_id is None:
        self.process.stop(False)
        self.load(_id)
        self.process = Process(self.st, *self.args, **self.kwargs)
        self.process.start()
        if internal:
            Alert("INFO", "Processo iniciado", "O processo foi iniciado automaticamente")
        


    def pause(self, internal=False):
        NodeManager.pause()
        self.process.pause()
        if internal:
            Alert("INFO", "Processo em pausa", "O processo foi parado automaticamente")

    def resume(self, internal=False):
        NodeManager.resume()
        self.process.resume()
        if internal:
            Alert("INFO", "Processo em execução", "O processo foi retomado automaticamente")

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
