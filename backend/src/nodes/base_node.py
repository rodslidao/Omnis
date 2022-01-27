from src.manager.socketio_manager import emit
from src.message import Message
from src.nodes.node_manager import NodeManager
#from src.exec_info import ExecutionCounter

NODE_TYPE = "BASE_NODE"

class BaseNode:
    def __init__(self, name, type, id, options, outputConnections) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.options = options
        self.outputConnections = outputConnections
        self.running = True

    def onSuccess(self, payload, additional=None):
        #ExecutionCounter.incrCountType(self.id, "success")
        self.on("onSuccess", payload, additional)

    def onSignal(self, signal=True):
        self.on("Sinal", signal)

    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        #ExecutionCounter.incrCountType(self.id, "failure")
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
            self.sendErrorMessage(self.id, errorMessage)
        #if trigger == "onFailure":
            #ExecutionCounter.incrCountType(self.id, "failure")
        for target in targets:
            self.sendConnectionExec(
                target.get("from").get("id"), target.get("to").get("id")
            )
            message = Message(
                target.get("from").get("id"),
                target.get("to").get("id"),
                target.get("from").get("name"),
                target.get("to").get("name"),
                self.id,
                target.get("from").get("nodeId"),
                payload,
                additional,
            )
            while not self.running:
                pass
            try:
                NodeManager.getNodeById(target.get("to").get("nodeId")).execute(message)
            except AttributeError:
                print("to:",target.get("to"), "to_id:",target.get("to").get("nodeId"))

    def pause(self):
        self.running = False
        return True

    def resume(self):
        self.running = True
        return True

    def stop(self):
        print("stop method not implemented for node type", self.type)
        return False

    def reset(self):
        print("reset method not implemented for node type", self.type)
        return False

    def pulse(self, color):
        message = {"NodeId": self.id, "color": color}
        emit("NODE_PULSE", message)

    def sendConnectionExec(self, fromId, toId):
        message = {"type": "CONNECTION_EXEC", "data": {"from": fromId, "to": toId}}
        emit("CONNECTION_EXEC", message)

    def sendErrorMessage(self, nodeId, errorMessage):
        message = {
            "type": "NODE_EXEC_ERROR",
            "data": {"nodeId": nodeId, "errorMessage": errorMessage},
        }
        emit("NODE_EXEC_ERROR", message)
