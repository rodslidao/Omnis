import asyncio
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
        self.store = store
        self.name = name

        @subscription.source(self.name)
        async def alerts_source(obj, info):
            queue = asyncio.Queue()
            self.store.append(queue)
            try:
                while True:
                    # value = 
                    # queue.task_done()
                    yield await queue.get()
            # except asyncio.CancelledError:
            #     pass 
            except Exception as e:
                queue.task_done()
                raise  
            finally:
                self.store.remove(queue)

        @subscription.field(self.name)
        async def sub_resolver(obj, info):
            return obj

    def put(self, info):
        """
        Send a message to the subscription queue.
        info (dict): message to be sent.
        """
        for queue in self.store:
            queue.put_nowait(dict(info.items()))
