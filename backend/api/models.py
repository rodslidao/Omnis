from ast import Return
from enum import Enum
from api import dbo
from bson.objectid import ObjectId
from src.loader import loadConfig, LoadingMode
from src.nodes.node_manager import NodeManager
from src.nodes.timer.timer import Chronometer
from api import logger, exception
from os import popen

def defaultException(function):
    """Decorator to catch exceptions and return a payload with success=False and errors=exception message"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            payload = {"status": {"success": False, "errors": [str(error)]}}
            return payload

    return wrapper


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
        print("Starting process")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer = Chronometer()
        self.startTiming = self.Chronometer.start().timestamp()

    @exception(logger)
    def runningTime(self):
        if self.status == Process.StatusCode.RUNNING or self.status == Process.StatusCode.PAUSED:
            return float(self.Chronometer.trigger().total_seconds())
        else:
            return 0.0

    @exception(logger)
    def stop(self):
        print("Stopping process")
        self.status = Process.StatusCode.STOPPED
        self.Chronometer.stop()
        self.endTiming = self.Chronometer.cron_End.timestamp()

    @exception(logger)
    def resume(self):
        print("Resuming process")
        self.status = Process.StatusCode.RUNNING
        self.Chronometer.resume()

    @exception(logger)
    def pause(self):
        print("Pausing process")
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

class grok():
    @staticmethod
    def get_url():
        txt = (popen('curl -s localhost:4040/api/tunnels | jq ".tunnels[].public_url"').read()).replace('//', '')
        return list(map( lambda x: dict(zip(('protocol','uri','port'), x.split(':'))), list(filter(None, txt.split('"')))))


class NodeSheet:
    @exception(logger)
    def createNodeSheet(self, _id, **kwargs):
        """Create a new NodeSheet object"""
        dbo.insert_one("NodeSheets", {'_id': ObjectId(_id), **kwargs})
        return self.getNodeSheetById(kwargs.get("_id"))

    @exception(logger)
    def getNodeSheetById(self, _id):
        """Get a NodeSheet by id"""
        self.NodeSheet = dbo.find_one("NodeSheets", {"_id": ObjectId(_id)})
        return self._format()

    @exception(logger)
    def updateNodeSheet(self, _id, **kwargs):
        # kwargs["_id"] = ObjectId(kwargs["_id"])
        """Update a NodeSheet by id"""
        print("updatating", kwargs)
        dbo.update_one("NodeSheets", {"_id": ObjectId(_id)}, {"$set": kwargs})
        return self.getNodeSheetById(_id)

    @exception(logger)
    def deleteNodeSheet(self, _id):
        # kwargs["_id"] = ObjectId(kwargs["_id"])
        """Delete a NodeSheet by id"""
        deleted_sheet = self.getNodeSheetById(_id)
        dbo.delete_one("NodeSheets", {"_id": ObjectId(_id)})
        return deleted_sheet

    @exception(logger)
    def getSketchList(self):
        return dbo.find_many("NodeSheets",  data={'content':0})
        
    @exception(logger)
    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet


class LastValue:

    NodeSheet = {"query": "lastLoadedNoneSheet"}

    @exception(logger)
    def loadConfig(node_id):
        """Load the last value of a node"""
        LastValue.setLastValue(LastValue.NodeSheet, {"NodeSheetID": node_id})

    @exception(logger)
    def getLoadedConfig():
        return LastValue.getLastValue(LastValue.NodeSheet)["NodeSheetID"]

    @exception(logger)
    def getLastValue(query):
        """Get the last value of a node"""
        return dbo.find_one("last-values", query)

    @exception(logger)
    def setLastValue(query, value):
        """Set the last value of a node"""
        dbo.update_one("last-values", query, {"$set": value})


class ProcessManager(Process):
    @exception(logger)
    def __init__(self, differ=None) -> None:
        super().__init__()
        self.lt = None

    @exception(logger)
    def isAnyOfStatus(self, *status):
        return any([self.status == st for st in status])

    @exception(logger)
    def startProcess(self):
        if self.isAnyOfStatus(Process.StatusCode.STOPPED):
            loadConfig(self.verifyChange(), LoadingMode.STARTUP)
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
        lt = dbo.find_one("last-values", {"query": "lastLoadedNoneSheet"})
        if lt["NodeSheetID"] != self.lt:
            print(lt["NodeSheetID"])
            self.lt = lt["NodeSheetID"]
        return NodeSheet().getNodeSheetById(self.lt)

    @exception(logger)
    def dict(self):
        return super().__call__()


process = ProcessManager()
