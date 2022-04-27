from src.utility.system.log_setup.setup import default_setup, exception, custom_handler
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from os import environ
from vidgear.gears.asyncio import WebGear_RTC
from time import sleep
from src.utility.system.class_inspect import is_static_method
import platform
from dotenv import load_dotenv

load_dotenv()
environ.setdefault("SO", platform.system())

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}
lvl = "info"

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels[lvl])


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if (
                callable(getattr(cls, attr))
                and not attr.startswith("__")
                and not is_static_method(cls, attr)
            ):
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

# custom_handler(logger, "mongo", "json", dbo, levels[lvl])

from src.manager.serial_manager import SerialManager
from src.manager.camera_manager import CameraManager

from src.nodes.serial.custom_serial import CustomSerial
from src.nodes.serial.gcode_obj import SerialGcodeOBJ
from src.nodes.camera.custom_camera import camera

for serial_config in dbo.find_many("serial-manager", {}):
    SerialManager.add(
        SerialGcodeOBJ(**serial_config)
        if serial_config.get("is_gcode", False)
        else CustomSerial(**serial_config)
    )


#! Camera options has to be set in database, not here.
cam_opt = options = {
    "CAP_PROP_FRAME_WIDTH": 640,
    "CAP_PROP_FRAME_HEIGHT": 480,
    "CAP_PROP_FPS": 30
}

#? This will be launch based in another file or still by all cameras set in database.?
for camera_config in dbo.find_many("camera-manager", {}):
    if not camera_config.get('disabled', False):
        CameraManager.add(camera(**camera_config, **options))

options = {
    "custom_stream": CameraManager,
    "custom_data_location": "./",
    # "enable_infinite_frames": True,
    "frame_size_reduction": 50,
    "jpeg_compression_quality": 21,
    # 'stabilize': True
}
CameraStreamer = WebGear_RTC(logging=True, **options)
