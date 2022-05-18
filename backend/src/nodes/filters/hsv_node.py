from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

from api import logger, exception
from api.decorators import for_all_methods

from cv2 import (
    COLOR_BGR2HSV_FULL,
    inRange,
    cvtColor,
    COLOR_BGR2HSV,
    bitwise_and,
    FONT_HERSHEY_SIMPLEX,
    putText,
    imread,
)

from numpy import array

NODE_TYPE = "HsvFilterNode"


@for_all_methods(exception(logger))
class HsvNode(BaseNode):
    """
    HsvNode is a class to convert an image to HSV color space and filter it by a color range.

    Signals ->
        "HSV Mask" -> returns the filtered color range in HSV color space.
        "Better HSV" -> returns the same at above but with an MorphologyEx applied to remove noise pixels.
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.color_range = {
            "lower": list(options["lower"].values()),
            "upper": list(options["upper"].values()),
        }
        self.auto_run = options.get(["auto_run"], False)
        self.image = imread("./src/imgs/no_image.jpg")
        NodeManager.addNode(self)

    def execute(self, message):
        target = message.targetName.lower()
        if target == "color_range":
            self.color_range = message.payload
        elif target == "imagem":
            self.image = message.payload
            self.on("Saida", self.read())

    @staticmethod
    def convert_frame(image, lower, upper):
        return inRange(
            cvtColor(image, COLOR_BGR2HSV_FULL),
            array(lower),
            array(upper),
        )

    def read(self):
        return self.convert_frame(
                    self.image,
                    self.color_range["lower"],
                    self.color_range["upper"],
                )

        return putText(
            _,
            f"HSV Range: {self.color_range}",
            (10, 30),
            FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

    def update_options(self, *args, **kwargs):
        if kwargs.get("lower") and kwargs.get("upper"):
            self.color_range["lower"] = list(kwargs["lower"].values())
            self.color_range["upper"] = list(kwargs["upper"].values())
        

    @staticmethod
    def stream_frame(frame, lower, upper):
        return HsvNode.convert_frame(frame, lower, upper)