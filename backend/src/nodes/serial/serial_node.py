if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.timer.task_time import setInterval
from src.manager.serial_manager import SerialManager

NODE_TYPE = "SERIAL"


class SerialNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_id = options["hardware"]["serial_id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        self.stop_event = self.execute()
        NodeManager.addNode(self)

    @setInterval(1)
    def execute(self, message=""):
        if not self.serial.is_open:
            try:
                self.serial.start()
                self.onSuccess(self.serial)
                self.on("serial", self.serial)
                return True
            except Exception as e:
                self.onFailure("Cant start serial", pulse=True, errorMessage=str(e))
        else:
            self.onSuccess(self.serial)
            return True
        return False

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
