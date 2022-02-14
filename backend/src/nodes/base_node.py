from src.message import Message
from src.nodes.node_manager import NodeManager
from src.logs.log import logSetup

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

        getattr(self.logger, level.lower())(f"{prefix}{message}{suffix}")

    def onSuccess(self, payload, additional=None):
        self.on("onSuccess", payload, additional)

    def onSignal(self, signal=True):
        self.on("Sinal", signal)

    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        self.log(f"onFailure: {payload}", level="warning")
        self.on("onFailure", payload, additional, pulse)

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
                if trigger != "onFailure":
                    self.log(f"Launch {message}", level="debug")
                NodeManager.getNodeById(target.get("to").get("nodeId")).execute(message)
            except AttributeError as e:
                self.log(f"Node {target.get('to').get('nodeId')} not found", level="warning")
                self.log(f"{e}", level="fatal")
                raise

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

    def sendConnectionExec(self, fromId, toId):
        message = {"type": "CONNECTION_EXEC", "data": {"from": fromId, "to": toId}}

    def sendErrorMessage(self, nodeId, errorMessage):
        message = {
            "type": "NODE_EXEC_ERROR",
            "data": {"nodeId": nodeId, "errorMessage": errorMessage},
        }
