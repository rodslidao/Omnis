
from inspect import currentframe
from datetime import datetime
from codetiming import Timer
from typing import Type
from time import sleep
import logging.config
import logging.config
import numexpr as ne
import numpy as np
import json as js
import traceback
import timeit
import cv2
import os

from time import sleep, monotonic

from omnis.serial.utilits.moves import movment as move, moves_exp as moves_exp
from omnis.serial.connections import serial, serial_exp
from omnis.serial.gcodes import gcode, gcode_exp
from omnis.opencv import macrofilter as macro
from omnis.camera.device import USB_Camera

import omnis.data.manipulator.new as new
import omnis.opencv.utility as my_cv2

import omnis.server.app as flask_app
import omnis.util.stop as stop

from omnis.structure_nodes import loop_process, loop, node
sizorLift = lambda atualPos, variacao=0, hipotenusa=160, aberturaMinima=149.509 : aberturaMinima - (hipotenusa**2 - ((hipotenusa**2-(aberturaMinima - atualPos)**2)**0.5+variacao)**2)**0.5
line = lambda: currentframe().f_back.f_lineno

from python_utils.mongodb import *
database = MongoDB("192.168.1.31", 27017, "Omnis")

imports = globals().copy()

#print(((stop.__init__).__dict__))