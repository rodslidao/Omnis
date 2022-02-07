from .models import *
from ariadne import MutationType
from src.nodes.alerts.alert_obj import Alert
from numpy import uint8, frombuffer
from cv2 import imdecode, imwrite
from os.path import abspath

mutation = MutationType()

@defaultException
@mutation.field("createNodeSheet")
def createNodeSheet_resolver(obj, info, **kwargs):
    """Create a new NodeSheet object and return it like a payload"""
    print(kwargs)
    returns = NodeSheet().createNodeSheet(**kwargs.get("input", {}))
    print("Returning:", returns)
    return {"status":{"success": True },"data": returns}


@defaultException
@mutation.field("updateNodeSheet")
def updateNodeSheet_resolver(obj, info, **kwargs):
    """Update a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().updateNodeSheet(kwargs.get("id"), **kwargs.get("input", {}))
    return {"status":{"success": True },"data": returns}


@defaultException
@mutation.field("deleteNodeSheet")
def deleteNodeSheet_resolver(obj, info, id):
    """Delete a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().deleteNodeSheet(id)
    return {"status":{"success": True },"data": returns}

@defaultException
@mutation.field("startProcess")
def startProcess_resolver(obj, info):
    """Start a process by id and return it like a payload"""
    process.startProcess()
    returns = process.dict()
    print(returns)
    return {"status":{"success": True },"data": returns}

@defaultException
@mutation.field("stopProcess")
def stopProcess_resolver(obj, info):
    """Stop a process by id and return it like a payload"""
    process.stopProcess()
    returns = process.dict()
    print(returns)
    return {"status":{"success": True },"data": returns}

@defaultException
@mutation.field("pauseProcess")
def pauseProcess_resolver(obj, info):
    """Pause a process by id and return it like a payload"""
    process.pauseProcess()
    returns = process.dict()
    print(returns)
    return {"status":{"success": True },"data": returns}

@defaultException
@mutation.field("resumeProcess")
def resumeProcess_resolver(obj, info):
    """Resume a process by id and return it like a payload"""
    process.resumeProcess()
    returns = process.dict()
    return {"status":{"success": True },"data": returns}

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

@mutation.field("createAlert")
async def createAlert_resolver(obj, info, input):
    """Create a new Alert object and return it like a payload"""
    returns = Alert(**input)
    return {"status":{"success": True },"data": returns}

@mutation.field("uploadFile")
async def uploadFile_resolver(obj, info, file):
    """Upload a file and return it like a payload"""
    print(file)
    return {"status":{"success": True },"data": file}

class Picutre():
    def __init__(self, name, _id=ObjectId()):
        self._id = _id
        self.name = name[:-3]
        self.extension = name[-3:]
        self.path =  f"/imgs/{self._id}"

    def export(self, path, img):
        """Export the picture to the path"""
        imwrite(path, img)
        return self.__dict__
        

@mutation.field("uploadPhoto")
async def uploadPhoto_resolver(obj, info, **kwargs):
    name = kwargs.get('photo').filename
    p = Picutre(name)
    path = f"{abspath('./src')}/{p.path}"
    img = imdecode(frombuffer(kwargs.get('photo').file.read(), uint8), 1)
    print(p.export(path, img))
    return {"filename": p.id, "path":p.path}
    