# from src.nodes.node_manager import NodeManager
# from src.nodes.base_node import BaseNode

# from api import logger, exception
# from api.decorators import for_all_methods

from cv2 import (
    COLOR_BGR2HSV_FULL,
    inRange,
    cvtColor,
    COLOR_BGR2HSV,
    bitwise_and,
    FONT_HERSHEY_SIMPLEX,
    putText,
)

from numpy import array

NODE_TYPE = "hsv-filter"


# @for_all_methods(exception(logger))
class HsvNode:
    """
    HsvNode is a class to convert an image to HSV color space and filter it by a color range.

    Signals ->
        "HSV Mask" -> returns the filtered color range in HSV color space.
        "Better HSV" -> returns the same at above but with an MorphologyEx applied to remove noise pixels.
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        # super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.color_range = {
            "lower": options["filter"]["lower"],
            "upper": ["filter"]["upper"],
        }
        self.auto_run = options["auto_run"]["value"]
        # NodeManager.addNode(self)

    def execute(self, message):
        target = message.targetName.lower()
        if target == "color_range":
            self.color_range = message.payload
        elif target == "image":
            self.message = message
            self.onSuccess(
                self.convert_frame(
                    message.payload,
                    self.color_range["lower"],
                    self.color_range["upper"],
                )
            )

    @staticmethod
    def convert_frame(image, lower, upper):
        return inRange(
            cvtColor(image, COLOR_BGR2HSV_FULL),
            array(lower),
            array(upper),
        )

    def get_frame(self):

        _ = bitwise_and(
            self.message.payload,
            self.message.payload,
            mask=self.convert_frame(
                self.message.payload,
                self.color_range["lower"],
                self.color_range["upper"],
            ),
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

    @staticmethod
    def stream_frame(frame, lower, upper):
        return HsvNode.convert_frame(frame, lower, upper)
