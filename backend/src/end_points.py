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

# imgRoute = [Route("/{img_name}", endpoint=frameReader)]

# videoRoute = [
#     # Route("/node_frame/{node_id}", endpoint=nodeVideoFeed),
#     # Route("/{video_id}", endpoint=videoFeed, methods=["GET", "POST"]),
# ]
