import cv2
from starlette.responses import StreamingResponse
from starlette.routing import Route
from os.path import abspath, isfile
import simplejpeg, asyncio
from cv2 import imread
failpath = abspath("./src/imgs/no_image.jpg")

from src.manager.camera_manager import CameraManager

async def frameReader(request):
    if request:
        path = abspath(f"./src/imgs/{request.path_params['img_name']}")
    else:
        path = ".s"
    if isfile(path):
        img = open(path, 'rb')
        status_code = 200
    else:
        img = open(failpath, 'rb')
        status_code = 404
    return StreamingResponse(img, status_code, media_type="image/jpeg")

async def frameGenerator(cam_id):
    cam = CameraManager.get_by_id(cam_id)
    if cam is None: img_fail = imread(failpath)
    while True:
        encodedImage = simplejpeg.encode_jpeg(
                    img_fail if cam is None else cam.read(),
                    colorspace="BGR"
                )
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0.001)

async def videoFeed(request):
    print(request.path_params)
    return StreamingResponse(frameGenerator(request.path_params['video_id']), media_type="multipart/x-mixed-replace; boundary=frame")

imgRoute = [
    Route("/{img_name}", endpoint=frameReader)
]

videoRoute = [
    Route("/{video_id}", endpoint=videoFeed)
]
