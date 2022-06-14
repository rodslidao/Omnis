from cmath import log
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode, Wizard
from src.manager.serial_manager import SerialManager
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from api import logger, exception
from api.decorators import for_all_methods

NODE_TYPE = "MoveAxisNode"


@for_all_methods(exception(logger))
class MovementNode(BaseNode):
    """
    A class to send movement commands GCODES trough an serial instace.

    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.serial_id = options["board"]["id"]
        self.serial = SerialManager.get_by_id(self.serial_id)
        # if self.serial is not isinstance(self.serial, SerialGcodeOBJ):
        #     raise Exception("Serial not found")
            # self.on("Falha", "Serial not connected")
        self.axis = []
        self.coordinates = {}
        self.wait_for_this = [{k.lower():v for k,v in x['to'].items() if k == "name"} for x in self.input_connections]
        self.wait_checks = 0
        for axi in options["axislist"]:
            if axi["isActive"]:
                self.axis.append(axi["name"].lower())
                self.coordinates[axi["name"].lower()] = axi["value"]
        self.relative = options.get("relative", False)
        self.trigger_delay = 2
        self.auto_run = options.get("auto_run", False)
        NodeManager.addNode(self)

    @Wizard._decorator
    def execute(self, message):
        # logger.info(f"{self.name} received message: {message}")
        action = message.targetName.lower()
        if action in self.axis:
            self.coordinates[action] = message.payload
        elif action == "xy":
            self.coordinates_f(message.payload)
        if self.wait_checks == len(self.wait_for_this) or action == "gatilho":
            self.gatilho_f()
        else:
            logger.error(f"Waiting for {self.wait_checks}/{len(self.wait_for_this)}")
        # else:
        #     return getattr(self, action + "_f")(message.payload)

    def coordinates_f(self, payload):
        try:
            for k, v in payload.items():
                self.coordinates[k.lower()] = v
            self.wait_checks+=1
        except AttributeError:
            self.on("Falha", "Invalid payload")

    # ToDo time for wait after movement needs to be set on options.
    def gatilho_f(self):
        self.wait_checks = 0
        # return
        if self.serial is not None and self.serial.is_open:
            movement = [
                (k, v)
                for k, v in self.coordinates.items()
                if v is not None
            ]

            # t = 0.5  # ! Remove this line

            if self.relative:
                self.serial.send("G91", log=False)
                # t = 1  # ! Remove this line
            else:
                self.serial.send("G90", log=False)
            # logger.info(f"coords: {movement}")
            self.serial.M_G0(*movement, sync=True)
            self.on("Sucesso", self.serial_id)

        else:
            if not self.serial.is_open:
                self.on("Falha","Serial not running", pulse=True)

            if self.serial is None:
                self.on("Falha","Serial not connected", pulse=True)

    # def stop(self):
    #     self.serial.stop()
    #     super().stop()

    # def resume(self):
    #     logger.info(f"{self.name} resumed")
    #     self.serial.resume()
    #     super().stop()

    # def pause(self):
    #     self.serial.pause()
    #     super().stop()

    def get_info(**kwargs):
        return {"options": SerialManager.get_info()}
