
from curses import baudrate
from src.nodes.node_registry import *
from src.nodes.node_manager import *
from src.message import Message

from src.nodes.serial.custom_serial import CustomSerial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ

ser = SerialGcodeOBJ(name="Teste", filters={"device": "/dev/ttyACM0"}, baudrate=250000)
ser.start()
_id = str(ser._id)

NODE_TO_LOAD = "movement"
NODE_NAME = "movement"
NODE_ID = "movement_id"
NODE_OPTIONS = {"hardware":{"serial_id":_id}, "axis":{"list_of_axis":['z','f'], "axis_values":{"z":0, "f":5000}} }
NODE_OUT_CONNECTIONS = {}
NODE_INP_CONNECTIONS = {}
NONE = None
targets = [1]

INITIAL_PAYLOADs = [Message(
                            NODE_ID,
                            NONE,
                            NODE_NAME,
                            "trigger",
                            NODE_ID,
                            NONE,
                            "TEST",
                            NONE,
                    ) for _ in targets]

NODE_CLASS = NodeRegistry.getNodeClassByName(NODE_TO_LOAD)

NODE_CLASS(
    NODE_NAME,
    NODE_ID,
    NODE_OPTIONS,
    NODE_OUT_CONNECTIONS,
    NODE_INP_CONNECTIONS,
)

retorno = [NodeManager.getNodeById(NODE_ID).execute(INITIAL_PAYLOAD) for INITIAL_PAYLOAD in INITIAL_PAYLOADs]
