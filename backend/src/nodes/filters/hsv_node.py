from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from .color_classes import ColorRange
from api import logger, exception

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


class HsvNode(BaseNode):
    """
    HsvNode is a class to convert an image to HSV color space and filter it by a color range.

    Signals ->
        "HSV Mask" -> returns the filtered color range in HSV color space.
        "Better HSV" -> returns the same at above but with an MorphologyEx applied to remove noise pixels.
    """

    @exception(logger)
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
        self.auto_run = options["auto_run"]
        NodeManager.addNode(self)

    @exception(logger)
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
