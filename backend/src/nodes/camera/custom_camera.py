from bson import ObjectId
import cv2
from threading import Thread
from time import sleep
from src.manager.camera_manager import CameraManager
class camera:
    def __init__(self, src=0, name="WebcamVideoStream"):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.name = name
        self._id = ObjectId()
        self.stopped = False
        self.t = Thread(target=self.update, name=self.name, args=(), daemon = True)
        CameraManager.add(self)

    def setPropertie(self, name, value):
        self.stream.set(getattr(cv2, name), value)
    
    def setProperties(self, properties):
        for name, value in properties.items():
            self.setPropertie(name, value)

    def start(self):
        self.t.start()
        return self

    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.t.join()
        CameraManager.remove(self)
    
    def __del__(self):
        if not self.stopped: self.stop()
        self.stream.release()

def checker():
    cam = camera(2)
    cam.start()
    sleep(2)
    cam.stop()