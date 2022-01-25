if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import cv2
from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode


NODE_TYPE = "COLORSPACE"


class ColorSpaceNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.CSO = options["colorSpaceOrigin"]
        self.CSC = options["colorSpaceConvert"]
        NodeManager.addNode(self)

    def execute(self, message):
        try:
            _ = cv2.cvtColor(
                message["payload"], getattr(cv2, f"COLOR_{self.CSC}2{self.CSO}")
            )
            self.onSuccess(_)
        except Exception as e:
            self.onFailure("Cant execute action", pulse=True, errorMessage=str(e))
