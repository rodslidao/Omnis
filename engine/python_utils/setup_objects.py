from numpy import e
from omnis.serial.gcodes import gcode, gcode_exp
from omnis.serial.connections import serial, serial_exp
from python_utils.imports import *
# from python_utils.nodes import *

# from imports import *
# from .nodes import *

script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

config_json_dir = script_dir+r'/json/config'
data_json_dir = script_dir+'/json/data'
data_images_dir = script_dir+'/images'
# print(f"{config_json_dir}/editable/devicefilter.json")
# exit()
default_cam_bkg = cv2.resize(cv2.imread(f"{data_images_dir}/static/background.jpg"), (0, 0), fx=0.5, fy=0.5)
#C:\Users\Henrycke\Documents\GitHub\CEO96F-RETROFIT\engine\data\images\static\background.jpg
# No futuro quero criar esses objetos de forma mais dinamica, mas preciso refatorar varias classes pra isso.
# setup_json = new.json(f"{config_json_dir}/internal/setup_objects.json", "setup", script_dir)


# ===========================================================================
# ============================ Define json object ===========================
# ===========================================================================
devicefilter_json = new.json(f"{config_json_dir}/editable/devicefilter.json", "devicefilter", script_dir)
positions_json = new.json(f"{config_json_dir}/machine/positions.json", "positions", script_dir)
stopreasons_json = new.json(f"{config_json_dir}/editable/stopreasons.json", "stopreasons", script_dir)
production_json = new.json(f"{config_json_dir}/editable/production.json", "production", script_dir)
keypoints_json = new.json(f"{config_json_dir}/editable/keypoints.json", "keypoints", script_dir)
templates_json = new.json(f"{config_json_dir}/editable/templates.json", "templates", script_dir)
cameras_json = new.json(f"{config_json_dir}/editable/cameras.json", "cameras", script_dir)
filters_json = new.json(f"{config_json_dir}/editable/filters.json", "filters", script_dir)
process_json = new.json(f"{config_json_dir}/editable/process.json", "process", script_dir)
pins_json = new.json(f"{config_json_dir}/machine/pins.json", "pins", script_dir)
serial_json = new.json(f"{config_json_dir}/editable/serial.json", "serial", script_dir)
server_json = new.json(f"{config_json_dir}/editable/server.json", "server", script_dir)
debug_json = new.json(f"{config_json_dir}/editable/debug.json", "debug", script_dir)
user_json = new.json(f"{config_json_dir}/editable/users.json", "users", script_dir)

# ===========================================================================
# ========================== Define camera objects ==========================
# ===========================================================================
cameras_objects = {}
for cam in cameras_json.value["cameras"]:
    device_cam = USB_Camera(cam)
    device_cam.start()
    cameras_objects[device_cam.name] = device_cam


# ===========================================================================
# ===================== Define area_processing objects ======================
# ===========================================================================
# processing_objects = {}
# for area in devicefilter_json.value:
#     cam_obj = cameras_objects[area["camera_device"]]
#     ide_obj = identificator_objects[area["filter"]]
#     process = macro.AreaProcessing(
#         area["filter"], cam_obj, keypoints_json.value, ide_obj, blur=(5, 5))
#     processing_objects[area["filter"]] = process

# ===========================================================================
# ======================= Define stop reasons objects =======================
# ===========================================================================
stopreasons_objects = {}
for stop_obj in stopreasons_json.value:
    stopreasons_objects[stop_obj['name']] = stop.reason(
        stop_obj['name'], logging.getLogger("stop_logger"), stop_obj['initial'])

# ===========================================================================
# ======================= Define productions objects =======================
# ===========================================================================
"""
production_objects = {}
for prod_model in production_json.value["models"]:
    prod_obj = new.production(data_json_dir+'/production', prod_model,
                               production_json.value["template"], script_dir, autoSave=True)
    production_objects[prod_model["name"]] = prod_obj
"""

# ===========================================================================
# ======================= Define serial objects =======================
# ===========================================================================
serial_objects = {}
machine_objects = {}
for serial_model in serial_json.value:
    serial_objects[serial_model["name"]] = serial.new(**serial_model)
    if serial_model.get("gcode"):
        machine_objects[serial_model["name"]] = gcode.gcode(serial_objects[serial_model["name"]])

