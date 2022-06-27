from bson import ObjectId
from pandas import value_counts
from .models import NodeSheet, grok
from ariadne import QueryType
from src.nodes.node_manager import NodeManager
from src.nodes.node_registry import NodeRegistry
from threading import enumerate as thread_enumerate
from src.manager.camera_manager import CameraManager
from src.manager.serial_manager import SerialManager
from src.nodes.calibration.camera_calibration import CameraCalibration
from threading import Thread
from api import dbo, logger, environ, auth, private_key
from datetime import datetime, timedelta, timezone
import jwt
from graphql.error import GraphQLError


query = QueryType()

payload = {"success": False, "errors": None}


@query.field("getNodeSheet")
@auth('developer')
def getNodeSheet_resolver(obj, info, **kwargs):
    """Get a NodeSheet by id and return it like a payload"""
    result = NodeSheet().getNodeSheetById(_id=kwargs.get("_id"))
    payload["success"] = True
    payload["data"] = result
    return payload


@query.field("allPhotos")
@auth('developer')
def resolve_allPhotos(obj, info, **kwargs):
    """Get all photos from the database"""
    payload = [{"filename": "a.png", "path": "imgs/a.png"}]
    return payload


@query.field("getSerials")
@auth('viewer')
def resolve_getSerials(obj, info, **kwargs):
    return {"status": True, "data": SerialManager.get()}


@query.field("getCameras")
@auth('viewer')
def resolve_getCameras(obj, info, **kwargs):
    return {"status": True, "data": CameraManager.get()}


@query.field("getSketchList")
@auth('viewer')
def resolve_get_sketch_list(obj, info, **kwargs):
    print(NodeSheet().get_sketch_list()[0])
    return {"status": True, "data": list(NodeSheet().get_sketch_list())}


@query.field("getNodeInfo")
@auth('operator')
def resolve_getNodeInfo(obj, info, node_type, **kwargs):
    """Get a Node by id and return it like a payload"""
    result = (NodeRegistry.getNodeClassByName(node_type)).get_info(
        **kwargs.get("kwargs", {})
    )
    return {"status": True, "data": result}


@query.field("getManutention")
@auth('maintenance')
def resolve_getManutention(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    return {"status": True, "data": grok.get_url()}


@query.field("getThr")
@auth('developer')
def resolve_getThr(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    return list([thread.name for thread in thread_enumerate()])


@query.field("calibrateCamera")
@auth('maintenance')
def resolve_calibrateCamera(obj, info, **kwargs):
    Thread(target=CameraCalibration(**kwargs.get("input", {})).calibrate).start()
    return True


@query.field("getLoadedNodes")
@auth('developer')
def resolve_getLoadedNodes(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    return NodeManager.getActiveNodes()


@query.field("getLoadedConfig")
@auth('developer')
def resolve_getLoadedConfig(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    return NodeSheet().getNodeSheetById(process.loaded_id)


@query.field("getDevicesList")
@auth('developer')
def resolve_getDevicesList(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    temp = list(dbo.find_many("pins"))
    for i in temp:
        i["_id"] = str(i["_id"])
    return temp


@query.field("getAxisList")
@auth('operator')
def resolve_getAxisList(obj, info, **kwargs):
    """Get a Node by id and return it like a payload"""
    temp = list(dbo.find_many("machine_axis"))
    for i in temp:
        i["_id"] = str(i["_id"])
    return temp

@query.field("authenticateUser")
def resolve_authUserProfile(obj, info, username=None, **kwargs):
    keep = {'password':0}
    user = dbo.find_one("users", {"username": username}, keep)
    if not user:
        user = dbo.find_one("users", kwargs, keep)
    if user:
        payload = user.copy()
        payload.update({"exp": datetime.now(tz=timezone.utc) + timedelta(hours=payload.get('exp', 24)), '_id': str(payload['_id'])})
        token = jwt.encode(
            payload,
            key=private_key,
            algorithm="EdDSA",
        )
        now = datetime.utcnow().timestamp()
        dbo.update_one('users', {'_id':ObjectId(user['_id'])}, {'$set':{' ':now}})
        user.update({'last_access': now})
        return {"user": user, "token": token}
    raise GraphQLError("Invalid Login")

@query.field("authUserProfile")
@auth('user')
def resolve_authUserProfile(obj, info, user):
    return user.json

@query.field("getUsersList")
@auth('manager')
def  getUsersList_resolver(obj, info, user):
    return list(dbo.find_many('users', {}, {'password':0}))


# *  ----------- Target ----------- * #
from src.nodes.process.target import targets as tg, target

@query.field("getTargetsList")
@auth('operator')
def getTargetsList(obj, info, **kwargs):
    return list(tg.values.keys())