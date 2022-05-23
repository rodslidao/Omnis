import asyncio
from ariadne import SubscriptionType
from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager
from .store import alerts, calibrations, nodes

from api.decorators import for_all_methods
from api import logger, exception

subscription = SubscriptionType()

"""
Create a decorator to pass (self.name) attribute from SubscriptionFactory method decorated with @subscription.source(self.name)
"""

@for_all_methods(exception(logger))
class SubscriptionFactory:
    def __init__(self, store, name):
        self.store = store
        self.name = name

        @subscription.source(self.name)
        async def alerts_source(obj, info):
            queue = asyncio.Queue()
            self.store.append(queue)
            try:
                while True:
                    yield await queue.get()
            except asyncio.CancelledError:
                self.store.remove(queue)
                raise

        @subscription.field(self.name)
        async def sub_resolver(obj, info):
            return obj

    def put(self, alert):
        """
        Put alert to queue without await
        """
        for queue in self.store:
            queue.put_nowait(alert)
