import cv2
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "COLORSPACE"


class ColorSpaceNode(BaseNode):
    """
    Convert an image color format to another.
    More info about color conversion methods can be found here: https://docs.opencv.org/4.5.5/de/d25/imgproc_color_conversions.html
    More info about color conversion codes can be found here:    https://docs.opencv.org/4.5.5/d8/d01/group__imgproc__color__conversions.html
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.CSO = options["colorSpaceOrigin"]
        self.CSC = options["colorSpaceConvert"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        try:
            _ = cv2.cvtColor(
                message["payload"], getattr(cv2, f"COLOR_{self.CSC}2{self.CSO}")
            )
            self.onSuccess(_)
        except Exception as e:
            self.onFailure("Cant execute action", pulse=True, errorMessage=str(e))
