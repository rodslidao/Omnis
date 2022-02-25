from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
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
        self.color_range = {"lower": options["lower"]["value"], "upper": options["upper"]["value"]}
        self.auto_run = options["auto_run"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        target = message["targetName"].lower()
        if target == "color_range":
            self.color_range = message["payload"]

        try:
            self.onSuccess(inRange(
                cvtColor(message['payload'], COLOR_BGR2HSV_FULL),
                array(self.color_range["lower"]),
                array(self.color_range["upper"]),
            ))
        except Exception as e:
            self.onFailure(e)
