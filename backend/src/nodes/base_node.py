from src.message import Message
from src.nodes.node_manager import NodeManager
from src.nodes.node_manager import nodes as NODE_LIST
from api import logger, exception

NODE_TYPE = "BASE_NODE"

class BaseNode:
    """
    A class that represents a node, and its properties.

    Attributes:
        name (str): The name of the node.
        type (str): The type of the node.
        id (str): The id of the node.
        options (dict): The options of the node.
        outputConnections (list): The output connections of the node.
    
    Methods:
        onSuccess(payload, additional): Sends a success message to the node.
        onSignal(signal): Sends a signal message to the node.
        onFailure(payload, additional): Sends a failure message to the node.
        on(trigger, payload, additional): Sends a message to the node.
        pause(): Pauses the node.
        resume(): Resumes the node.
        stop(): Stops the node.
        reset(): Resets the node.
        pulse(color): Pulses the node.
        sendConnectionExec(fromId, toId): Sends a connection execution message to the node.
        sendErrorMessage(nodeId, errorMessage): Sends an error message to the node.

        log(message, level="debug", prefix="", suffix=""): Logs a message.


    """
    
    @exception(logger)
    def __init__(self, name, type, id, options, outputConnections) -> None:
        self.name = name
        self.type = type
        self._id = id
        self.options = options
        self.outputConnections = outputConnections
        self.running = True

    @exception(logger)
    def onSuccess(self, payload, additional=None):
        self.on("onSuccess", payload, additional)
    
    @exception(logger)
    def onSignal(self, signal=True):
        self.on("Sinal", signal)
    
    @exception(logger)
    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        self.on("onFailure", payload, additional, pulse)
    
    @exception(logger)
    def on(self, trigger, payload, additional=None, pulse=False, errorMessage=""):
        targets = list(
            filter(
                lambda connection: connection.get("from").get("name") == trigger,
                self.outputConnections,
            )
        )
        if pulse:
            self.sendErrorMessage(self._id, errorMessage)
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
                #print(f'Trigger: {target.get("to").get("nodeId")}, message: {message}')
                #print(target.get("to").get("nodeId"))
                node_ro_run = NodeManager.getNodeById(target.get("to").get("nodeId"))
                node_ro_run.execute(message)
            except Exception as e:
                print(e)
                self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))

    @exception(logger)
    def AutoRun(self):
        message = Message(
                "auto_run",
                "auto_run",
                "auto_run",
                "auto_run",
                "auto_run",
                "auto_run",
                "auto_run"
            )
        NodeManager.getNodeById(self._id).execute(message)
        
    @exception(logger)
    def pause(self):
        self.running = False
        return True

    @exception(logger)
    def resume(self):
        self.running = True
        return True

    @exception(logger)
    def stop(self):
        return False
    
    @exception(logger)
    def reset(self):
        return False

    @exception(logger)
    def pulse(self, color):
        message = {"NodeId": self._id, "color": color}
    
    @exception(logger)
    def sendConnectionExec(self, fromId, toId):
        message = {"type": "CONNECTION_EXEC", "data": {"from": fromId, "to": toId}}
    
    @exception(logger)
    def sendErrorMessage(self, nodeId, errorMessage):
        message = {
            "type": "NODE_EXEC_ERROR",
            "data": {"nodeId": nodeId, "errorMessage": errorMessage},
        }

#    @staticmethod
    def  __str__(self) -> str:
        return f"[{self._id}] ({self.type}) {self.name}"