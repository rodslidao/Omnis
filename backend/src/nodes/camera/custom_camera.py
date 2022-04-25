from bson import ObjectId
from numpy import ascontiguousarray
from src.manager.camera_manager import CameraManager
from threading import Thread
from time import sleep
from time import sleep

import cv2
import datetime

from api import logger, exception, for_all_methods


@for_all_methods(exception(logger))
class FPS:
    """
    FPS class for calculating frames per second. \n

    Usage: \n
    \tFPS().start():\t-> returns FPS() itself and start the counter \n
    \tFPS().update():\t returns None and updates the counter \n
    \tFPS().fps():\t\t returns the current FPS

    """

    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def update(self):
        if self.elapsed() >= 5:
            self._numFrames = 0
            self.start()
        self._numFrames += 1

    def elapsed(self):
        return (datetime.datetime.now() - self._start).total_seconds()

    def fps(self):
        return self._numFrames / self.elapsed()


@for_all_methods(exception(logger))
class camera:
    """
    Complex api for USB cameras.
    When a new camera is started, it will be added to the CameraManager using camera._id as key.
    When a camera is stopped, it will be removed from the CameraManager.

    :set_property(name, value):
        Set a property of the camera.
        a list of properties can be found here: https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html

    :get_property(name):
        Get a property of the camera.

    :get_properties():
        Get all properties of the camera.

    :start():
        Start the camera.
        returns self.

    :stop():
        Stop the camera.
        returns self.

    :reset():
        Reset the camera.
        returns self.

    :read():
        Read the current frame.
        returns the current frame.

    :to_dict():
        Returns a dictionary representation of the camera.


    """

    def __init__(self, src=0, name="WebcamVideoStream", _id=None):
        self.src = src

        # Todo: Test another back_end API for camera.
        self.stream = cv2.VideoCapture(src)#, cv2.CAP_V4L2)

        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

        #! That is not ideal, properties should be set in the constructor as **keyword arguments
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.name = name
        self._id = ObjectId(_id)
        self.stopped = True
        self.t = None
        self.properties = {}
        if self.stream.isOpened():
            (self.grabbed, self.frame) = self.stream.read()
            cv2.imwrite("./frame.jpg", self.read())
        self.start()
        CameraManager.add(self)

    def set_property(self, name, value):
        self.stream.set(getattr(cv2, name) if isinstance(name, str) else name, value)

    def set_properties(self, properties):
        for name, value in properties.items():
            self.set_property(name, value)

    def reset(self):
        logger.info("Resetting camera")
        self.stopped = True
        CameraManager.update()
        self.start()
        return self

    def start(self):
        """
        Start the camera.
        returns self.
        """
        if self.stopped:
            self.stopped = False
            self.t = Thread(
                target=self.updateFrame, name=self.name, args=(), daemon=True
            )
            self.t.start()
            CameraManager.update()
        return self

    def updateFrame(self):
        """
        Update the frame of the camera.
        returns None.
        """
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
            self.scale_lines_draw()

    def read(self):
        """
        Read the current frame.
        returns the current frame.
        """

        #! Do not use this, the ROI needs to be set in the constructor, or another node should be used.
        # return ascontiguousarray(self.frame[130:350, 120:520])
        return self.frame

    def stop(self):
        """
        Stop the camera.
        returns self.
        """
        self.stopped = True
        try:
            self.t.join()
        except RuntimeError:
            pass
        CameraManager.update()
        return self

    def remove(self):
        CameraManager.remove(self)

    def __del__(self):
        if not self.stopped:
            self.stop()
        self.stream.release()

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


def checker(src=2):
    """
    Checks if the camera is running.
    """
    cam = camera(src)
    cam.start()
    sleep(src)
    cam.stop()
