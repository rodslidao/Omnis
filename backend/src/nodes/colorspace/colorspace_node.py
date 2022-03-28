from tkinter import N
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

from api import logger, exception

NODE_TYPE = "COLORSPACE"
from cv2 import (
    cvtColor,
    COLOR_BGR2HSV,
    COLOR_HSV2BGR,
    COLOR_BGR2RGB,
    COLOR_RGB2BGR,
    COLOR_BGR2GRAY,
    COLOR_GRAY2BGR,
)

color_operations = {
    "BGR2HSV": COLOR_BGR2HSV,
    "HSV2BGR": COLOR_HSV2BGR,
    "BGR2RGB": COLOR_BGR2RGB,
    "RGB2BGR": COLOR_RGB2BGR,
    "BGR2GRAY": COLOR_BGR2GRAY,
    "GRAY2BGR": COLOR_GRAY2BGR,
}


class ColorspaceNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.operation = options.color_space["value"]
        self.image = None
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        self.image = message.payload
        try:
            self.image = cvtColor(self.image, color_operations[self.operation])
            self.onSuccess(self.image)
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))

    @exception(logger)
    def get_frame(self):
        return self.image

    @staticmethod
    @exception(logger)
    def get_info():
        return {"options": {"color_space": list(color_operations.keys())}}
