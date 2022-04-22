from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.timer.task_time import setInterval
from src.manager.serial_manager import SerialManager
from api import logger, exception, for_all_methods

NODE_TYPE = "SERIAL"


@for_all_methods(exception(logger))
class SerialNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_id = options["hardware"]["serial_id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        self.stop_event = self.execute()
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @setInterval(1)
    def execute(self, message=""):
        if not self.serial.is_open:
            self.serial.start()
            self.onSuccess(self.serial)
            self.on("serial", self.serial)
            return True
        else:
            self.onSuccess(self.serial)
            return True

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
