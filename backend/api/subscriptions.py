import asyncio
from .objects.alert import queues
from ariadne import SubscriptionType

subscription = SubscriptionType()

@subscription.source("alerts")
async def alerts_source(obj, info):
    queue = asyncio.Queue()
    queues.append(queue)
    print("queues:", queues)
    try:
        while True:
            alert =  {"level":"info2"}
            yield alert
    except asyncio.CancelledError:
        queues.remove(queue)
        raise

@subscription.field("alerts")
async def alerts_resolver(obj, info):
    print(obj)
    return obj