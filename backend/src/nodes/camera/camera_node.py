from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.camera.custom_camera import camera
from src.nodes.timer.task_time import setInterval

NODE_TYPE = "CAMERA"


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
        self.camera = camera(options.hardware.get("camera_id"))
        NodeManager.addNode(self)
        self.stop_event = self.execute()

    @setInterval(0.5)
    def execute(self, message=""):
        try:
            self.onSuccess(self.get_frame())
        except Exception as e:
            self.camera.reset()
            self.onFailure("Cant read camera frame", pulse=True, errorMessage=str(e))
    
    def get_frame(self):
        return self.camera.read()

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
