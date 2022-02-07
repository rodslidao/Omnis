import asyncio
from .store import alerts
from ariadne import SubscriptionType

subscription = SubscriptionType()

@subscription.source("alerts")
async def alerts_source(obj, info):
    queue = asyncio.Queue()
    alerts.append(queue)
    try:
        while True:
            print("waiting for queue...")
            alert =  await queue.get()
            yield alert
    except asyncio.CancelledError:
        alerts.remove(queue)
        raise

@subscription.field("alerts")
async def alerts_resolver(obj, info):
    return obj