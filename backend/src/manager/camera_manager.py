from src.manager.base_manager import BaseManager


class CameraObjectManager(BaseManager):
    def __init__(self):
        super().__init__()

    def broadCast(self, message):
        for ser in self.store:
            ser.send(message)

    def add(self, payload):
        super().add(payload)

    #  This function is used to update the camera object.
    #  When something hits the url @ip:@port/videos/<camera_id>
    def set_stream_id(self, stream_id):
        self.stream_id = str(stream_id)

    def __dell__(self):
        for v in self.stream.values():
            v.stop()

    def read(self):
        return self.store[self.stream_id].read()

    def stop(self):
        for v in self.stream.values():
            v.stop()


CameraManager = CameraObjectManager()
