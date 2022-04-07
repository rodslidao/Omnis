from time import sleep
import timeit
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.manager.serial_manager import SerialManager
from api import logger, exception
from os import popen
NODE_TYPE = "MOVEMENT"


class MovementNode(BaseNode):
    """
    A class to send movement commands GCODES trough an serial instace.

    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.serial_id = options["hardware"]["serial_id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        self.axis = list(map(lambda x: x.lower(), options["axis"]["list_of_axis"]))
        self.relative = options["axis"].get("relative", False)
        self.trigger_delay = 10
        self.coordinates = {
            k.lower(): v
            for k, v in options["axis"]["values"].items()
            if k.lower() in self.axis
        }
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        action = message.targetName.lower()
        if action in self.axis:
            self.coordinates[action] = message.payload
        else:
            return getattr(self, action + "_f")(message.payload)


    @exception(logger)
    def coordinates_f(self, payload):
        for k, v in payload.items():
            self.coordinates[k.lower()] = v

    #ToDo time for wait after movment needs to be set on options.
    @exception(logger)
    def trigger_f(self, payload=None):
        if self.serial is not None and self.serial.is_open:
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
               if (k in self.axis and v is not None)
            ]

            t = 0.5     #! Remove this line
             
            if self.relative:
                self.serial.send("G91")
                t = 1   #! Remove this line
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

    @exception(logger)
    def stop(self):
        try:
            self.serial.stop()
        except AttributeError:
            pass

    @exception(logger)
    def resume(self):
        super().resume()

    @exception(logger)
    def pause(self):
        super().pause()
