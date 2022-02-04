
from datetime import  datetime
from ssl import AlertDescription
from api.store import alerts


AlertLevel ={
    "INFO":"INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "LOG": "LOG"
}

class AlertManager():
    
    async def add(alert):
        for queue in alerts:
            await queue.put(alert)
    
    def put(alert):
        for queue in alerts:
            queue.put_nowait(alert)


class Alert():
    def __init__(self, level, title, description, how2solve="", buttonText="Ok", buttonAction="Ok"):
        self.level = level
        self.date = float(datetime.now().timestamp())
        self.title = title
        self.description = description
        self.how2solve = how2solve
        self.buttonText = buttonText
        self.buttonAction = buttonAction
        AlertManager.put(self)
        #await AlertManager.add(self)
        
            
    def __str__(self) -> str:
        message = ""
        for k,v in self.__dict__.items():
            message += f"{k[0].upper()}{k[1:]}:\t{v}\n"
        return message

    @classmethod
    def dict(self):
        return self.__dict__
