import cv2
from numpy import float32, uint8, int0
from src.nodes.drawdimensionaldata.draw_functions import draw, identifyObjects
import cv2

import cv2
image = cv2.imread('src/imgs/Teste2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
parm = {

    "area":{
        "min":10000,
        "max":15000
    },

    # "width":{
    #     "min":10,
    #     "max":1000
    # },

    # "height":{
    #     "min":10,
    #     "max":1000
    # },
}
data = identifyObjects(mask, **parm)
image = cv2.bitwise_xor(image, image, mask=mask)
for n in range(len(data)):
    D = draw(**data[n](), image=image)
    D.drawAll()
cv2.imshow('image', image)
cv2.imshow('mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
