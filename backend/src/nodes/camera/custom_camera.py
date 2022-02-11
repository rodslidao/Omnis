from bson import ObjectId
import cv2
from threading import Thread
from time import sleep
from src.manager.camera_manager import CameraManager
from time import sleep

import datetime
from collections import deque

class FPS:
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


class camera:
    def __init__(self, src=0, name="WebcamVideoStream"):
        self.src = src
        self.stream = cv2.VideoCapture(src, cv2.CAP_V4L2)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.name = name
        self._id = ObjectId()
        self.stopped = True
        self.properties = {}
        if self.stream.isOpened():
            (self.grabbed, self.frame) = self.stream.read()
            CameraManager.add(self)

    def set_property(self, name, value):
        self.stream.set(getattr(cv2, name) if isinstance(name, str) else name, value)

    def set_properties(self, properties):
        for name, value in properties.items():
            self.set_property(name, value)

    def reset(self):
        print("Resetting camera...")
        self.stopped = True
        CameraManager.update()
        self.start()
        return self

    def start(self):
        print("Starting camera...")
        self.fps = FPS().start()
        self.stopped = False
        self.t = Thread(target=self.updateFrame, name=self.name, args=(), daemon=True)
        self.t.start()
        CameraManager.update()
        return self

    def updateFrame(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
            cv2.putText(
                self.frame,
                "FPS: {:.2f}".format(self.fps.fps()),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            self.fps.update()

    def read(self):
        return self.frame

    def stop(self):
        print("Stopping camera...")
        # self.fps.stop()
        self.stopped = True
        try:
            self.t.join()
        except RuntimeError:
            pass
        CameraManager.remove(self)
        return self

    def __del__(self):
        if not self.stopped:
            self.stop()
        self.stream.release()

    def to_dict(self):
        return {
            "_id": self._id,
            "src": self.src,
            "name": self.name,
            "properties": self.properties,
            "running": not self.stopped,
        }


def checker():
    cam = camera(2)
    cam.start()
    sleep(2)
    cam.stop()
