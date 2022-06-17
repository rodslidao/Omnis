from datetime import datetime
from api.store import alerts
from api import logger, exception
from api.decorators import for_all_methods
from api.subscriptions import SubscriptionFactory

AlertLevel = {"INFO": "INFO", "WARNING": "WARNING", "ERROR": "ERROR", "LOG": "LOG"}

AlertManager = SubscriptionFactory(alerts, 'alerts')

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
        how_to_solve="",
        button_text="Ok",
        button_action="Ok",
        delay=0,
    ):
        """
        Create a new Alert object.
        """
        self.level = level 
        self.date = float(datetime.now().timestamp())
        self.title = title
        self.description = description
        self.how_to_solve = how_to_solve
        self.button_text = button_text
        self.button_action = button_action
        getattr(logger, self.level.lower())(f"{self.items()}")
        AlertManager.put(self)

    def __str__(self) -> str:
        """
        Return a string representation of the Alert object.
        """
        message = ""
        for k, v in self.items():
            message += f"{k[0].upper()}{k[1:]}:\t{v}\n"
        return message

    def __repr__(self) -> str:
        return str(self)

    def items(self):
        """
        Return a dictionary representation of the Alert object.
        """
        return vars(self)
