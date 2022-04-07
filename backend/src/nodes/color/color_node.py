from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.color.color_obj import ColorOBJ as color
from api import logger, exception

NODE_TYPE = "COLOR"

color_modes = [
    color.RGB, color.HEX, color.HSV, color.CV2_HSV
]

class ColorNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections

        self.color_code = options["color_code"]
        self.color_mode = options["color_name"]
        
        self.color = color(self.color_code, self.color_mode)
        self.auto_run = options["auto_run"]["value"]

        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=None):
        if message:
            self.color = color(message.payload, self.color_mode)
        for output in color_modes:
            self.on(output, self.color.get(output))

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "color_modes": color_modes,
            }
        }
