from api import logger, dbo
from src.manager.camera_manager import CameraManager
from cv2 import imwrite

from src.nodes.matrix.matrix_obj import Slot, Blister
try:
    cam = CameraManager.get_by_id('6244b07d3a8338aceae46cee')
    # print(
    # cam.stream.get(CAP_PROP_FRAME_HEIGHT),
    # cam.stream.get(CAP_PROP_FRAME_WIDTH)
    # )
    while True:
        scale = cam.get_scale()
        # imwrite('./test.jpg', cam.draw_markers())
        config = [(0,0), (355,210), [28.2,46], [0, 0], [10,5], [30,20]]
        A = Slot(*config, scale=1)
        B = Slot(*config, scale=scale)
        C = Blister([20,10], "LC_Simplex_Virtual", B)
        # dbo.insert_one('blister-manager', C.export())
        A = C.draw(cam.read())
        imwrite('./test.jpg', A)
        input("next..")

finally:
    dbo.close()
    CameraManager.stop()

# uvicorn.run(stremer, host="0.0.0.0", port=5555)

