from src.nodes.node_manager import NodeManager
from starlette.responses import StreamingResponse
from starlette.routing import Route
from os.path import abspath, isfile
import simplejpeg, asyncio
from cv2 import imread

failpath = abspath("./src/imgs/no_image.jpg")

from src.manager.camera_manager import CameraManager
from api import logger, exception


@exception(logger)
async def frameReader(request):
    path = None
    if request:
        path = abspath(f"./src/imgs/{request.path_params['img_name']}")

    if not isfile(path):
        path, status_code = failpath, 400
    else:
        status_code = 200

    return StreamingResponse(open(path, "rb"), status_code, media_type="image/jpeg")


@exception(logger)
async def nodeFrameGenerator(node_id):
    fail_frame = imread(failpath)
    while True:
        try:
            frame = (NodeManager().getNodeById(node_id)).get_frame()
        except:
            frame = fail_frame
        encodedImage = simplejpeg.encode_jpeg(frame, colorspace="BGR")
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0.001)


@exception(logger)
async def nodeVideoFeed(request):
    return StreamingResponse(
        nodeFrameGenerator(request.path_params["node_id"]),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@exception(logger)
async def frameGenerator(cam_id):
    cam = CameraManager.get_by_id(cam_id)
    if cam is None:
        img_fail = imread(failpath)
    while True:
        encodedImage = simplejpeg.encode_jpeg(
            img_fail if cam is None else cam.read(), colorspace="BGR"
        )
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0.001)


@exception(logger)
async def videoFeed(request):
    return StreamingResponse(
        frameGenerator(request.path_params["video_id"]),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


imgRoute = [Route("/{img_name}", endpoint=frameReader)]

videoRoute = [
    Route("/node_frame/{node_id}", endpoint=nodeVideoFeed),
    Route("/{video_id}", endpoint=videoFeed),
]
