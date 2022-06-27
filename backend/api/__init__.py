from os import environ
from platform import system
from threading import Thread
from bson import encode
from dotenv import load_dotenv
from .log import logger, exception, custom_handler, logger, levels, lvl
from .decorators import for_all_methods
import jwt
from graphql.type import GraphQLResolveInfo
from graphql.error import GraphQLError

from src.manager.mongo_manager import connectToMongo, getDb

load_dotenv()
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
                raise GraphQLError("Invalid credential")
            else:
                user = User(**token)
                if user >= lvl:
                    kwargs.update({'user':user})
                    return resolver(obj, info, *args, **kwargs)
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

from ariadne import ScalarType
from bson import ObjectId
ID = ScalarType("ID")

@ID.serializer
def ID_serializar(value):
    logger.info('seta')
    return value.srt

@ID.value_parser
def ID_v_parser(value):
    if value:
        return ObjectId(value)

@ID.literal_parser
def ID_l_parser(ast):
    return ID_v_parser(str(ast.value))



#  "eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJfaWQiOiI2MmI0NmM3ZjE3NTRmZTljNzhhMjNkN2YiLCJhdmF0YXJfaW1hZ2UiOiJodHRwczovL3Bwcy53aGF0c2FwcC5uZXQvdi90NjEuMjQ2OTQtMjQvMTE3NzY1NzM0XzkyNTMyNTQ2Nzk1OTM5M182NTgzODkyNTE0OTQzNzU0NjI2X24uanBnP2NjYj0xMS00Jm9oPTAxX0FWeGxfblEtUWlWV01SdFhjV3BNYXhCUnV3TWtMdEsxLXpHaXNpMGhPczE4VGcmb2U9NjJDMkFFNTciLCJlbWFpbCI6ImhlbnJ5Y2tlLmJvenphQG9yYWtvbG8uY29tLmJyIiwibGFzdF9uYW1lIjoiQm96emEgU2NoZW5iZXJrIiwiZmlyc3RfbmFtZSI6IkhlbnJ5Y2tlIiwibGV2ZWwiOiJkZXZlbG9wZXIiLCJsYXN0X2FjY2VzcyI6MTY1NjAxNTU0NC43NjcyNDksImV4cCI6MTY1NjQxOTcyMH0.gEpdR50_E0tj5n_qXdfsBsFjhf9HXXcA5TRGYyjPOst5Ig2iCwN_twtmxQCGU0krOxLUO56r2WDvc8fV-EToCA"
#  "eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJfaWQiOiI2MmIzNTNjMjE3NTRmZTljNzhhMjNkNzMiLCJhdmF0YXJfaW1hZ2UiOiJodHRwczovL21lZGlhLWV4cDEubGljZG4uY29tL2Rtcy9pbWFnZS9DNEQwM0FRSEowd2phLXg5RXpBL3Byb2ZpbGUtZGlzcGxheXBob3RvLXNocmlua184MDBfODAwLzAvMTU4OTI0MjU1OTM3OD9lPTE2NjEzODU2MDAmdj1iZXRhJnQ9a0VJQ2JFekEzVVItRm41Q3FxTEJOYkZXREtIR1VfdjVDTkctQW5vS2pKRSIsImVtYWlsIjoicm9kcmlnby5nb21lc0BvcmFrb2xvLmNvbS5iciIsImxhc3RfbmFtZSI6IkdvbWVzIGRvcyBTYW50b3MiLCJmaXJzdF9uYW1lIjoiUm9kcmlnbyIsImxldmVsIjoiZGV2ZWxvcGVyIiwibGFzdF9hY2Nlc3MiOjE2NTYyODMzNzMuNDY0MDI2LCIgIjoxNjU2MzMzMjE5LjI0ODg5NiwiZXhwIjoxNjU2NDE5Nzk0fQ.MTiJjH5wY6gLiQPxfo-0biJqfSxnkN56dzmadgOgewzW6Ex4Ga81kb_r1H9KgBNoiwnlIrm-TFNBGpf11V5_Aw"