_all = globals().copy()
# ===========================================================================
# ======================== Define identifier objects ========================
# ===========================================================================

class dimension():
    def __init__(self, center, dots, area, rects, rectangle):
        self.area = area
        self.rectangle = rectangle
        self.dots = dots
        self.rects = rects
        self.center = center

class identificador:
    def __init__(self, name, cam, machine, filter_data, autoColor=True):
        self.filter = macro.makeFilter(name, filter_data)[name]
        self.cam = cam
        self.AC = autoColor
        pass

    def function(self, image, filter_obj) -> dict:
        color_range  = filter_obj.colorRange.get('cv2_hsv')
        hsv_mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL), np.array(color_range['lower']), np.array(color_range['upper']))
        better_hsv = cv2.morphologyEx(
                cv2.morphologyEx(hsv_mask, cv2.MORPH_CLOSE, filter_obj.kernel_A),
                                                cv2.MORPH_OPEN,  filter_obj.kernel_B)


        contours, hierarchy = cv2.findContours(better_hsv, mode=getattr(cv2, filter_obj.mode), method=getattr(cv2, filter_obj.method))
        #cv2.imshow("Processimg", image)
        data = []
        try:
            hierarchy = hierarchy[0]
        except TypeError:
            return data
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            area = cv2.contourArea(currentContour)
            template = {}
            areas = filter_obj.areaRange.getRange(unit='px')['px']
            if areas['min'] < area < areas['max']:

                template["area"] = area

                xA, yA, wA, hA = cv2.boundingRect(currentContour)
                template["rectangle"] = ((xA, yA), (wA, hA))

                boxA = np.int0(cv2.boxPoints(cv2.minAreaRect(currentContour)))
                
                sortedBoxX =sorted(boxA, key=lambda x: x[0])
                sortedBoxY =sorted(boxA, key=lambda x: x[1])
                A,B,C,D = tuple(sortedBoxX[0]), tuple(sortedBoxX[-1]), tuple(sortedBoxY[0]), tuple(sortedBoxY[-1])

                AB = (abs(A[0]-B[0])**2+abs(A[1]-B[1])**2)**0.5
                AC = (abs(A[0]-C[0])**2+abs(A[1]-C[1])**2)**0.5
                AD = (abs(A[0]-D[0])**2+abs(A[1]-D[1])**2)**0.5
                # M =  (int((abs(A[0]-B[0])/2)+A[0]), int((abs(C[1]-D[1])/2)+C[1]))
                # template["center"] = M
                
                template["dots"] = {'A':A, 'B':B, 'C':C, 'D':D}
                template["rects"] = {'AB':AB, 'AC':AC, 'AD':AD}

                momentsA = cv2.moments(currentContour)
                cxA = int(momentsA["m10"] / momentsA["m00"])
                cyA = int(momentsA["m01"] / momentsA["m00"])
                template["center"] = (cxA, cyA)
                
                data.append(template)
        return data 

    def identify(self) -> dict:
        if self.AC:
            _min, _max = self.defineColor(self.cam.read())
            self.filter.colorRange.lower = macro.cor(_min, 'cv2_hsv')
            self.filter.colorRange.upper = macro.cor(_max, 'cv2_hsv')

        data = self.function(self.cam.read(), self.filter)
        self.dataset = set()
        for n in data:
            self.dataset.add(dimension(**n))
        return self.dataset

    def defineColor(self, img_color):
        # procura na amostra de cor, a cor dominante
        rgb_base = self.rgbDominantColor(img_color)
        
        # cria uma imagem de amostra que contenha somente a cor dominante
        rgb_base_img = np.zeros([200, 200, 3], np.uint8)
        for c in range(0,3):
            rgb_base_img[:, :, c] = np.zeros([200, 200]) + rgb_base[c]

        # converte a amosta de cor dominante pra hsv
        hsv_bkg = cv2.cvtColor(rgb_base_img, cv2.COLOR_BGR2HSV_FULL)

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
serial_objects["Octopus V1.1"].start()

