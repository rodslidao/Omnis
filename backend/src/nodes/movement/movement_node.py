from time import sleep
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.manager.serial_manager import SerialManager
from api import logger, exception
from api.decorators import for_all_methods

NODE_TYPE = "MOVEMENT"


@for_all_methods(exception(logger))
class MovementNode(BaseNode):
    """
    A class to send movement commands GCODES trough an serial instace.

    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.serial_id = options["hardware"]["serial_id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        self.axis = []
        self.coordinates = {}
        for axi in options["axisList"]:
            if axi["isActive"]:
                self.axis.append(axi["name"].lower())
                self.coordinates[axi["name"].lower()] = axi["value"]
        self.relative = options["axis"].get("relative", False)
        self.trigger_delay = 10
        self.coordinates = {
            k.lower(): v
            for k, v in options["axis"]["values"].items()
            if k.lower() in self.axis
        }
        self.auto_run = options.get(["auto_run"], False)
        NodeManager.addNode(self)

    def execute(self, message):
        action = message.targetName.lower()
        if action in self.axis:
            self.coordinates[action] = message.payload
        else:
            return getattr(self, action + "_f")(message.payload)

    def coordinates_f(self, payload):
        for k, v in payload.items():
            self.coordinates[k.lower()] = v

    # ToDo time for wait after movement needs to be set on options.
    def trigger_f(self, payload=None):
        if self.serial is not None and self.serial.is_open:
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
                if (k in self.axis and v is not None)
            ]

            t = 0.5  # ! Remove this line

            if self.relative:
                self.serial.send("G91")
                t = 1  # ! Remove this line
            else:
                self.serial.send("G90")

            self.serial.M_G0(*movement, sync=True)
            sleep(t)
            self.onSuccess(self.serial_id)

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

    def get_info(**kwargs):
        return {"options": SerialManager.get_info()}
