from bson import ObjectId
import cv2
from threading import Thread
from time import sleep
from src.manager.camera_manager import CameraManager
from time import sleep

import datetime
class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def update(self):    
        self._numFrames += 1
        if self._numFrames >= 1000: 
            self._numFrames = 0
            self.start()


    def elapsed(self):
        return (datetime.datetime.now() - self._start).total_seconds()

    def fps(self):
        return self._numFrames / self.elapsed()

class camera:
    def __init__(self, src=0, name="WebcamVideoStream"):
        self.src = src
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            raise ValueError("Camera not found")
        (self.grabbed, self.frame) = self.stream.read()
        self.name = name
        self._id = ObjectId()
        self.stopped = True
        self.properties = {}
        CameraManager.add(self)

    def setPropertie(self, name, value):
        self.stream.set(getattr(cv2, name), value)
    
    def setProperties(self, properties):
        for name, value in properties.items():
            self.setPropertie(name, value)

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
        self.t = Thread(target=self.updateFrame, name=self.name, args=(), daemon = True)
        self.t.start()
        CameraManager.update()
        return self

    def updateFrame(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
            cv2.putText(self.frame, "FPS: {:.2f}".format(self.fps.fps()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            self.fps.update()

    def read(self):
        return self.frame

    def stop(self):
        print("Stopping camera...")
        self.fps.stop()
        self.stopped = True
        try:
            self.t.join()
        except RuntimeError:
            pass
        CameraManager.remove(self)
        return self
    
    def __del__(self):
        if not self.stopped: self.stop()
        self.stream.release()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "src": self.src,
            "name": self.name,
            "properties": self.properties,
            "running": not self.stopped
        }                


def checker():
    cam = camera(2)
    cam.start()
    sleep(2)
    cam.stop()