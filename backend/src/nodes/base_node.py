from src.nodes.alerts.alert_obj import Alert
from src.message import Message
from src.nodes.node_manager import NodeManager
from api import logger, exception
from api.decorators import for_all_methods
from api.store import nodes
from api.subscriptions import SubscriptionFactory
from threading import Event
from src.end_points import NodeStatus
from threading import Thread, Event
import asyncio
import queue
event_list = queue.Queue()

from src.manager.process_manager import ProcessManager as process

NODE_TYPE = "BASE_NODE"
rtc_status = SubscriptionFactory(nodes, "nodes")
BaseNode_websocket = NodeStatus("node_status_updater", lambda: True)

class Wizard(object):
    def _decorator(exteral_execution):
        def magic(self, message):
            try:
                exteral_execution(self, message)
                event_list.get()
            except Exception as e:
                Alert("error", "Falha durante o processo", "Erro: {}".format(e))
                # process.stop()
                exit()
                raise e
            finally:
                event_list.task_done()
        return magic

    _decorator = staticmethod(_decorator)

    @_decorator
    def execute(self):
        logger.error("The Wizard decorator should decorate an node 'execute' function.")

    _decorator = staticmethod(_decorator)


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

    def __init__(self, name, type_, id, options, output_connections) -> None:
        self.name = name
        self.type = type_
        self._id = id
        self.options = options
        self.output_connections = output_connections
        self.running = True
        self.stop_event = Event()
        self.status = "LOADED"
        self.info = {
            "name": self.name,
            "type": self.type,
            "id": self._id,
            "info": self.status,
        }
        self.update_status({"status": "LOADED"})
        self.auto_run = options.get("auto_run", False)
        logger.debug(f"[{type(self).__name__}] || {self.name} Node loaded")
        # Thread(target=self.auto_update, name=f"NodeStatus_auto_update", daemon=True).start()

    def auto_update(self):
        asyncio.run(BaseNode_websocket.broadcast_on_change(self.who_am_i, self.who_am_i))

    def onSuccess(self, payload, additional=None):
        self.on("onSuccess", payload, additional)

    def onSignal(self, signal=True):
        self.on("Sinal", signal)

    def onFailure(self, payload, additional=None, pulse=True, errorMessage=""):
        self.on("onFailure", payload, additional, pulse)

    def on(self, trigger, payload, additional=None, pulse=False, errorMessage=""):
        for target in list(
            filter(
                lambda connection: connection.get("from").get("name") == trigger,
                self.output_connections,
            )
        ):

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

            node_to_run = NodeManager.getNodeById(target.get("to").get("nodeId"))

            if not self.running:
                node_to_run.update_status({"status": "PAUSED"})

            while not self.running:
                if self.stop_event.isSet():
                    return self.resume()

            logger.debug(f"[{self}] Sending message {message} to node [{node_to_run}]")
            if node_to_run and not self.stop_event.isSet():
                event_list.put(message._id)
                self.update_status(
                    {
                        "status": "SENDING",
                        "message": {
                            "from": target.get("from").get("id"),
                            "to": target.get("to").get("id"),
                        },
                    }
                )
                A = Thread(
                    target=node_to_run.execute,
                    args=(message,),
                    name=f"{str(self)}({message.sourceName}) -> {message}",
                    daemon=True,
                )
                A.start()
                A.join(2)
                self.status = {
                        "status": "SENDED",
                        "message": {
                            "from": "",
                            "to": "",
                        },
                    }
                

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
        self.info["name"] = self.name
        self.info["type"] = self.type
        self.info["id"] = self._id
        self.info["info"] = self.status
        # rtc_status.put(self.info)
        return self.info

    def update_status(self, info):
        self.status = info
        return self.who_am_i()
        # BaseNode_websocket._broadcast(self.who_am_i())
        

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
        return f"[{self.type}|{self.name}]"

    def to_dict(self):
        return {
            "name": self.name,
            "id": self._id,
            "options": self.options,
            "output_connections": self.output_connections,
        }

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def normalize_id_on_dict(dictionary):
        temp = dictionary.copy()
        temp["_id"] = str(dictionary["_id"])
        return temp