from os import environ
from platform import system
from threading import Thread
from dotenv import load_dotenv
from .log import logger, exception, custom_handler, logger, levels, lvl
from .decorators import for_all_methods

from src.manager.mongo_manager import connectToMongo, getDb

load_dotenv()
environ.setdefault("SO", system())

connectToMongo()
dbo = getDb()
# custom_handler(logger, "mongo", "json", dbo, levels[lvl])

from src.manager.serial_manager import SerialManager
from src.manager.camera_manager import CameraManager
from src.nodes.serial.custom_serial import Serial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from src.nodes.serial.pins_obj import pin
from src.nodes.serial.axes import axis
from src.nodes.camera.custom_camera import Camera
from src.nodes.alerts.alert_obj import Alert

pins = [pin(**p) for p in dbo.find_many("pins")]
axes = [
    axis(**a)
    for a in dbo.find_many("machine_axis", data={"_id": 1, "name": 1, "board": 1})
]
# logger.info(f"Aqui: {axes}")
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


mangers = {
    "camera-manager": {"manager": CameraManager, "class": [Camera]},
    "serial-manager": {"manager": SerialManager, "class": [Serial, SerialGcodeOBJ]},
}

# def automatic_classes():
# Thread(target=Managers_Import, args=(mangers,)).start()
Managers_Import(mangers)
