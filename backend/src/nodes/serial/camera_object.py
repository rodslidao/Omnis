import cv2
from bson.objectid import ObjectId
from time import sleep
import threading


class CameraOBJ:
    def __init__(self, src, name=None, resetOnFail=True, **kwargs) -> None:
        self.src = src
        self.name = name if name else "cam_" + str(src)
        self.id = ObjectId()
        self.resetOnFail = resetOnFail
        self.stopped = threading.Event()
        self.running = threading.Event()
        self.stream = self._open()
        self.thread = None
        if kwargs.get("properties"):
            for key, value in kwargs.get("properties").items():
                self.setPropertie(key, value)

    def _open(self):
        if not self.running.is_set():
            self.running.set()
            print("Opening camera: " + str(self.src))
            self.stream = cv2.VideoCapture(self.src)
            print("added camera: " + str(self.src))
            self.thread = threading.Thread(target=self.update, name=self.name, args=())
            self.thread.daemon = True
            self.thread.start()
            sleep(3)
        return self.stream

    def read(self):
        return self.frame

    def stop(self):
        self.stopped.set()
        self.stream.release()
        self.running.clear()

    def setPropertie(self, name, value):
        self.stream.set(getattr(cv2, "CAP_PROP_" + name), value)

    def update(self):
        while not self.stopped.is_set():
            (self.grabbed, self.frame) = self.stream.read()
            if not self.grabbed:
                raise Exception("Camera not grabbed")
        raise Exception("Camera thread stopped")

    def __del__(self):
        self.stop()
