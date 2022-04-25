from src.manager.camera_manager import CameraManager
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception, for_all_methods
import cv2
import numpy as np

NODE_TYPE = "CAMERA"


@for_all_methods(exception(logger))
class CameraNode(BaseNode):
    """
    Trigger it self every 'n' seconds.\n
    \n
    Signals -> \n
    \t:onSuccess: - Send last frame read.\n
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.camera_id = options["hardware"]["camera_id"]
        self.camera = CameraManager.get_by_id(self.camera_id).start()

        self.auto_run = options["auto_run"]["value"]

        bkg = cv2.imread(r"C:\Users\Henrycke\Desktop\bkg2.jpeg")
        bkg = cv2.rotate(bkg, cv2.cv2.ROTATE_90_CLOCKWISE)
        bkg = cv2.resize(bkg, (652, 802))
        self.bkg = np.concatenate((bkg, np.zeros((802, 900, 3), np.uint8)), axis=1)

        NodeManager.addNode(self)

    def execute(self, message=""):
        self.onSuccess(self.get_frame())

    def get_frame(self):
        return self.bkg  # self.camera.read()

    @staticmethod
    def get_info():
        return {"options": CameraManager.get_info()}
