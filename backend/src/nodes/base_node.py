from math import fabs
from cv2 import log
# from src.manager.socketio_manager import emit
from src.message import Message
from src.nodes.node_manager import NodeManager
from src.logs.log import logSetup
import logging
#from src.exec_info import ExecutionCounter

NODE_TYPE = "BASE_NODE"

class BaseNode:
    def __init__(self, name, type, id, options, outputConnections) -> None:
        self.name = name
        self.type = type
        self._id = id
        self.options = options
        self.outputConnections = outputConnections
        self.running = True
        self.logger = logSetup(__class__.__name__, alias=self.name, id=self._id, path=__name__)
        self.log("Created")
    def log(self, message, level="debug", prefix="", suffix=""):
        #if not prefix:
            #prefix = f"{self.type} {self.name} {self._id} \t"

        getattr(self.logger, level.lower())(f"{prefix}{message}{suffix}")

    def onSuccess(self, payload, additional=None):
        #ExecutionCounter.incrCountType(self._id, "success")
        self.on("onSuccess", payload, additional)

    def onSignal(self, signal=True):
        self.on("Sinal", signal)

    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        #ExecutionCounter.incrCountType(self._id, "failure")
        self.log(f"onFailure: {payload}", level="warning")
        self.on("onFailure", payload, additional, pulse)

    def on(self, trigger, payload, additional=None, pulse=False, errorMessage=""):
        # filter targets from outputConnections using intrf.from.name == trigger

        targets = list(
            filter(
                lambda connection: connection.get("from").get("name") == trigger,
                self.outputConnections,
            )
        )
        if pulse:
            self.sendErrorMessage(self._id, errorMessage)
        #if trigger == "onFailure":
            #ExecutionCounter.incrCountType(self._id, "failure")
        for target in targets:

            self.sendConnectionExec(
                target.get("from").get("id"), target.get("to").get("id")
            )
            message = Message(
                target.get("from").get("id"),
                target.get("to").get("id"),
                target.get("from").get("name"),
                target.get("to").get("name"),
                target.get("from").get("nodeId"),
                target.get("to").get("nodeId"),
                payload,
                additional,
            )
            while not self.running:
                pass
            try:
                if trigger != "onFailure":
                    self.log(f"Launch {message}", level="debug")
                NodeManager.getNodeById(target.get("to").get("nodeId")).execute(message)
            except AttributeError as e:
                self.log(f"Node {target.get('to').get('nodeId')} not found", level="warning")
                self.log(f"{e}", level="fatal")
                raise
                # print("to:",target.get("to"), "to_id:",target.get("to").get("nodeId"))

    def pause(self):
        self.log(f"Paused", level="debug")
        self.running = False
        return True

    def resume(self):
        self.log(f"Resumed", level="debug")
        self.running = True
        return True

    def stop(self):
        self.log(f"stop method not implemented for node type {self.type}", level="debug")
        return False

    def reset(self):
        self.log(f"reset method not implemented for node type {self.type}", level="debug")
        return False

    def pulse(self, color):
        message = {"NodeId": self._id, "color": color}
        # emit("NODE_PULSE", message)

    def sendConnectionExec(self, fromId, toId):
        message = {"type": "CONNECTION_EXEC", "data": {"from": fromId, "to": toId}}
        # emit("CONNECTION_EXEC", message)

    def sendErrorMessage(self, nodeId, errorMessage):
        message = {
            "type": "NODE_EXEC_ERROR",
            "data": {"nodeId": nodeId, "errorMessage": errorMessage},
        }
        # emit("NODE_EXEC_ERROR", message)
