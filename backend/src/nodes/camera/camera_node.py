from src.manager.camera_manager import CameraManager
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception
from api.decorators import for_all_methods

NODE_TYPE = "CameraNode"

@for_all_methods(exception(logger))
class CameraNode(BaseNode):
    """
    Trigger it self every 'n' seconds.\n
    \n
    Signals -> \n
    \t:onSuccess: - Send last frame read.\n
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.camera_id = options["camera"]["id"]
        self.camera = CameraManager.get_by_id(self.camera_id).start()
        self.auto_run = options.get("auto_run", True)
        NodeManager.addNode(self)

    def execute(self, message=""):
        self.on("Imagem", self.get_frame())

    def get_frame(self):
        return self.camera.read()

    @staticmethod
    def get_info():
        return {"options": CameraManager.get_info()}
