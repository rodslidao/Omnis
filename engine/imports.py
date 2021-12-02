import logging.config
import json as js
import timeit
from typing import Type

from externallibs import info
import externallibs.structure_nodes.structure as node
import externallibs.new_serial.connection as serial
import externallibs.opencv.macrofilter as macro
import externallibs.new_serial.movment as move
import externallibs.new_serial.gcode as gcode
import externallibs.opencv.utility as my_cv2
import externallibs.camera.device as device
import externallibs.server.app as flask_app
import externallibs.jsoneditor.new as json
import externallibs.util.stop as stop

from inspect import currentframe
from datetime import datetime
import logging.config
import numpy as np
import traceback
import os
import cv2

sizorLift = lambda atualPos, variacao=0, hipotenusa=160, aberturaMinima=149.509 : aberturaMinima - (hipotenusa**2 - ((hipotenusa**2-(aberturaMinima - atualPos)**2)**0.5+variacao)**2)**0.5
line = lambda: currentframe().f_back.f_lineno