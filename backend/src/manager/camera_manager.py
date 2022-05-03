from src.manager.base_manager import BaseManager


class CameraObjectManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.stream = {}

    def broadCast(self, message):
        for ser in self.store:
            ser.send(message)

    def add(self, payload):
        super().add(payload)

        self.stream[str(payload._id)] = self.get_by_id(payload._id)
        self.stream_id = str(payload._id)

    def set_stream_id(self, stream_id):
        print("Updating stream id", stream_id)
        self.stream_id = str(stream_id)

    def __dell__(self):
        for v in self.stream.values():
            v.stop()

    def read(self):
        return self.stream[self.stream_id].read()

    def stop(self):
        for v in self.stream.values():
            v.stop()


CameraManager = CameraObjectManager()
