from datetime import datetime, timedelta
from bson import ObjectId
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
    
    # def fake_data(self):
    #     date = faker.date_time_between(start_date="-1y", end_date="now")
    
    #     return {
    #         "_id":self._id,
    #         "createAt": date,
    #         "expireAt": datetime.utcnow()+timedelta(**self.delay),
    #         "model": choice(["A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "L"]),
    #         "status": faker.boolean(),
    #         "process_seconds": faker.random_number(digits=2),
    #     }



