import asyncio
import queue
from ariadne import SubscriptionType

from api.decorators import for_all_methods
from api import logger, exception

subscription = SubscriptionType()

"""
Create a decorator to pass (self.name) attribute from SubscriptionFactory method decorated with @subscription.source(self.name)
"""

@for_all_methods(exception(logger))
class SubscriptionFactory:
    def __init__(self, store, name):
        self.store = asyncio.Queue()
        self.name = name

        @subscription.source(self.name)
        async def alerts_source(obj, info):
            try:
                while True:
                    yield await self.store.get()
            finally:
                logger.debug(f"Subscription: {self.name} closing...")

        @subscription.field(self.name)
        async def sub_resolver(obj, info):
            return obj
    
    def put(self, info):
        """
        Send a message to the subscription queue.
        info (dict): message to be sent.
        """
        self.store.put_nowait(dict(info.items()))