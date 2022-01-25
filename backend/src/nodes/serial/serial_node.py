if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode
from serial_obj import SerialOBJ
from gcode_obj import SerialGcodeOBJ
from nodes.timer.task_time import setInterval


NODE_TYPE = "SERIAL"


class SerialNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_name = options["hardware"]["serial_name"]
        self.serial_port = options["porta"]["serial_port"]
        self.serial_bandrate = options["velocidade"]["serial_bandrate"]
        self.reconnect = options["reconectar"]["reconnect"]
        if options["tipo"] == "gcode":
            serial_class = SerialGcodeOBJ
        else:
            serial_class = SerialOBJ
        self.serial = serial_class(
            self.serial_name,
            self.serial_port,
            self.serial_bandrate,
            reconnect=self.reconnect,
        )
        self.running = self.serial.isAlive
        self.stop_event = self.execute()
        NodeManager.addNode(self)

    @setInterval(0.5)
    def execute(self, message=""):
        if not self.running():
            try:
                self.serial.iniciar()
            except Exception as e:
                self.onFailure("Cant start serial", pulse=True, errorMessage=str(e))
                return
        if self.running():
            self.onSuccess({"serial": self.serial})

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
