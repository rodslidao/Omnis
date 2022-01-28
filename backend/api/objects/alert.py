from asyncio import queues
from datetime import  datetime
from enum import Enum
import asyncio
a = asyncio.Queue()
alerts, queues = [], [a]
class AlertLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    LOG = "LOG"

class AlertManager():

    def add(alert):
        alerts.append(alert)
        for queue in queues:
            queue.put(alert)

    def get():
        for n in alerts:
            print(n)

    def remove(alert):
        alerts.remove(alert)
        return alert

class Alert():
    def __init__(self, level, title, description, solve):
        self.level = level
        self.date = float(datetime.now().timestamp())
        self.title = title
        self.description = description
        self.how2solve = solve
        AlertManager.add(self)
    
    def __str__(self) -> str:
        message = ""
        for k,v in self.__dict__.items():
            message += f"{k[0].upper()}{k[1:]}:\t{v}\n"
        return message
        

# generate random alerts
for i in range(10):
    Alert(
        AlertLevel.INFO,
        "Info - {}".format(i),
        "This is an info alert",
        "You can solve this alert by doing something"
    )
