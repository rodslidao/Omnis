from email.policy import default
from .models import *
from ariadne import MutationType
from src.nodes.alerts.alert_obj import Alert
from numpy import uint8, frombuffer
from cv2 import imdecode, imwrite
from os.path import abspath

from src.nodes.camera.custom_camera import camera
from src.nodes.serial.custom_serial import CustomSerial

from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager

mutation = MutationType()


@defaultException
@mutation.field("createNodeSheet")
def createNodeSheet_resolver(obj, info, _id, **kwargs):
    """Create a new NodeSheet object and return it like a payload"""
    print(kwargs)
    returns = NodeSheet().createNodeSheet(_id, **kwargs)
    return {"data": returns}


@defaultException
@mutation.field("updateNodeSheet")
def updateNodeSheet_resolver(obj, info, _id, **kwargs):
    """Update a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().updateNodeSheet(_id, **kwargs)
    return {"data": returns}


@defaultException
@mutation.field("deleteNodeSheet")
def deleteNodeSheet_resolver(obj, info, id):
    """Delete a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().deleteNodeSheet(id)
    return {"data": returns}


@defaultException
@mutation.field("startProcess")
def startProcess_resolver(obj, info):
    """Start a process by id and return it like a payload"""
    process.startProcess()
    returns = process.dict()
    return {"data": returns}


@defaultException
@mutation.field("stopProcess")
def stopProcess_resolver(obj, info):
    """Stop a process by id and return it like a payload"""
    process.stopProcess()
    returns = process.dict()
    return {"data": returns}


@defaultException
@mutation.field("pauseProcess")
def pauseProcess_resolver(obj, info):
    """Pause a process by id and return it like a payload"""
    process.pauseProcess()
    returns = process.dict()
    return {"data": returns}


@defaultException
@mutation.field("resumeProcess")
def resumeProcess_resolver(obj, info):
    """Resume a process by id and return it like a payload"""
    process.resumeProcess()
    returns = process.dict()
    return {"data": returns}


@defaultException
@mutation.field("loadConfig")
def loadConfig_resolver(obj, info, _id):
    try:
        LastValue.loadConfig(_id)
        return True
    except Exception as e:
        print(e)
        return False


@defaultException
@mutation.field("getLoadedConfig")
def getLoadedConfig_resolver(obj, info):
    try:
        return LastValue.getLoadedConfig()
    except Exception as e:
        print(e)
        return False


@defaultException
@mutation.field("createAlert")
async def createAlert_resolver(obj, info, input):
    """Create a new Alert object and return it like a payload"""
    returns = Alert(**input)
    return {"data": returns}


@defaultException
@mutation.field("uploadFile")
async def uploadFile_resolver(obj, info, file):
    """Upload a file and return it like a payload"""
    print(file)
    return {"data": file}


class Picutre:
    def __init__(self, name, _id=ObjectId()):
        self._id = _id
        self.name = name[:-3]
        self.extension = name[-3:]
        self.path = f"/imgs/{self._id}"

    def export(self, path, img):
        """Export the picture to the path"""
        imwrite(path, img)
        return self.__dict__


@defaultException
@mutation.field("uploadPhoto")
async def uploadPhoto_resolver(obj, info, **kwargs):
    name = kwargs.get("photo").filename
    p = Picutre(name)
    path = f"{abspath('./src')}/{p.path}"
    img = imdecode(frombuffer(kwargs.get("photo").file.read(), uint8), 1)
    print(p.export(path, img))
    return {"filename": p.id, "path": p.path}


# @mutation.field("createNode") #? Como criar novos nodes de forma dinamica e individual?

# *  ----------- Cameras ----------- * #
@defaultException
@mutation.field("createCamera")
def createCamera_resolver(obj, info, **kwargs):
    """Create a new Camera object and return it like a payload"""
    returns = camera(**kwargs.get("input", {})).to_dict()
    return {"data": returns}


@defaultException
@mutation.field("startCamera")
def startCamera_resolver(obj, info, _id):
    """Start a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id)).start()
    returns = camera.to_dict()
    return {"data": returns}


@defaultException
@mutation.field("stopCamera")
def stopCamera_resolver(obj, info, _id):
    """Stop a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id)).stop()
    returns = camera.to_dict()
    return {"data": returns}


@defaultException
@mutation.field("resetCamera")
def resetCamera_resolver(obj, info, _id):
    """Reset a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id)).reset()
    returns = camera.to_dict()
    return {"data": returns}


@defaultException
@mutation.field("setCameraProperty")
def setCameraProperty_resolver(obj, info, _id, **kwargs):
    """Set a camera property by id and return it like a payload"""
    camera = CameraManager.get_by_id(_id)
    returns = camera.set_properties(kwargs.get("input", {}))
    return {"data": returns}


# *  ----------- Serial ----------- * #
@defaultException
@mutation.field("createSerial")
def createSerial_resolver(obj, info, **kwargs):
    """Create a new Serial object and return it like a payload"""
    returns = CustomSerial(**kwargs.get("input", {})).to_dict()
    return {"data": returns}


@defaultException
@mutation.field("startSerial")
def startSerial_resolver(obj, info, _id):
    """Start a serial by id and return it like a payload"""
    serial = SerialManager.get_by_id(_id).start()
    returns = serial.to_dict()
    return {"data": returns}


@defaultException
@mutation.field("stopSerial")
def stopSerial_resolver(obj, info, _id):
    """Stop a serial by id and return it like a payload"""
    serial = SerialManager.get_by_id(_id).stop()
    returns = serial.to_dict()
    return {"data": returns}


@defaultException
@mutation.field("communicateSerial")
def communicateSerial_resolver(obj, info, _id, payload):
    """Communicate a serial by id and return it like a payload"""
    serial = SerialManager.get_by_id(_id)
    serial.send(payload)
    print("ok")
    return {"status": True, "data": serial.to_dict()}
