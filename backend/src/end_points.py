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

control_clients = {}
class Controls(WebSocketEndpoint):
    encoding = "json"
    def __init__(self, _id):
        self._id = _id

    def __call__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        return self
        
    async def relay(queue, websocket):
        while True:
            message = await queue.get()
            await websocket.send(message)
            
    async def on_connect(self, websocket):
        await websocket.accept()
        control_clients[self._id] = websocket
        
    # async def on_receive(self, websocket, data):        
    #     await websocket.send_json({"respose":'ok'})

    async def update_client_message(self, payload:dict):
        if control_clients.get(self._id):
            await control_clients.get(self._id).send_json(payload)
    
    async def on_disconnect(self, websocket, close_code=100):
        control_clients.pop(self._id, 'default')