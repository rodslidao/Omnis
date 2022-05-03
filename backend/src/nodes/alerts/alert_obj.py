from datetime import datetime
from api.store import alerts
from api import logger, exception
from api.decorators import for_all_methods

AlertLevel = {"INFO": "INFO", "WARNING": "WARNING", "ERROR": "ERROR", "LOG": "LOG"}


@for_all_methods(exception(logger))
class AlertManager:
    async def add(alert):
        """
        Await to add alert to queue
        """
        for queue in alerts:
            await queue.put(alert)

    def put(alert):
        """
        Put alert to queue without await
        """
        for queue in alerts:
            queue.put_nowait(alert)


@for_all_methods(exception(logger))
class Alert:
    """
    Add an alert object to all subscribed queue's.
    """

    def __init__(
        self,
        level,
        title,
        description,
        how2solve="",
        buttonText="Ok",
        buttonAction="Ok",
    ):
        """
        Create a new Alert object.
        """
        self.level = level
        self.date = float(datetime.now().timestamp())
        self.title = title
        self.description = description
        self.how2solve = how2solve
        self.buttonText = buttonText
        self.buttonAction = buttonAction
        logger.debug(f"New alert created: {self}")
        AlertManager.put(self)

    def __str__(self) -> str:
        """
        Return a string representation of the Alert object.
        """
        message = ""
        for k, v in self.__dict__.items():
            message += f"{k[0].upper()}{k[1:]}:\t{v}\n"
        return message

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def dict(self):
        """
        Return a dictionary representation of the Alert object.
        """
        return self.__dict__
