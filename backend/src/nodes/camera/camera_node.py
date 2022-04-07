from src.manager.camera_manager import CameraManager
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "CAMERA"


class CameraNode(BaseNode):
    """
    Trigger it self every 'n' seconds.\n
    \n
    Signals -> \n
    \t:onSuccess: - Send last frame read.\n
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.camera_id = options["hardware"]["camera_id"]
        self.camera = CameraManager.get_by_id(self.camera_id).start()

        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        self.onSuccess(self.get_frame())

    @exception(logger)
    def get_frame(self):
        return self.camera.read()

    @staticmethod
    @exception(logger)
    def get_info():
        info = {}
        print(CameraManager.get())
        info["options"] = {"hardware": CameraManager.get()}
        return info
