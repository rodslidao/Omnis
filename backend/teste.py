print('a')
from pprint import pprint
import cv2
from src.nodes.drawdimensionaldata.draw_functions import draw, imshow, waitKey, destroyAllWindows, identifyObjects
import cv2

import cv2
image = cv2.imread('src/imgs/Teste2.jpg')
mask = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

data = identifyObjects(mask)
pprint(len(data))
# exit()
for n in [0, 7]:
    D = draw(**data[n](), image=image)
    D.drawAll()
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
