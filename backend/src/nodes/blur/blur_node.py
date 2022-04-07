from email.mime import image
from re import A
from statistics import median
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

from cv2 import GaussianBlur, blur, medianBlur
from api import logger, exception

NODE_TYPE = "BLUR"


blur_types = {"GAUSSIAN": GaussianBlur, "MEDIAN": medianBlur, "DEFAULT": blur}


class BlurNode(BaseNode):
    """
    Node to somothing an image
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.type = options["blur_type"]
        self.k_size = options["blur_intensity"]
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        self.image = message.payload
        try:
            _ = blur_types[self.type](
                self.image,
                self.k_size if self.type == "MEDIAN" else (self.k_size, self.k_size),
            )
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
                "blur_types": list(blur_types.keys()),
            }
        }
