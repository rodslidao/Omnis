from .models import *
from ariadne import QueryType
from src.nodes.node_registry import NodeRegistry
from threading import enumerate as thread_enumerate

query = QueryType()

payload = {"success": False, "errors": None}


@defaultException
@query.field("getNodeSheet")
def getNodeSheet_resolver(obj, info, **kwargs):
    """Get a NodeSheet by id and return it like a payload"""
    result = NodeSheet().getNodeSheetById(_id=kwargs.get("_id"))
    payload["success"] = True
    payload["data"] = result
    return payload


@defaultException
@query.field("getProcess")
def getProcess_resolver(obj, info):
    return {"status": {"success": True}, "data": process.dict()}


@query.field("allPhotos")
def resolve_allPhotos(obj, info, **kwargs):
    """Get all photos from the database"""
    payload = [{"filename": "a.png", "path": "imgs/a.png"}]
    return payload


from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager


@query.field("getSerials")
def resolve_getSerials(obj, info, **kwargs):
    return {"status": True, "data": SerialManager.get()}


@query.field("getCameras")
def resolve_getCameras(obj, info, **kwargs):
    return {"status": True, "data": CameraManager.get()}


@query.field("getSketchList")
def resolve_get_sketch_list(obj, info):
    returns = list(NodeSheet().get_sketch_list())
    return {"status": True, "data": returns}


@query.field("getNodeInfo")
def resolve_getNodeInfo(obj, info, node_type):
    """Get a Node by id and return it like a payload"""
    result = (NodeRegistry.getNodeClassByName(node_type)).get_info()
    return {"status": True, "data": result}


@query.field("getManutention")
def resolve_getManutention(obj, info):
    """Get a Node by id and return it like a payload"""
    return {"status": True, "data": grok.get_url()}


@query.field("getThr")
def resolve_getThr(obj, info):
    """Get a Node by id and return it like a payload"""
    return list([thread.name for thread in thread_enumerate()])
