from time import sleep
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.manager.serial_manager import SerialManager
NODE_TYPE = "MOVEMENT"
class MovementNode(BaseNode):
    """
    A class to send movement commands GCODES trough an serial instace.

    """
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_id = options["hardware"]["serial_id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        self.axis = list(map(lambda x: x.lower(), options["axis"]["list_of_axis"]))
        self.coordinates = {k.lower(): v for k, v in options["axis"]["axis_values"].items() if k.lower() in self.axis}
        NodeManager.addNode(self)

    def execute(self, message):
        action = message.targetName.lower()
        if action in self.axis:
            self.coordinates[action] = message.payload[action]
        else:
            try:
                return getattr(self, action+'_f')(message.payload)
            except Exception as e:
                self.onFailure("Cant execute action", pulse=True, errorMessage=str(e))

    def coordinates_f(self, payload):
        for k, v in payload["coordinates"].items():
            self.coordinates[k] = v
        self.coordinates = payload["coordinates"]

    def trigger_f(self, payload=None):
        sleep(0.2)
        if self.serial is not None and self.serial.is_open:
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
                if (k in self.axis and v is not None)
            ]
            try:
                print(self.serial.__dict__)
                self.serial.M_G0(*movement, sync=True)
                self.log(f"success: {movement}")
                self.onSuccess(self.serial)
            except Exception as e:
                self.onFailure("Cant execute movement", pulse=True, errorMessage=str(e))
        else:
            if not self.serial.is_open:
                self.onFailure("Serial not running", pulse=True)

            if self.serial is None:
                self.onFailure("Serial not connected", pulse=True)

    def stop(self):
        try:
            self.serial.stop()
        except AttributeError:
            pass

    def resume(self):
        super().resume()
    
    def pause(self):
        super().pause()
