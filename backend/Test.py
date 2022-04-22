
class message:
    def __init__(self, targetName, payload):
        self.targetName = targetName
        self.payload = payload

from os import environ

import cv2

from api import dbo
from src.nodes.blister.blister_obj import Blister
from src.nodes.identify.identify_functions import identifyObjects
from src.nodes.filters.hsv_node import HsvNode
from src.nodes.switch.switch_node import SwitchNode
import numpy as np
from bson import ObjectId

blister_identify = dbo.find_one(
    "blister-manager", {"_id": ObjectId("6256d313daaa135378e4cb27")}
)
blister_joint = dbo.find_one(
    "blister-manager", {"_id": ObjectId("62582ba7694506e2beac17d7")}
)

dbo.close()
blister_i = Blister(**blister_identify)
blister_j = Blister(**blister_joint)

bkg = cv2.imread(r"C:\Users\Henrycke\Desktop\bkg2.jpeg")
bkg = cv2.rotate(bkg, cv2.cv2.ROTATE_90_CLOCKWISE)
bkg = cv2.resize(bkg, (652, 802))
bkg = np.concatenate((bkg, np.zeros((802, 900, 3), np.uint8)), axis=1)
verify = SwitchNode('IF0', ObjectId(), {'auto_run': {'value': False}}, [], [])

# color = Image('./color_template.jpeg')
# print(color.dominant_color_range())

bkgf = HsvNode.convert_frame(bkg.copy(), [100.8, 89.6, 126.7], [187.2, 166.4, 235.3])

slots_of_roi = blister_i.roi(bkgf)

show_roi = blister_i.roi(bkg.copy())
blister_i.draw(bkg)
blister_j.draw(bkg)


identifyObjects(slots_of_roi(), area={"min": 100, "max": 20000})

if_msg = message("eval", "bool(a)")
out_true = message("True", "Dados aqui")
out_false = message("False", -1)

verify.execute(out_false)
verify.execute(out_true)

slots_of_roi.re_order(T=True, steps_x=1, start_x=0, x=-1, y=-1)
show_roi.re_order(T=True, steps_x=1, start_x=0, x=-1, y=-1)
blister_j.transpose()

for _ in range(slots_of_roi().size):
    roi_index, roi = next(slots_of_roi)
    item_msg = message("a", roi.item)            # This is create automatically by the node manager
    verify.execute(
        
    )
    if verify.execute(if_msg) != -1:             # The switch node will trrigger 'True' interface, if the condition is true
        cv2.imshow("ROI", bkg)
        cv2.moveWindow("ROI", 0, 0)
        slot_index, s = next(blister_j)
        frame = show_roi(*roi_index).item
        list(map(lambda x: cv2.drawContours(frame, [x.countour], -1, (0, 255, 0), 1), roi.item))

        cv2.arrowedLine(bkg, tuple(map(int, roi.center)), tuple(map(int, s.center)), (0,255,0), 1, cv2.LINE_AA, tipLength=0.025)

        cv2.imshow(str(roi_index), frame)
        cv2.moveWindow(str(roi_index), *roi.start)

        cv2.waitKey(250)
cv2.waitKey(0)
