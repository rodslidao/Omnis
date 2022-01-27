from enum import Enum
from api import dbo
from bson.objectid import ObjectId
from datetime import datetime
from src.nodes.timer.task_time import setInterval
from src.loader import loadConfig, LoadingMode
from src.nodes.node_manager import NodeManager
from src.nodes.timer.timer import Chronometer

def defaultException(function):
    """Decorator to catch exceptions and return a payload with success=False and errors=exception message"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            payload = {"success": False, "errors": [str(error)]}
            return payload

    return wrapper


class Process:
    class StatusCode(Enum):
        RUNNING = "RUNNING"
        STOPPED = "STOPPED"
        PAUSED = "PAUSED"
        ERROR = "ERROR"

    def __init__(self) -> None:
        self._id = ObjectId()
        self.status = Process.StatusCode.STOPPED
        self.errors = []
        self.format = "%m/%d/%y %H:%M:%S"
        self.endTiming , self.startTiming = 0.0, 0.0

    def start(self):
        print("Starting process")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer = Chronometer()
        self.startTiming = self.Chronometer.start().timestamp()
    
    def runningTime(self):
        return float(self.Chronometer.trigger().total_seconds())

    def stop(self):
        print("Stopping process")
        self.status = Process.StatusCode.STOPPED
        self.Chronometer.stop()
        self.endTiming = self.Chronometer.cron_End.timestamp()

    def resume(self):
        print("Resuming process")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer.resume()

    def pause(self):
        print("Pausing process")
        self.status = Process.StatusCode.PAUSED
        self.Chronometer.pause()

    def __call__(self):
        return {"_id": str(self._id), "running_seconds": self.runningTime(), "end_at": float(self.endTiming), "start_at": float(self.startTiming)}


class NodeSheet:
    def createNodeSheet(self, **kwargs):
        """Create a new NodeSheet object"""
        _id = ObjectId()
        dbo.NodeSheets.insert_one({"_id": _id, **kwargs})
        return self.getNodeSheetById(_id)

    def getNodeSheetById(self, id):
        """Get a NodeSheet by id"""
        self.NodeSheet = dbo.NodeSheets.find_one({"_id": ObjectId(id)})
        return self._format()

    def updateNodeSheet(self, id, **kwargs):
        """Update a NodeSheet by id"""
        dbo.NodeSheets.update_one({"_id": ObjectId(id)}, {"$set": kwargs})
        return self.getNodeSheetById(id)

    def deleteNodeSheet(self, id):
        """Delete a NodeSheet by id"""
        deleted_sheet = self.getNodeSheetById(id)
        dbo.NodeSheets.delete_one({"_id": ObjectId(id)})
        return deleted_sheet

    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet


class ProcessManager(Process):
    def __init__(self, differ=None) -> None:
        super().__init__()
        self.lt = None

    def startProcess(self):
        loadConfig(self.verifyChange(), LoadingMode.STARTUP)
        super().start()

    def stopProcess(self):
        NodeManager.stop()
        super().stop()

    def pauseProcess(self):
        NodeManager.pause()
        super().pause()

    def resumeProcess(self):
        NodeManager.resume()
        super().resume()
    
    def verifyChange(self):
        lt = dbo["last-values"].find_one({"query": "lastLoadedNoneSheet"})
        if lt["NodeSheetID"] != self.lt:
            print(lt["NodeSheetID"])
            self.lt = lt["NodeSheetID"]
        return NodeSheet().getNodeSheetById(self.lt)
    
    def dict(self):
        return super().__call__()