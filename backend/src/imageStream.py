from src.nodes.node_manager import NodeManager
from starlette.responses import StreamingResponse, JSONResponse
from starlette.routing import Route
from os.path import abspath, isfile
import simplejpeg
from cv2 import imread
from src.manager.camera_manager import CameraManager

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


def nodeFrameGenerator(node_id):
    fail_frame = imread(failpath)
    while True:
        try:
            frame = (NodeManager.getNodeById(node_id)).get_frame()
        except Exception:
            frame = fail_frame
        if isinstance(frame, str):
            frame = fail_frame
        encodedImage = encode(frame)
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")


def encode(frame):
    return simplejpeg.encode_jpeg(frame, colorspace="BGR", quality=90, fastdct=True)


def nodeVideoFeed(request):
    return StreamingResponse(
        nodeFrameGenerator(request.path_params["node_id"]),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


def frameGenerator(cam_id):
    cam = CameraManager.get_by_id(cam_id)
    if cam is None:
        img_fail = imread(failpath)
    while True:
        encodedImage = encode(img_fail if cam is None else cam.read())
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")


def videoFeed(request):
    if request.path_params["video_id"] not in ["null", None, "undefined"]:
        CameraManager.set_stream_id(request.path_params["video_id"])
    return JSONResponse({"selected_camera": request.path_params["video_id"]})


imgRoute = [Route("/{img_name}", endpoint=frameReader)]

videoRoute = [
    Route("/node_frame/{node_id}", endpoint=nodeVideoFeed),
    Route("/{video_id}", endpoint=videoFeed, methods=["GET", "POST"]),
]
