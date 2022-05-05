from bson import ObjectId
from src.manager.camera_manager import CameraManager
from cv2 import line, putText, FONT_HERSHEY_SIMPLEX, rectangle, LINE_AA
from api import logger, exception, dbo
from api.decorators import for_all_methods
from vidgear.gears import CamGear
from cv2 import undistort
from numpy import array


@for_all_methods(exception(logger))
class Camera(CamGear):
    """_summary_

    Args:
        CamGear (_type_): _description_
    """

    def __init__(self, source=0, name="WebcamVideoStream", _id=None, **options):
        super().__init__(source, **options)
        self.start()
        self.name = name
        self.source = source
        self.opt = options
        self._id = ObjectId(_id)
        self.distortion_obj = dbo.find_one(
            "camera-calibrations", {"_id": str(self._id)}
        )
        self.marker_len = self.distortion_obj.get("markerLength")
        self.mtx, self.dist = array(self.distortion_obj.get("mtx")), array(
            self.distortion_obj.get("dist")
        )
        CameraManager.add(self)

    def read(self):
        if self.marker_len:
            return undistort(super().read(), self.mtx, self.dist, None)
        return super().read()

    def remove(self):
        CameraManager.remove(self)

    def to_dict(self):
        """
        Returns a dictionary representation of the camera.
        """
        return {
            "_id": str(self._id),
            "src": self.source,
            "name": self.name,
            "properties": self.opt,
            # "running": not self.__terminate.is_set(),
        }

    def scale_lines_draw(self):
        """
        Draw lines to scale the image.
        """
        x_size = 20
        line_qtd = 3
        line_size = 150

        for i, n in enumerate(range(10, line_size + 1, int(line_size / line_qtd))):
            line(
                self.frame,
                (int(320 - ((n) / 2)), int(240 + (i * x_size / 2))),
                (int(320 + ((n) / 2)), int(240 + (i * x_size / 2))),
                (255, 255, 255),
                thickness=1,
            )
            putText(
                self.frame,
                f"{n}",
                (int(320 - line_size / 2), int(240 + (i * x_size / 2))),
                FONT_HERSHEY_SIMPLEX,
                0.25,
                (255, 255, 255),
                1,
                LINE_AA,
            )
            rectangle(self.frame, (120, 170), (520, 310), (255, 255, 255), 1)
