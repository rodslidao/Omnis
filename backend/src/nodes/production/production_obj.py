from datetime import datetime, timedelta
from bson import ObjectId
from time import sleep
class productionOBJ():
    def __init__(self, expire_delay={'minutes':0.5}) -> None:
        self.process_seconds = None
        self.date = datetime.utcnow()
        self._id = ObjectId()
        self.st = datetime.utcnow()
        self.delay = expire_delay

    def start(self):
        self.st = datetime.utcnow()
        pass

    def finish(self, model=None, status=False):
        self.model=model
        self.status=status
        self.expire = self.date + timedelta(**self.delay)
        return self()
    
    def __call__(self):
        return {
            "_id": self._id,
            "createAt": self.date,
            "expireAt": self.expire,
            "model": self.model,
            "status": self.status,
            "process_seconds": (datetime.utcnow()-self.st).total_seconds(),
        }


