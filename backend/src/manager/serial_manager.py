from src.manager.base_manager import BaseManager

class SerialObjectManager(BaseManager):
    def __init__(self):
        super().__init__()

    def broadCast(self, message):
        for ser in self.store:
            ser.send(message)

SerialManager = SerialObjectManager()