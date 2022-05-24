from bson import ObjectId
from src.manager.camera_manager import CameraManager
from cv2 import line, putText, FONT_HERSHEY_SIMPLEX, rectangle, LINE_AA
from api import logger, exception, dbo
from api.decorators import for_all_methods
from vidgear.gears import CamGear
from cv2 import undistort, cvtColor, COLOR_BGR2GRAY, arcLength

from cv2.aruco import (
    DetectorParameters_create,
    Dictionary_get,
    detectMarkers,
)

from numpy import array, mean
from src.utility.image_processing.guess_aruco_type import ARUCO_DICT


@for_all_methods(exception(logger))
class Camera(CamGear):
    """_summary_

    Args:
        CamGear (_type_): _description_
    """

    def __init__(
        self,
        source=0,
        name="WebcamVideoStream",
        _id=None,
        disable=False,
        **options,
    ):
        self._id = ObjectId(_id)
        self.name = name
        self.source = source
        self.opt = options
        self.config = options.get("config")
        if not disable:
            print(options.get("props"))
            self.distortion_obj = dbo.find_one(
                "camera-calibrations", {"_id": str(self._id)}
            )
            self.marker_len = self.distortion_obj is not None
            if self.marker_len:
                self.mtx, self.dist = array(self.distortion_obj.get("mtx")), array(
                    self.distortion_obj.get("dist")
                )
            super().__init__(source, **options.get("props"))
            self.start()
            CameraManager.add(self)

    def read(self):
        # if self.marker_len:
        #     return undistort(super().read(), self.mtx, self.dist, None)
        return super().read()

    def remove(self):
        CameraManager.remove(self)

    def get_scale(self):
        parameters = DetectorParameters_create()
        aruco_dict = Dictionary_get(ARUCO_DICT.get(self.config.get("marker_type")))
        corners, _, _ = detectMarkers(
            cvtColor(self.read(), COLOR_BGR2GRAY),
            aruco_dict,
            parameters=parameters,
        )
        return self.estimate_pixel_cm_ratio(corners, self.config.get("marker_size"))

    @staticmethod
    def estimate_pixel_cm_ratio(corners, aruco_size):
        """
        Estimate the pixel to cm ratio of the aruco marker.
        :param corners: corners of the aruco marker
        :param aruco_size: size of the aruco marker
        :return: pixel to cm ratio
        """
        print(len(corners))

        return mean([arcLength(corner, True) / (aruco_size * 4) for corner in corners])

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

    def __str__(self) -> str:
        return str(self.to_dict())

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
