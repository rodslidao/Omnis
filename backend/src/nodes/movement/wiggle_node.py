from src.nodes.base_node import BaseNode, Wizard
from src.manager.serial_manager import SerialManager
NODE_TYPE = "PositionAdjustmentNode"


"""
options:
axisListDialog
mode
zStep
repetitions
invert
divider
velocity['value']
board
"""
class Wiggle_Node(BaseNode):
    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections, input_connections)
        self.axisList = options["axisListDialog"]
        self.mode = options["mode"]
        self.zStep = options["zStep"]
        self.repetitions = options["repetitions"]
        self.invert = options["invert"]
        self.divider = options["divider"]
        self.velocity['value'] = options["velocity"]
        self.board = options["board"]

        self.serial = SerialManager.get_by_id(self.board['id'])
        if not self.serial: raise TypeError("SERIAL DEAD")
        self.serial.resume()

    @Wizard._decorator
    def execute(self, message):
        action = message.targetName.lower()
        if action == "xy":
            self.xy(message.payload)
        if (self.wait_checks >= len(self.wait_for_this)) and self.has_trigger: self.trigger.set()
        if (action == "gatilho" and  self.trigger.wait(120)) or ((self.wait_checks >= len(self.wait_for_this)) and not self.has_trigger):
            if self.has_trigger: self.trigger.clear()
            self.trigger()
        # elif action == "x":
        #     self.x(message.payload)
        # elif action == "y":
        #     self.y(message.payload)
        # elif action == "z":
        #     self.z(message.payload)
        else:
            self.on("Falha", "Invalid action")
            raise TypeError("Invalid action")

    def trigger(self):
        for i in range(self.repetitions):
            for axis in self.axisList:
                for signal in ['min', 'max']:
                    coordinates = {}
                    coordinates[axis['name'].lower()] = {'min':None, 'max':None}
                    coordinates[axis['name'].lower()][signal] = self.coordinates[axis['name']]+(axis[signal]/(self.divider*i))
            start_signal = ['min', 'max'] if self.invert['direction'] else ['max', 'min']
            start_axis =   ['Y', 'X'] if self.invert['axis'] else ['X', 'Y']
            for axis in start_axis:
                for signal in start_signal:
                    pos = (axis.lower(), coordinates[axis['name'].lower()][signal], 'F', self.velocity['value'])
                    self.serial.G0(*pos)
            self.serial.G0(*('Z', self.coordinates['z']+(self.zStep/(self.divider*i)), 'F', self.velocity['value']))
        self.onSuccess('Sucesso', 'Movimento realizado com sucesso')

    def xy(self, payload, axis=None):
        for k, v in payload.items():
            self.coordinates[k.lower()] = v
            self.wait_checks+=1
    
#Axis List = [{"name": "X", "min":-10, "max":10}]
# cord{x}{min}