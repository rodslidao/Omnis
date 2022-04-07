from src.manager.camera_manager import CameraManager
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.camera.custom_camera import camera
from src.nodes.timer.task_time import setInterval
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
        self.camera_id = options['hardware']['camera_id']
        self.camera = CameraManager.get_by_id(self.camera_id ).start()
#        self.stop_events = set()
        #self.execute = setInterval(0.5, self.stop_event, "CameraNode")(self.execute)
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    #@setInterval(0.5, "CameraNode")
    @exception(logger)
    def execute(self, message=""):
        self.onSuccess(self.get_frame())

        # except Exception as e:
        #     self.camera.reset()
            # self.onFailure("Cant read camera frame", pulse=True, errorMessage=str(e))

    @exception(logger)
    def get_frame(self):
        return self.camera.read()

    # @exception(logger)
    # def stop(self):
    #     list(map(lambda x: x.set(), self.stop_events))
    #     print("Camera_Stopped")

    # @exception(logger)
    # def reset(self):
    #     self.stop()
    #     self.stop_events = set()
    #     self.execute = setInterval(0.5, self.stop_events, "CameraNode")(self.execute)

    @staticmethod
    @exception(logger)
    def get_info():
        info = {}
        print(CameraManager.get())
        info["options"] = {"hardware": CameraManager.get()}
        return info
