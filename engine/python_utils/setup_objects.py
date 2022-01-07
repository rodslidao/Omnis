# from setup_app_base import _mainfinal_json as config_file, json, script_dir


# class deviceFilter():
#     def __init__(self, name, machine, camera_device, filter) -> None:
#         pass


from omnis.serial.gcodes import gcode, gcode_exp
from omnis.serial.connections import serial, serial_exp
from python_utils.imports import *
# serial_objects = {}
# for serial_config in config_file.get('serial'):
#     serial_objects[serial_config['name']] = serial.new(**serial_config)


# camera_json = json(script_dir+r'\data\json\config\editable\cameras.json')
# cameras_objects = {}
# for cam in camera_json():
#     cameras_objects[cam["name"]] = USB_Camera(cam)

# from omnis.camera.device import USB_Camera
# for device_config in config_file.get('deviceFilter'):
#     machine = serial_objects.get(device_config['machine'])
#     camera_device = cameras_objects[device_config['camera_device']]
#     name = device_config['name']
#     deviceFilter(**device_config)

serial_objects = {serial_config.get("name"):serial.new(**serial_config) for serial_config in database.find_many("serials", {})}
server_objects = {server_config.get("name"): server_config for server_config in database.find_many("servers", {"name":"Parallax"})}
machine_objects = {serial_name:gcode.gcode(serial_objects[serial_name]) for serial_name in serial_objects if serial_objects[serial_name].kwargs.get("gcode")}
serial_objects["controller"].start()
# machine_objects = {}