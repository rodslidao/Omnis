
from main import *
import externallibs.opencv.utility as utility

window_json = json.new(f"{config_json_dir}/window.json", "window", script_dir)
default_cam_bkg = cv2.resize(cv2.imread(f"{data_images_dir}/static/background.png"),(0,0), fx=0.5, fy=0.5)

identificator_name = "Color_Find"

identificator_objects
stopreasons_objects
_area = processing_objects["small_blue"]
production_objects


utility.createWindow(window_json.value)
key = 0
while  key != ord('q'):
    key = cv2.waitKey(1)
    _value = utility.getWindow(window_json.value)
    _min = (_value['H Min'],_value['S Min'],_value['V Min'])
    _max = (_value['H Max'],_value['S Max'],_value['V Max'])
    lower =  macro.cor(_min, 'cv2_hsv')
    upper = macro.cor(_max, 'cv2_hsv')

    k_a = macro.Kernel(sizes=[_value['A Min'], _value['A Min']]).kernel
    k_b = macro.Kernel(sizes=[_value['A Max'], _value['A Max']]).kernel

    # _area.identifier.config.colorRange.lower = lower
    # _area.identifier.config.colorRange.upper = upper
    # _area.identifier.config.kernel_A = k_a
    # _area.identifier.config.kernel_B = k_b
    
    _area.process(drawData=True)
    cv2.imshow("area", cv2.resize(_area.world2draw, (1080, 720)))
    if key == ord('k'):
        print(upper.getColor('hsv'))
        print(lower.getColor('hsv'))

