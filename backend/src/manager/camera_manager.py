from src.manager.base_manager import BaseManager
from api import logger

class CameraObjectManager(BaseManager):
    def __init__(self):
        super().__init__()

    def broadCast(self, message):
        for ser in self.store:
            ser.send(message)

    def add(self, payload):
        super().add(payload)
        if len(self.store) == 1:
            self.store['default'] = payload

    def __dell__(self):
        for v in self.store.values():
            v.stop()

    def read(self, stream_id='default'):
        return self.store.get(stream_id, self.store['default']).read()

    def stop(self):
        for v in self.store.values():
            v.stop()


CameraManager = CameraObjectManager()
