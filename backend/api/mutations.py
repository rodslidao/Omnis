from pickle import TRUE
from turtle import update
from .models import NodeSheet, ObjectId
from ariadne import MutationType
from src.nodes.alerts.alert_obj import Alert
from numpy import uint8, frombuffer
from cv2 import imdecode, imwrite, log
from os.path import abspath

from src.nodes.camera.custom_camera import Camera
from src.nodes.serial.custom_serial import Serial

from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager

from src.nodes.process.process import process

from src.utility.system.date import set_system_date
from api import logger, auth, dbo

mutation = MutationType()


@mutation.field("createNodeSheet")
@auth('manager')
def createNodeSheet_resolver(obj, info, _id, **kwargs):
    """Create a new NodeSheet object and return it like a payload"""
    returns = NodeSheet().create_node_sheet(_id, **kwargs)
    return  returns


@mutation.field("saveNodeSheet")
@auth('manager')
def saveNodeSheet_resolver(obj, info, _id=None, **kwargs):
    """Create a new NodeSheet object and return it like a payload"""
    returns = NodeSheet().save_node_sheet(_id, **kwargs)
    return {"data": returns}


@mutation.field("updateNodeSheet")
@auth('manager')
def updateNodeSheet_resolver(obj, info, _id, **kwargs):
    """Update a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().update_node_sheet(_id, **kwargs)
    return  returns



@mutation.field("deleteNodeSheet")
@auth('manager')
def deleteNodeSheet_resolver(obj, info, _id):
    """Delete a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().delete_node_sheet(_id)
    return  returns

@mutation.field("duplicateNodeSheet")
@auth('manager')
def duplicateNodeSheet_resolver(obj, info, _id):
    """Duplicate a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().duplicate_node_sheet(_id)
    return  returns

@mutation.field("startProcess")
@auth('operator')
def startProcess_resolver(obj, info, _id):
    """Start a process by id and return it like a payload"""
    process.start(_id)
    return


@mutation.field("stopProcess")
@auth('operator')
def stopProcess_resolver(obj, info):
    """Stop a process by id and return it like a payload"""
    process.stop()
    return 


@mutation.field("pauseProcess")
@auth('operator')
def pauseProcess_resolver(obj, info):
    """Pause a process by id and return it like a payload"""
    process.pause()
    return


@mutation.field("resumeProcess")
@auth('operator')
def resumeProcess_resolver(obj, info):
    """Resume a process by id and return it like a payload"""
    process.resume()
    return 


@mutation.field("loadConfig")
@auth('operator')
def loadConfig_resolver(obj, info, _id):
    process.load(_id)
    logger.debug("Query Loaded config with id {}".format(_id))
    return NodeSheet().getNodeSheetById(_id)


@mutation.field("getLoadedConfig")
@auth('viewer')
def getLoadedConfig_resolver(obj, info):
    return process.getLoadedId()


@mutation.field("createAlert")
@auth('developer')
async def createAlert_resolver(obj, info, input):
    """Create a new Alert object and return it like a payload"""
    returns = Alert(**input)
    return {"data": returns}


@mutation.field("uploadFile")
async def uploadFile_resolver(obj, info, file):
    """Upload a file and return it like a payload"""
    print(file)
    return {"data": file}


class Picture:
    def __init__(self, name, _id=ObjectId()):
        self._id = _id
        self.name = name[:-3]
        self.extension = name[-3:]
        self.path = f"/imgs/{self._id}"

    def export(self, path, img):
        """Export the picture to the path"""
        imwrite(path, img)
        return self.__dict__


@mutation.field("uploadPhoto")
async def uploadPhoto_resolver(obj, info, **kwargs):
    name = kwargs.get("photo").filename
    p = Picture(name)
    path = f"{abspath('./src')}/{p.path}"
    img = imdecode(frombuffer(kwargs.get("photo").file.read(), uint8), 1)
    print(p.export(path, img))
    return {"filename": p.id, "path": p.path}
    
@mutation.field("takePhoto")
async def takePhoto_resolver(obj, info, **kwargs):
    camera_id = kwargs.get("camera_id")
    p = Picture(str(camera_id))
    path = f"{abspath('./src')}/{p.path}{p.name}.jpeg"
    img = CameraManager.get_by_id(camera_id).read()
    print(p.export(path, img))
    return {"filename": p._id, "path": p.path}

# *  ----------- Cameras ----------- * #
@mutation.field("createCamera")
def createCamera_resolver(obj, info, **kwargs):
    """Create a new Camera object and return it like a payload"""
    returns = Camera(**kwargs.get("input", {})).to_dict()
    return {"data": returns}


@mutation.field("startCamera")
def startCamera_resolver(obj, info, _id):
    """Start a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id))
    returns = camera.to_dict()
    return {"data": returns}


@mutation.field("stopCamera")
def stopCamera_resolver(obj, info, _id):
    """Stop a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id)).stop()
    returns = camera.to_dict()
    return {"data": returns}


@mutation.field("resetCamera")
def resetCamera_resolver(obj, info, _id):
    """Reset a camera by id and return it like a payload"""
    camera = (CameraManager.get_by_id(_id)).reset()
    returns = camera.to_dict()
    return {"data": returns}


@mutation.field("setCameraProperty")
def setCameraProperty_resolver(obj, info, _id, **kwargs):
    """Set a camera property by id and return it like a payload"""
    camera = CameraManager.get_by_id(_id)
    returns = camera.set_properties(kwargs.get("input", {}))
    return {"data": returns}


# *  ----------- Serial ----------- * #
@mutation.field("createSerial")
def createSerial_resolver(obj, info, **kwargs):
    """Create a new Serial object and return it like a payload"""
    returns = Serial(**kwargs.get("input", {})).to_dict()
    return  returns


@mutation.field("startSerial")
def startSerial_resolver(obj, info, _id):
    """Start a serial by id and return it like a payload"""
    serial = SerialManager.get_by_id(_id)
    returns = serial.to_dict()
    return  returns


@mutation.field("stopSerial")
def stopSerial_resolver(obj, info, _id):
    """Stop a serial by id and return it like a payload"""
    serial = SerialManager.get_by_id(_id).stop()
    returns = serial.to_dict()
    return  returns


@mutation.field("sendSerial")
@auth('operator')
def sendSerial_resolver(obj, info, _id, payload):
    """Communicate a serial by id and return it like a payload"""
    return SerialManager.get_by_id(_id).send(payload).to_dict()


@mutation.field("syncHostTime")
def syncHostTime_resolver(obj, info, timestamp):
    """Sync the host time with the server time"""
    try:
        set_system_date(timestamp)
    except Exception:
        return False
    return True

# *  ----------- User ----------- * #
@mutation.field("registerUser")
@auth('manager')
def registerUser_resolver(obj, info, **kwargs):
    dbo.insert_one('users', kwargs['newUser'])
    return True

@mutation.field("deleteUser")
@auth('manager')
def deleteUser_resolver(obj, info, _id, user):
    dbo.delete_one('users', {"_id": ObjectId(_id)})
    return True

@mutation.field("updateUser")
@auth('manager')
def updateUser_resolver(obj, info, _id, **kwargs):
    dbo.update_one('users', {'_id':  ObjectId(_id)}, {"$set":kwargs['input']})
    return True

# *  ----------- Target ----------- * #
from src.nodes.process.target import targets as tg, target

@mutation.field("updateTargets")
@auth('operator')
def updateTargets(obj, info, **kwargs):
    tg(*list(map(target, kwargs['targets'])))
    return True
