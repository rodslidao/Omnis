from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

from cv2 import (
    getStructuringElement,
    MORPH_BLACKHAT,
    MORPH_CLOSE,
    MORPH_CROSS,
    MORPH_DILATE,
    MORPH_ELLIPSE,
    MORPH_ERODE,
    MORPH_GRADIENT,
    MORPH_HITMISS,
    MORPH_OPEN,
    MORPH_RECT,
    MORPH_TOPHAT,
    morphologyEx,
)

NODE_TYPE = "MORPHOPERATION"

operations_types = {
    "ERODE": MORPH_ERODE,
    "DILATE": MORPH_DILATE,
    "OPEN": MORPH_OPEN,
    "CLOSE": MORPH_CLOSE,
    "GRADIENT": MORPH_GRADIENT,
    "TOPHAT": MORPH_TOPHAT,
    "BLACKHAT": MORPH_BLACKHAT,
    "HITMISS": MORPH_HITMISS,
}

element_types = {
    "RECT": MORPH_RECT,
    "CROSS": MORPH_CROSS,
    "ELLIPSE": MORPH_ELLIPSE,
}


class MorphoperationNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.op_type = options.operation_type["value"]
        self.element_type = options.element_type["value"]
        self.k_size = options.k_size["value"]
        self.kernel = getStructuringElement(
            element_types[self.element_type], (self.k_size, self.k_size)
        )

        self.auto_run = options["auto_run"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        self.image = message["payload"]
        try:
            _ = morphologyEx(self.image, operations_types[self.op_type], self.kernel)
            self.onSuccess(_)
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))

    @exception(logger)
    def get_frame(self):
        return self.image

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "operations_types": list(operations_types.keys()),
                "element_types": list(element_types.keys()),
            }
        }
