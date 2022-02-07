if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from color_classes import ColorRange


from cv2 import (
    inRange,
    cvtColor,
    COLOR_BGR2HSV_FULL,
    morphologyEx,
    MORPH_CLOSE,
    MORPH_OPEN,
)

from numpy import array, ones, uint8

NODE_TYPE = "HSV"


class HSVMaskNode(BaseNode):
    def __init__(self, name, type, id, options, outputConnections) -> None:
        super().__init__(name, type, id, options, outputConnections)
        self.lower = options["lower"]["value"]
        self.upper = options["upper"]["value"]
        self.mode = options["color_mode"]
        self.interations = options["interations"]
        self.kernel = ones((5, 5), uint8)
        self.color_range = ColorRange(
            "color_range", self.mode, self.lower, self.upper
        ).get("cv2_hsv")
        NodeManager.addNode(self)

    def execute(self, message):
        try:
            hsv_mask = inRange(
                cvtColor(message, COLOR_BGR2HSV_FULL),
                array(self.color_range["lower"]),
                array(self.color_range["upper"]),
            )
            better_hsv = morphologyEx(
                morphologyEx(
                    hsv_mask, MORPH_CLOSE, self.kernel, iterations=self.interations
                ),
                MORPH_OPEN,
                self.kernel,
                iterations=self.interations,
            )
            self.on("Better HSV", better_hsv)
            self.on("HSV Mask", hsv_mask)
        except Exception as e:
            self.onFailure(e)
