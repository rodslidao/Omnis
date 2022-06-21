from src.nodes.alerts.alert_obj import Alert
from src.nodes.node_manager import NodeManager
from starlette.responses import StreamingResponse, JSONResponse
from starlette.routing import Route
from os.path import abspath, isfile
import simplejpeg
from cv2 import imread, imencode
from src.manager.camera_manager import CameraManager
from vidgear.gears.asyncio.helper import reducer
import asyncio
from api import logger
from starlette.endpoints import WebSocketEndpoint
from bson import ObjectId
failpath = abspath("./src/imgs/no_image.jpg")

def frameReader(request):
    path = None
    if request:
        path = abspath(f"./src/imgs/{request.path_params['img_name']}")

    if not isfile(path):
        path, status_code = failpath, 400
    else:
        status_code = 200

    return StreamingResponse(open(path, "rb"), status_code, media_type="image/jpeg")

def encode(frame):
    return simplejpeg.encode_jpeg(frame, colorspace="BGR", quality=90, fastdct=True)

async def frame_producer(_id='default'):
    while True:
        yield (b"--frame\r\nContent-Type:video/jpeg2000\r\n\r\n" + imencode(".jpg", await reducer(CameraManager.read(_id), percentage=75))[1].tobytes() + b"\r\n")
        await asyncio.sleep(0.00001)

async def custom_video_response(scope):
    """
    Return a async video streaming response for `frame_producer2` generator
    """
    logger.info(scope)
    assert scope["type"] in ["http", "https"]
    await asyncio.sleep(0.00001)
    return StreamingResponse(
        frame_producer(scope.path_params.get('video_id', 'default')),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )

from starlette.websockets import WebSocket

class Echo(WebSocketEndpoint):
    encoding = "json"
    _id = None

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        node_id = data.get("nodeId")
        if node_id:
            running_node = NodeManager.getNodeById(node_id)
            if running_node:
                running_node.update_options(data['options'])
        await websocket.send_json({"echo": data['options']})

    async def on_disconnect(self, websocket, close_code=100):
        print("disconnected")

control_sessions= {}

class Controls(WebSocketEndpoint):
    encoding = "json"
    def __init__(self, _id, serial):
        self._id = _id
        self.serial = serial

    def __call__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        return self
        
    async def relay(queue, websocket):
        while True:
            message = await queue.get()
            await websocket.send(message)
            
    async def on_connect(self, websocket):
        await websocket.accept()
        if control_sessions.get(self._id) is not None:
            control_sessions[self._id].add(websocket)
        else:
            control_sessions[self._id] = set([websocket])
        
    async def on_receive(self, websocket, data):
        if data["context"] == "movementScale":
            # Define a escala de movimento
            for axis in self.serial.axes.values():
                axis.step = float(data["value"])

        elif data["context"] == "joggingDistance":
            # Move a distancia especificada
            axis = self.serial.axes[data["id"]]
            axis.move(data["value"])
            axis.position=self.serial.G0(axis())[axis.name]

        elif data["context"] == "outputDevices":
            # Ativa ou desativa os dispositivos de saida
            self.serial.send(self.serial.pins[data["id"]].set_value(data["pwm"]))

        elif data["context"] == "joggingStep":
            # Movimento "Relativo"
            axis = self.serial.axes[data["id"]]
            axis.move(axis.position + axis.step * (1 if not data['isNegative'] else -1))
            axis.position=self.serial.G0(axis())[axis.name]
        else:
            logger.info(data)

        await websocket.send_json({"respose":'ok'})

    async def update_client_message(self, payload:dict):
        for session in control_sessions.get(self._id):
            await session.send_json(payload)
    
    async def on_disconnect(self, websocket, close_code=100):
        control_sessions.get(self._id, set()).remove(websocket)
        logger.info(f"{len(control_sessions.get(self._id))} remaining sessions")