from src.message import Message
from src.nodes.node_manager import NodeManager
from api import logger, exception
from api.decorators import for_all_methods
from api.store import nodes
from api.subscriptions import SubscriptionFactory
from threading import Event

from threading import Thread, Event, Lock
NODE_TYPE = "BASE_NODE"
rtc_status = SubscriptionFactory(nodes, 'nodes')     

CKL = Lock()
event_list = {}
class Wizard(object):
    def _decorator(exteral_execution):
        def magic( self, *args, **kwargs ):
            try:
                CKL.acquire()
                logger.warning(f"{self.__class__.__name__} - {exteral_execution.__name__}")
                event_list[self._id] = Event()
                exteral_execution( self, *args, **kwargs )
                event_list[self._id].set()
            except KeyError:
                event_list[self._id] = Event().set()
            finally:
                logger.warning(f"{self.__class__.__name__} - {exteral_execution.__name__} - END")
                CKL.release()
        return magic
    _decorator = staticmethod( _decorator )

    @_decorator
    def execute( self ) :
        logger.error("normal call")

    _decorator = staticmethod( _decorator )

@for_all_methods(exception(logger))
class BaseNode(Wizard):
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
        self.update_status({
            "status": "LOADED"
        })
        logger.info("[%s] Node loaded", self)

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
            node_to_run = NodeManager.getNodeById(target.get("to").get("nodeId"))

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

            if not self.running:
                node_to_run.update_status({"status": "PAUSED"})

            while not self.running:
                if self.stop_event.isSet():
                    self.resume()
                    return

            if node_to_run and not self.stop_event.isSet():
                logger.info(f'Trigger: {node_to_run}')
                self.update_status({"status": "SENDING", "message":{"from":target.get("from").get("id"), "to":target.get("to").get("id")}})
                Thread(target=node_to_run.execute, args=(message,), name=f"{str(self)}({message.sourceName}) -> {message}", daemon=True).start()
                # self.resume()
                # node_to_run.update_status({"status": "RUNNING", "message":{"from":None, "to":None}})
                # self.update_status({"status": "RUNNING", "message":{"from":None, "to":None}})

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

    def who_am_i(self):
        self.info = {
            "name": self.name,
            "type": self.type,
            "id": self._id,
            "info": self.status,
        }
        rtc_status.put(self.info)
        return self.info
        
    
    def update_status(self, info):
        self.status = info
        self.who_am_i()

    def pause(self):
        self.running = False
        return True

    def resume(self):
        self.running = True
        self.stop_event.clear()
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

    def to_dict(self):
        return {
            "name": self.name,
            "id": self._id,
            "options": self.options,
            "output_connections": self.output_connections,
        }
        
    @staticmethod
    def normalize_id_on_dict(dictionary):
        temp = dictionary.copy()
        temp["_id"] = str(dictionary["_id"])
        return temp