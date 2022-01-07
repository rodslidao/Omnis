from numpy import e
from omnis.serial.gcodes import gcode, gcode_exp
from omnis.serial.connections import serial, serial_exp
from python_utils.imports import *
from python_utils.Identificators.I_class import *

camera_objects = {camera_config.get("name"):USB_Camera(camera_config) for camera_config in database.find_many("cameras", {})}
serial_objects = {serial_config.get("name"):serial.new(**serial_config) for serial_config in database.find_many("serials", {})}
server_objects = {server_config.get("name"): server_config for server_config in database.find_many("servers", {"name":"Parallax"})}
machine_objects = {serial_name:gcode.gcode(serial_objects[serial_name]) for serial_name in serial_objects if serial_objects[serial_name].kwargs.get("gcode")}

devicefilter_list = [dv for dv in database.find_many("devices_filters", {})]

model_objects = {dv["filter"]:database.find_one("filters_config", {"name": dv["filter"]}) for dv in devicefilter_list}

filter_objects = {
                    dv["filter"]:Filter(
                        dv["filter"],
                        [database.find_one("colors_filters",  n) for n in model_objects[dv["filter"]]["colors"]],
                        [database.find_one("areas_filters",   n) for n in model_objects[dv["filter"]]["areas"]],
                        [database.find_one("kernels_filters", n) for n in model_objects[dv["filter"]]["kernels"]],
                        [database.find_one("retrieval_algorithm_filters", n) for n in model_objects[dv["filter"]]["mode"]],
                        [database.find_one("approximation_methods", n) for n in model_objects[dv["filter"]]["methods"]]
                    ) for dv in devicefilter_list
                }

Identifyer_objects = {
        dv["filter"]:Identifyer(dv["name"], camera_objects[dv["camera_device"]], machine_objects[dv["machine"]], filter_objects[dv["filter"]] ) for dv in devicefilter_list
}

#! Isso deve mudar.
for c in camera_objects.values():
    c.start()
serial_objects["controller"].start()

