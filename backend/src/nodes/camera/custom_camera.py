from cmath import log
from src.nodes.alerts.alert_obj import Alert
from bson import ObjectId
from src.manager.camera_manager import CameraManager
from cv2 import line, putText, FONT_HERSHEY_SIMPLEX, rectangle, LINE_AA, error
from api import logger, exception, dbo
from api.decorators import for_all_methods
from vidgear.gears import CamGear
from cv2 import undistort, cvtColor, COLOR_BGR2GRAY, arcLength, VideoWriter_fourcc

from cv2.aruco import (
    DetectorParameters_create,
    Dictionary_get,
    detectMarkers,
    drawAxis,
    drawDetectedMarkers,
    estimatePoseSingleMarkers,
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
        self.aruco_parms = DetectorParameters_create()
        self.aruco_dict = Dictionary_get(ARUCO_DICT.get(self.config.get("marker_type")))
        self.fail_count = 0
        self.fail_limit = 3
        # if not disable:
        #     print(options.get("props"))
        #     self.distortion_obj = dbo.find_one(
        #         "camera-calibrations", {"_id": str(self._id)}
        #     )
        #     self.marker_len = self.distortion_obj is not None
        #     if self.marker_len:
        #         self.mtx, self.dist = array(self.distortion_obj.get("mtx")), array(
        #             self.distortion_obj.get("dist")
        #         )
        if self.opt.get("props", {}).get("CAP_PROP_FOURCC"):
            self.opt["props"]["CAP_PROP_FOURCC"] = VideoWriter_fourcc(
                *options["props"]["CAP_PROP_FOURCC"][:4]
            )
        for s in self.source:
            try:
                super().__init__(s, **self.opt.get("props"))
                logger.info(f"Camera {self.name} initialized with source {s}")
                break
            except ValueError:
                self.stop()
            except (error, RuntimeError):
                logger.warning("Camera source: {} fail".format(s))
                # super().stop()
                # continue
                # super().__init__(self.source, **self.opt.get("props"))
            # else:
            #     Alert('error', 'Camera sem resposta', 'Não foi possivel iniciar a camera', 'A fonte alternativa não responde, verifique a conexão com a camera. e reinicie o sistema.')
            #     raise RuntimeError("[Camera] Camera source invalid")
        self.start()
        CameraManager.add(self)
        
    # def run(self):
    #     try:
    #         super().run()
    def run(self):
        try:
            super().run()
        except (error, RuntimeError):
            logger.warning("Camera não sem sinal, tentando conserto automatico...")
            self.fail_count += 1
            if self.fail_count >= self.fail_limit:
                logger.warning("Camera não sem sinal, reiniciando...")
                self.fail_count = 0
                self.stop()
                self.start()
            else:
                self.run()
            # super().stop()
            # continue
            # super().__init__(self.source, **self.opt.get("props"))
    #Corrupt JPEG data: premature end of data segment
    def read(self):
        # if self.marker_len:
        #     return undistort(super().read(), self.mtx, self.dist, None)
        return super().read()

    def remove(self):
        CameraManager.remove(self)

    def get_scale(self):
        corners, _, _ = self.detect_markers()
        return self.estimate_pixel_cm_ratio(corners, self.config.get("marker_size"))

    def detect_markers(self):
        return detectMarkers(
            cvtColor(self.read(), COLOR_BGR2GRAY),
            self.aruco_dict,
            parameters=self.aruco_parms,
        )

    def draw_markers(self, size_of_marker=0.010):
        corners, ids, rejected = self.detect_markers()
        rvecs, tvecs, _ = estimatePoseSingleMarkers(
            corners, size_of_marker, self.mtx, self.dist
        )
        length_of_axis = size_of_marker / 2
        frame = drawDetectedMarkers(self.read().copy(), corners, ids)
        
        if tvecs is not None:
            for r, t in zip(rvecs, tvecs):
                frame = drawAxis(
                    frame,
                    self.mtx,
                    self.dist,
                    r,
                    t,
                    length_of_axis,
                )
        return frame
    @staticmethod
    def estimate_pixel_cm_ratio(corners, aruco_size):
        """
        Estimate the pixel to cm ratio of the aruco marker.
        :param corners: corners of the aruco marker
        :param aruco_size: size of the aruco marker
        :return: pixel to cm ratio
        """
        print(arcLength(corners[0], True)/4)

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

    def __dell__(self):
        self.stop()