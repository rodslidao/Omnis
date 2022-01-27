if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from time import sleep
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

NODE_TYPE = "MOVEMENT"


class MovementNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial = False
        self.axis = list(map(lambda x: x.lower(), options["axis"]["list_of_axis"]))
        self.coordinates = {k.lower(): v for k, v in options["axis"]["axis_values"].items() if k.lower() in self.axis}
        NodeManager.addNode(self)

    def execute(self, message):
        action = message.targetName.lower()
        #print(f"MovementNode [{self.id}]:")
        if action in self.axis:
            self.coordinates[action] = message.payload[action]
        else:
            try:
                getattr(self, action+'_f')(message.payload)
            except Exception as e:
                #print(e)
                self.onFailure("Cant execute action", pulse=True, errorMessage=str(e))

    def serial_f(self, payload):
        #print(f"MovmentNode [{self.id}][Serial]:", payload)
        self.serial = payload

    def coordinates_f(self, payload):
        for k, v in payload["coordinates"].items():
            self.coordinates[k] = v
        self.coordinates = payload["coordinates"]

    def trigger_f(self, payload=None):
        #print(f"MovmentNode [{self.id}][Trigger]")
        sleep(0.2)
        if self.serial is not None and self.serial.isAlive():
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
                if (k in self.axis and v is not None)
            ]
            try:
                self.serial.M_G0(*movement, nonsync=None)
                self.onSuccess(self.serial)
            except Exception as e:
                #print(e)
                self.onFailure("Cant execute movement", pulse=True, errorMessage=str(e))
        else:
            if not self.serial.isAlive():
                #print("Serial not running")
                self.onFailure("Serial not running", pulse=True)

            if self.serial is None:
                #print("Serial not connected")
                self.onFailure("Serial not connected", pulse=True)

    def stop(self):
        #print(f"MovmentNode [{self.id}]: Stop")
        try:
            self.serial.stop()
        except AttributeError:
            pass

    def resume(self):
        super().resume()
        #print(f"MovmentNode [{self.id}]: resume")
    
    def pause(self):
        super().pause()
        #print(f"MovmentNode [{self.id}]: pause")
