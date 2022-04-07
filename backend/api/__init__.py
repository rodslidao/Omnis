from src.utility.system.log_setup.setup import default_setup, exception
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from os import environ
from time import sleep

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels["debug"])

from src.manager.mongo_manager import connectToMongo, getDb


if environ.get("PYTHON_RUN", "true").lower() == "false":
    print("Python is set to not running...")
    while True:
        print("Waiting for 20 minutes.")
        sleep(20 * 60)


connectToMongo()
dbo = getDb()

from src.manager.serial_manager import SerialManager
from src.manager.camera_manager import CameraManager
from src.nodes.serial.custom_serial import CustomSerial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from src.nodes.camera.custom_camera import camera

for serial_config in dbo.find_many('serial-manager', {}):
    print("Serials:", serial_config)
    SerialManager.add(SerialGcodeOBJ(**serial_config) if serial_config.get("is_gcode", False) else CustomSerial(**serial_config))

for camera_config in dbo.find_many('camera-manager', {}):
    print("Cameras:", camera_config)
    CameraManager.add(camera(**camera_config))
