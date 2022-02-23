import asyncio
from .store import alerts, serials, cameras
from ariadne import SubscriptionType
from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager

subscription = SubscriptionType()


@subscription.source("alerts")
async def alerts_source(obj, info):
    print("listenning alert queue...")
    queue = asyncio.Queue()
    alerts.append(queue)
    try:
        while True:
            alert = await queue.get()
            yield alert
    except asyncio.CancelledError:
        alerts.remove(queue)
        raise


@subscription.field("alerts")
async def alerts_resolver(obj, info):
    return obj


#! Escopo de código repetido, verificar possivel solução
@subscription.source("cameras")
async def cameras_source(obj, info):
    print("listenning camera queue...")
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

#! Escopo de código repetido, verificar possivel solução
@subscription.source("serials")
async def serials_source(obj, info):
    print("listenning serial queue...")
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
