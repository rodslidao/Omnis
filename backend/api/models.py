from enum import Enum
from api import dbo
from bson.objectid import ObjectId
from datetime import datetime
from src.loader import loadConfig, LoadingMode
from src.nodes.node_manager import NodeManager
from src.nodes.timer.task_time import setInterval

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
        self.startTime = datetime.now()
        self.endTime = datetime.now()
        self.calculateRunningTime()
        self.status = Process.StatusCode.STOPPED
        self.errors = []
        self.format = "%m/%d/%y %H:%M:%S"

    def start(self):
        self.startTime = datetime.now()
        self.status = Process.StatusCode.RUNNING

    def stop(self):
        self.endTime = datetime.now()
        self.status = Process.StatusCode.STOPPED
        self.calculateRunningTime()
        self.calculateRunningTime.stop()

    def pause(self):
        self.status = Process.ProcessStatus.PAUSED

    def calculateRunningTime(self):
        #st = #datetime.strptime(self.startTime.strftime(self.format), self.format)
        #ed = #datetime.strptime(self.endTime.strftime(self.format), self.format)
        self.runningTime = (self.endTime - self.startTime).total_seconds()

    def __call__(self):
        return self.__dict__


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
        self.verifyChange()
        loadConfig(self.NodeSheet, LoadingMode.STARTUP)
        super().start()

    def stopProcess(self):
        NodeManager().stop()
        super().stop()

    def pauseProcess(self):
        NodeManager().pause()
        super().pause()

    def verifyChange(self):
        lt = dbo["last-values"].find_one({"query": "lastLoadedNoneSheet"})
        if lt["NodeSheetID"] != self.lt:
            print(lt["NodeSheetID"])
            self.NodeSheet = NodeSheet().getNodeSheetById(lt["NodeSheetID"])
            self.lt = lt["NodeSheetID"]
            return True
        return False
    
    def dict(self):
        return super().__call__()