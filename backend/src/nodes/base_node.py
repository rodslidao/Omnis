from src.message import Message
from src.nodes.node_manager import NodeManager
from api import logger, exception
from api.decorators import for_all_methods
from threading import Event

from threading import Thread
NODE_TYPE = "BASE_NODE"


@for_all_methods(exception(logger))
class BaseNode:
    """
    A class that represents a node, and its properties.

    Attributes:
        name (str): The name of the node.
        type (str): The type of the node.
        id (str): The id of the node.
        options (dict): The options of the node.
        output_connections (list): The output connections of the node.

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
        sendConnectionExec(fromId, toId):
        Sends a connection execution message to the node.
        sendErrorMessage(nodeId, errorMessage): Sends an error message to the node.

    """

    def __init__(self, name, type, id, options, output_connections) -> None:
        self.name = name
        self.type = type
        self._id = id
        self.options = options
        self.output_connections = output_connections
        self.running = True
        self.stop_event = Event()

    def onSuccess(self, payload, additional=None):
        self.on("onSuccess", payload, additional)

    def onSignal(self, signal=True):
        self.on("Sinal", signal)

    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        self.on("onFailure", payload, additional, pulse)

    def on(self, trigger, payload, additional=None, pulse=False, errorMessage=""):
        targets = list(
            filter(
                lambda connection: connection.get("from").get("name") == trigger,
                self.output_connections,
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
            # logger.info(f"{self}({message.sourceName}) -> {message}")
            node_ro_run = NodeManager.getNodeById(target.get("to").get("nodeId"))
            # try:
            Thread(target=node_ro_run.execute, args=(message,), name=f"{str(self)}({message.sourceName}) -> {message}", daemon=True).start()
            # T.join()
            # except Exception as e:
            #     logger.error(f"{node_ro_run}({message.targetName}) -> {e}")
            #     return False

    def AutoRun(self):
        message = Message(
            "auto_run",
            "auto_run",
            "auto_run",
            "auto_run",
            "auto_run",
            "auto_run",
            "auto_run",
        )
        self.reset()
        self.execute(message)

    def pause(self):
        self.running = False
        return True

    def resume(self):
        self.running = True
        return True

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop()
        self.stop_event.clear()
        self.running = True

    # Todo: Implement the following methods in the frontend0
    def pulse(self, color):
        return {"NodeId": self._id, "color": color}

    def sendConnectionExec(self, fromId, toId):
        return {"type": "CONNECTION_EXEC", "data": {"from": fromId, "to": toId}}

    def sendErrorMessage(self, nodeId, errorMessage):
        return {
            "type": "NODE_EXEC_ERROR",
            "data": {"nodeId": nodeId, "errorMessage": errorMessage},
        }

    def __str__(self) -> str:
        return f"[{self.type}|{self._id}|{self.name}]"

    @staticmethod
    def normalize_id_on_dict(dictionary):
        temp = dictionary.copy()
        temp["_id"] = str(dictionary["_id"])
        return temp
