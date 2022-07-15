from ast import Return
from os import environ
from platform import system
from threading import Thread
from dotenv import load_dotenv
from .log import logger, exception, custom_handler, logger, levels, lvl
from .decorators import for_all_methods
import jwt
from graphql.type import GraphQLResolveInfo
from graphql.error import GraphQLError
from bson.dbref import DBRef

from src.manager.mongo_manager import connectToMongo, getDb

load_dotenv()
load_dotenv(f'.env.{environ.get("NODE_ENV")}')
environ.setdefault("SO", system())

connectToMongo()
dbo = getDb()

key_context = dbo.find_one("keys")
from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key
with open(key_context["path"], "r") as private, open(key_context["path"]+'.pub', "r") as public:
    private_key = load_ssh_private_key(private.read().encode(), key_context["pass"].encode())
    public_key =  load_ssh_public_key(public.read().encode(), key_context["pass"].encode())

from src.manager.serial_manager import SerialManager
from src.manager.camera_manager import CameraManager
from src.nodes.serial.custom_serial import Serial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from src.nodes.serial.pins_obj import pin
from src.nodes.serial.axes import axis
from src.nodes.camera.custom_camera import Camera
from src.nodes.alerts.alert_obj import Alert
from src.utility.crud.user import User

def auth(lvl=None):
    def decorator(resolver):
        def wrapper(obj, info: GraphQLResolveInfo, *args, **kwargs):
            try:
                token = info.context["request"].headers.get('authorization').split(' ')[-1]
                header_data = jwt.get_unverified_header(token)
                token = jwt.decode(token, key=public_key, algorithms=[header_data['alg']])
            except Exception as e:
                logger.debug(f"Acess Denied, invalid or missing token: {e}.")
                #raise GraphQLError("Invalid credential")
            else:
                user = User(**token)
                if user >= lvl:
                    logger.debug(f"User: {user.json} requesting {resolver.__name__}")
                    kwargs.update({'user':user})
                    return resolver(obj, info, *args, **kwargs)
                logger.debug(f"User: {user.json} don't has permissions to request {resolver.__name__}")
                raise GraphQLError('Permission Denied')
        return wrapper
    return decorator


pins = [pin(**p) for p in dbo.find_many("pins")]
axes = [
    axis(**a)
    for a in dbo.find_many("machine_axis", data={"_id": 1, "name": 1, "board": 1})
]

def Managers_Import(definitions):
    for collection, manager_class in definitions.items():
        for config in dbo.find_many(collection, {}):
            if not config.get("disabled", False):
                try:
                    match config.get("is_gcode"):
                        case True:
                            manager_class["class"][1](
                                pins={
                                    str(p._id): p
                                    for p in pins
                                    if p.board == str(config["_id"])
                                },
                                axes={
                                    str(a._id): a
                                    for a in axes
                                    if a.board == str(config["_id"])
                                },
                                **config
                            )
                        case _:
                            manager_class["class"][0](**config, **config.get("options"))
                except Exception as e:
                    Alert(
                        "error",
                        "Dispositivo com Falha",
                        'Não foi possível iniciar o dispositivo "{}".\n Erro: {}'.format(
                            config.get("name"), e
                        ),
                        how_to_solve="Verifique se o dispositivo está conectado corretamente",
                        delay=3,
                    )
                    exit()

mangers = {
    "camera-manager": {"manager": CameraManager, "class": [Camera]},
    "serial-manager": {"manager": SerialManager, "class": [Serial, SerialGcodeOBJ]},
}


Managers_Import(mangers)
from ariadne import ObjectType, ScalarType
from bson import ObjectId
ID = ScalarType("ID")
DB_VALUE = ScalarType("DB_VALUE")

DBREF_object = ScalarType("DBREF_object")
DBREF_matrix = ScalarType("DBREF_matrix")
DBREF_process = ScalarType("DBREF_process")
DBREF_variable = ScalarType("DBREF_variable")
DBREF_sketch = ScalarType("DBREF_sketch")

@ID.serializer
def ID_serializar(value):
    if isinstance(value, ObjectId): return str(value)
    elif isinstance(value, dict):
        for k, v in value.items():
           value[k] = ID_serializar(v)
        return value
    elif isinstance(value, list):
        return list(map(ID_serializar, value))
    return value


@ID.value_parser
def ID_v_parser(value):
    if value:
        return ObjectId(value)
    return value

@ID.literal_parser
def ID_l_parser(ast):
    return ID_v_parser(str(ast.value))


@DB_VALUE.serializer
def DB_VALUE_serializar(value, collection=None):
    if isinstance(value, DBRef):
        return ID_serializar(dbo.find_one(value.collection, {'_id':value.id}))
    elif not isinstance(value, str):
        if isinstance(value.get("_id"), ObjectId) and value.get("collection", collection):
            return ID_serializar(dbo.find_one(value.get("collection", collection), {"_id":value["_id"]}))
    return value

@DB_VALUE.value_parser
def DB_VALUE_v_parser(value, collection=None):
    if isinstance(value, dict):
        return {"$ref":value.get('ref', collection), '$id': ID_v_parser(value['_id'])}
    elif isinstance(value, list):
        if not collection:
            return list(map(DB_VALUE_v_parser, value))
        else:
            return [DB_VALUE_v_parser(v,collection) for v in value]

@DBREF_object.value_parser
def DBREF_object_v_parser(value):
    return DB_VALUE_v_parser(value, collection='object')

@DBREF_matrix.value_parser
def DBREF_matrix_v_parser(value):
    return DB_VALUE_v_parser(value, collection='matrix')

@DBREF_process.value_parser
def DBREF_process_v_parser(value):
    return DB_VALUE_v_parser(value, collection='process')

@DBREF_variable.value_parser
def DBREF_variable_v_parser(value):
    return DB_VALUE_v_parser(value, collection='variable')

@DBREF_sketch.value_parser
def DBREF_sketch_v_parser(value):
    return DB_VALUE_v_parser(value, collection='sketch')

custom_types = [ID, DB_VALUE, DBREF_object, DBREF_matrix, DBREF_process, DBREF_variable, DBREF_sketch]
