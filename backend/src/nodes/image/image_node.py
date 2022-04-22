from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.image.image_obj import Image
from api import logger, exception, for_all_methods

NODE_TYPE = "IMAGE"

properties = [
    "path",
    "height",
    "width",
    "size",
    "color_space",
    "channels",
    "area",
    "dominant_color",
    "dominant_color_array",
    "dominant_color_range",
]


@for_all_methods(exception(logger))
class ImageNode(BaseNode):
    """
    Node to manipulate an image with mos common operations.
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.image = None  # ? Maybe we should use a Image object instead of None ?
        self.properties = options.image.get("properties", [])
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    def execute(self, message=""):

        self.image = Image(image=message.payload)
        self.onSuccess(self.image)

        for prop in self.properties:
            self.on(prop, getattr(self.image, prop))

    def get_frame(self):
        return self.image()

    @staticmethod
    def get_info():
        return {"options": {"properties": properties}}
