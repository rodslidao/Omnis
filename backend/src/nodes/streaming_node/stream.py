from src.manager.camera_manager import CameraManager
from src.nodes.node_manager import NodeManager
from bson import ObjectId


class StreamNode:
    def __init__(self) -> None:
        self._id = ObjectId()
        self.name = "StreamNode"
        # self.camera = StreamNode.update_camera(camera_id)
        # self.node = StreamNode.update_node(node_id)
        CameraManager.add(self)

    @staticmethod
    def update_node(node_id):
        return NodeManager.getNodeById(node_id)

    @staticmethod
    def update_camera(camera_id):
        return CameraManager.get_by_id(camera_id)

    def source_update(self, node_id, *args, **kwargs):
        self.node = StreamNode.update_node(node_id)
        return bool(self.node)

    def read(self):
        return self.node.read()

    def stop(self):
        pass
        # self.camera.stop()


Stream = StreamNode()
