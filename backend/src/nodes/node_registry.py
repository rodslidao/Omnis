if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# import all nodes from .nodes folder
from .button.button_node import ButtonNode
from .define.variable_node import VariableNode
from .display.printer_node import PrinterNode
from .movement.movement_node import MovementNode
from .serial.camera_node import CameraNode
from .serial.serial_node import SerialNode

# Copilot suggestion for new nodes:
# from src.nodes.display.display_node import DisplayNode
# from src.nodes.led.led_node import LEDNode
# from src.nodes.motor.motor_node import MotorNode
# from src.nodes.sensor.sensor_node import SensorNode


class RegEntry:
    def __init__(self, name, clss):
        self.name = name
        self.clss = clss


# array of all nodes, use RegEntry to register nodes, like Regentry("name", clss)
nodeRegistry = [
    RegEntry("button", ButtonNode),
    RegEntry("camera", CameraNode),
    RegEntry("movement", MovementNode),
    RegEntry("printer", PrinterNode),
    RegEntry("serial", SerialNode),
    RegEntry("variable", VariableNode)
    # RegEntry("file_reader", FileReaderNode)
    # RegEntry("file_writer", FileWriterNode)
    # RegEntry("logger", LoggerNode)
    # RegEntry("timer", TimerNode)
]


class NodeRegistry:
    @staticmethod
    def getNodeClassByName(name):
        for entry in nodeRegistry:
            if entry.name == name:
                return entry.clss
        else:
            raise Exception("Class " + name + " not registered")
