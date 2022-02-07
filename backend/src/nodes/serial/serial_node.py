if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from .serial_obj import SerialOBJ
from .gcode_obj import SerialGcodeOBJ
from src.nodes.timer.task_time import setInterval


NODE_TYPE = "SERIAL"


class SerialNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_name = options["hardware"]["serial_name"]
        self.serial_port = options["porta"]["serial_port"]
        self.serial_bandrate = options["velocidade"]["serial_baudrate"]
        self.reconnect = options["reconectar"]["serial_reconnect"]

        if options["connection_type"]["serial_connection_type"] == "gcode":
            serial_class = SerialGcodeOBJ
        else:
            serial_class = SerialOBJ

        self.serial = serial_class(
            self.serial_name,
            self.serial_port,
            self.serial_bandrate,
            reconnect=self.reconnect,
        )
        #print("SerialNode:", self.serial_name, self.serial_port, self.serial_bandrate)
        self.stop_event = self.execute()
        NodeManager.addNode(self)

    @setInterval(1)
    def execute(self, message=""):
        #print("Executing SerialNode")
        if not self.serial.isAlive():
            try:
                self.serial.start()
                self.onSuccess(self.serial)
                self.on("serial", self.serial)
                return
            except Exception as e:
                self.onFailure("Cant start serial", pulse=True, errorMessage=str(e))
        else:
            self.onSuccess(self.serial)

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
