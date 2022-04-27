from bson import ObjectId
from numpy import ascontiguousarray
from src.manager.camera_manager import CameraManager
from threading import Thread
from time import sleep
from time import sleep

import cv2
import datetime

from api import logger, exception, for_all_methods
from vidgear.gears import CamGear
@for_all_methods(exception(logger))
class camera(CamGear):
    def __init__(self, source=0, name="WebcamVideoStream", _id=None, **options):
        super().__init__(source, **options)
        self.start()
        self.name = name
        self._id = ObjectId(_id)
        CameraManager.add(self)

    def remove(self):
        CameraManager.remove(self)

    def to_dict(self):
        """
        Returns a dictionary representation of the camera.
        """
        return {
            "_id": str(self._id),
            "src": self.src,
            "name": self.name,
            "properties": self.properties,
            "running": not self.stopped,
        }

    def scale_lines_draw(self):
        x, y = 20, 300
        l = 3
        s = 150

        for i, n in enumerate(range(10, s + 1, int(s / l))):
            cv2.line(
                self.frame,
                (int(320 - ((n) / 2)), int(240 + (i * x / 2))),
                (int(320 + ((n) / 2)), int(240 + (i * x / 2))),
                (255, 255, 255),
                thickness=1,
            )
            cv2.putText(
                self.frame,
                f"{n}",
                (int(320 - s / 2), int(240 + (i * x / 2))),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.25,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

        cv2.rectangle(self.frame, (120, 170), (520, 310), (255, 255, 255), 1)
