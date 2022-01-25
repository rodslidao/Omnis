if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode

NODE_TYPE = "MOVEMENT"


class MovementNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial = False
        self.axis = list(map(lambda x: x.lower(), options["axis"]))
        self.coordinates = {k: v for k, v in options if k in self.axis}
        NodeManager.addNode(self)

    def execute(self, message):
        action = message["targetName"].lower()
        if action in self.axis:
            self.coordinates[action] = message["payload"][action]
        else:
            try:
                getattr(self, action)(message["payload"])
            except Exception as e:
                self.onFailure("Cant execute action", pulse=True, errorMessage=str(e))

    def serial(self, payload):
        self.serial = payload["serial"]

    def coordinates(self, payload):
        for k, v in payload["coordinates"].items():
            self.coordinates[k] = v
        self.coordinates = payload["coordinates"]

    def trigger(self, payload=None):
        if self.serial is not None and self.serial.isAlive():
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
                if (k in self.axis and v is not None)
            ]
            try:
                self.serial.MG0(*movement, nonsync=None)
                self.onSuccess({"serial": self.serial})
            except Exception as e:
                self.onFailure("Cant execute movement", pulse=True, errorMessage=str(e))
        else:
            if not self.serial.isAlive():
                self.onFailure("Serial not running", pulse=True)

            if self.serial is None:
                self.onFailure("Serial not connected", pulse=True)
