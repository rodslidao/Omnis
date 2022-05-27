from os import environ
from platform import system
from threading import Thread
from dotenv import load_dotenv
from vidgear.gears.asyncio import WebGear
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
from src.nodes.camera.custom_camera import Camera
from src.nodes.alerts.alert_obj import Alert


def Managers_Import(definitions):
    for collection, manager_class in definitions.items():
        for config in dbo.find_many(collection, {}):
            if not config.get("disabled", False):
                try:
                    match config.get("is_gcode"):
                        case True:
                            manager_class["class"][1](**config)
                        case _:
                            manager_class["class"][0](**config, **config.get("options"))
                except Exception:
                    Alert(
                            "error",
                            "Dispotivo com Falha",
                            'Não foi possível iniciar o dispositivo "{}"'.format(
                                config.get("name")
                            ),
                            how2solve="Verifique se o dispositivo está conectado corretamente",
                            delay=3
                        )


mangers = {
    "camera-manager": {"manager": CameraManager, "class": [Camera]},
    "serial-manager": {"manager": SerialManager, "class": [Serial, SerialGcodeOBJ]},
}

# Managers_Import(mangers)
async def automatic_classes():
    Thread(target=Managers_Import, args=(mangers,)).start()


# options = {
#     "custom_stream": CameraManager,
#     "custom_data_location": "./",
#     "frame_size_reduction": 50,
#     "jpeg_compression_quality": 21,
# }

# stremer = WebGear(logging=True)
# stremer = WebGear_RTC(logging=True, **options)
