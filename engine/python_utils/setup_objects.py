from setup_app_base import _mainfinal_json as config_file, json, script_dir


class deviceFilter():
    def __init__(self, name, machine, camera_device, filter) -> None:
        pass


from omnis.serial.gcodes import gcode, gcode_exp
from omnis.serial.connections import serial, serial_exp
serial_objects = {}
for serial_config in config_file.get('serial'):
    serial_objects[serial_config['name']] = serial.new(**serial_config)


camera_json = json(script_dir+r'\data\json\config\editable\cameras.json')
cameras_objects = {}
for cam in camera_json():
    cameras_objects[cam["name"]] = USB_Camera(cam)

from omnis.camera.device import USB_Camera
for device_config in config_file.get('deviceFilter'):
    machine = serial_objects.get(device_config['machine'])
    camera_device = cameras_objects[device_config['camera_device']]
    name = device_config['name']
    deviceFilter(**device_config)