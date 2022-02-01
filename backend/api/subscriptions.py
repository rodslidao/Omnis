import asyncio
from .store import alerts
from ariadne import SubscriptionType

subscription = SubscriptionType()

@subscription.source("alerts")
async def alerts_source(obj, info):
    queue = asyncio.Queue()
    alerts.append(queue)
    # queue = queues[0]
    # print("queues:", queues)
    try:
        while True:
            print("waiting for queue...")
            alert =  await queue.get() #{"level":"info2"}
            # print(alert.level)
            yield alert
    except asyncio.CancelledError:
        alerts.remove(queue)
        raise

@subscription.field("alerts")
async def alerts_resolver(obj, info):
    return obj