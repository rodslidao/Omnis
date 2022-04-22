from src.utility.system.log_setup.setup import default_setup, exception, custom_handler
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from os import environ
from time import sleep
from src.utility.system.class_inspect import is_static_method
import platform
environ.setdefault("SO", platform.system())

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}
lvl = 'info'

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels[lvl])

def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)) and not attr.startswith("__") and not is_static_method(cls, attr):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

from src.manager.mongo_manager import connectToMongo, getDb


if environ.get("PYTHON_RUN", "true").lower() == "false":
    print("Python is set to not running...")
    while True:
        print("Waiting for 20 minutes.")
        sleep(20 * 60)


connectToMongo()
dbo = getDb()

custom_handler(logger, "mongo", "json", dbo, levels[lvl])
logger.info("Logger is set up.")

from src.manager.serial_manager import SerialManager
from src.manager.camera_manager import CameraManager

from src.nodes.serial.custom_serial import CustomSerial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from src.nodes.camera.custom_camera import camera

if True or environ.get("SO").lower() == "linux":
    for serial_config in dbo.find_many('serial-manager', {}):
        serial_config['port'] = 'COM3'
        SerialManager.add(SerialGcodeOBJ(**serial_config) if serial_config.get("is_gcode", False) else CustomSerial(**serial_config))

    for camera_config in dbo.find_many('camera-manager', {}):
        CameraManager.add(camera(**camera_config))