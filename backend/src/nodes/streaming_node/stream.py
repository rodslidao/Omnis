from src.manager.camera_manager import CameraManager
from src.nodes.node_registry import NodeRegistry
from bson import ObjectId


class StreamNode:
    def __init__(self, camera_id, node_type) -> None:
        self._id = ObjectId()
        self.name = "StreamNode"
        self.camera = StreamNode.update_camera(camera_id)
        self.node = StreamNode.update_node(node_type)
        CameraManager.add(self)

    @staticmethod
    def update_node(node_type):
        return NodeRegistry.getNodeClassByName(node_type)

    @staticmethod
    def update_camera(camera_id):
        return CameraManager.get_by_id(camera_id)

    def source_update(self, camera_id, node_type):
        self.camera = StreamNode.update_camera(camera_id)
        self.node = StreamNode.update_node(node_type)
        print(self.camera, self.node)
        return bool(self.camera and self.node)

    def read(self):
        return self.node.stream_frame(self.camera.read())


Stream = StreamNode("6244b07d3a8338aceae46cee", "HSV")
