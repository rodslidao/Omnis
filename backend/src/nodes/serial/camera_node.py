from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from .camera_object import CameraOBJ
from src.nodes.timer.task_time import setInterval

NODE_TYPE = "CAMERA"


class CameraNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.camera = CameraOBJ(options.hardware.get("camera_id"))
        NodeManager.addNode(self)
        self.stop_event = self.execute()

    @setInterval(0.5)
    def execute(self, message=""):
        try:
            self.onSuccess(self.camera.read())
        except Exception as e:
            self.camera.stop()
            self.onFailure("Cant read camera frame", pulse=True, errorMessage=str(e))

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
