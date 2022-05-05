import asyncio
from ariadne import SubscriptionType
from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager
from .store import alerts, calibrations

from api.decorators import for_all_methods
from api import logger, exception

subscription = SubscriptionType()


@for_all_methods(exception(logger))
class SubscriptionFeeder:
    def __init__(self, store):
        self.store = store

    def put(self, alert):
        """
        Put alert to queue without await
        """
        for queue in self.store:
            queue.put_nowait(alert)


@subscription.source("alerts")
async def alerts_source(obj, info):
    queue = asyncio.Queue()
    alerts.append(queue)
    try:
        while True:
            alert = await queue.get()
            print("get alert")
            yield alert
    except asyncio.CancelledError:
        print("Cancelled")
        alerts.remove(queue)
        raise


@subscription.field("alerts")
async def alerts_resolver(obj, info):
    return obj


@subscription.source("calibrations")
async def calibrations_source(obj, info):
    queue = asyncio.Queue()
    calibrations.append(queue)
    try:
        while True:
            calibration = await queue.get()
            print("get calibration")
            yield calibration
    except asyncio.CancelledError:
        print("Cancelled")
        calibrations.remove(queue)
        raise


@subscription.field("calibrations")
async def calibrations_resolver(obj, info):
    return obj


@subscription.source("cameras")
async def cameras_source(obj, info):
    queue = asyncio.Queue()
    CameraManager.queues.append(queue)
    try:
        while True:
            camera = await queue.get()
            yield camera
    except asyncio.CancelledError:
        CameraManager.queues.remove(queue)
        raise


@subscription.field("cameras")
async def cameras_resolver(obj, info):
    return obj


@subscription.source("serials")
async def serials_source(obj, info):
    queue = asyncio.Queue()
    SerialManager.queues.append(queue)
    try:
        while True:
            yield await queue.get()
    except asyncio.CancelledError:
        SerialManager.queues.remove(queue)
        raise


@subscription.field("serials")
async def serials_resolver(obj, info):
    return obj
