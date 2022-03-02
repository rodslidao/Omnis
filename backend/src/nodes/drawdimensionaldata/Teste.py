from pickle import TRUE
from cv2 import (
    LINE_4,
    ellipse,
    imread,
    imshow,
    imwrite,
    waitKey,
    destroyAllWindows,
    drawContours,
    arrowedLine,
    rectangle,
    circle,
    putText,
    drawMarker,
    FONT_HERSHEY_SIMPLEX,
    LINE_AA,
    setMouseCallback,
    EVENT_LBUTTONDOWN
)
import numpy as np
class dimensional_data(object):
    """
    Class to represent all parameters of a contour.

    get(key) -> get the value of the key.
    set(key, value) -> set the value of the key.

    Instante() -> return a dict of the object.

    Properties:
    \t _id: ObjectId()\n
    \t area: area of the contour\n
    \t perimeter: perimeter of the contour\n
    \t diameter: diameter of the contour\n
    \t AB: distance between the top left vertex and the to right vertex\n
    \t AC: distance between the top left vertex and the bottom right vertex\n
    \t AD: distance between the top left vertex and the bottom left vertex\n
    \t center: center of the contour\n
    \t vertices: vertices of the contour in coordinates (x, y)\n
    \t box: box of the contour in coordinates (x, y, width, height)\n

    """

    def __init__(
        self,
        area=None,
        perimeter=None,
        diameter=None,
        AB=None,
        AC=None,
        AD=None,
        center=None,
        vertices=None,
        box=None,
    ):
        self.area = area
        self.perimeter = perimeter
        self.diameter = diameter
        self.AB = AB
        self.AC = AC
        self.AD = AD
        self.center = center
        self.vertices = vertices
        self.box = box

    def get(self, key):
        return getattr(self, key)

    def __call__(self):
        return vars(self)


D = dimensional_data(
    100,
    400,
    100,
    100,
    ((100 ** 2) + (100 ** 2)) ** 0.5,
    200,
    (150, 150),
    4,
    np.int0([[100, 100], [200, 100], [200, 200], [100, 200]]),
)

print(D())
image = imread("teste.jpg")

circle(image, (D.center[0], D.center[1]), np.int0(D.diameter / 2), (255, 255, 255), 1)
drawMarker(
    image,
    (D.center[0], D.center[1]),
    (255, 255, 255),
    markerType=2,
    markerSize=10,
    thickness=1,
)

drawContours(image, [D.box], -1, (100, 100, 100), 1, LINE_4)
arrowedLine(image, D.box[0], D.box[1], (255, 0, 0), 1)
arrowedLine(image, D.box[0], D.box[2], (0, 255, 0), 1)
arrowedLine(image, D.box[0], D.box[3], (0, 0, 255), 1)


s = [[b, a] for a in [-1,1] for b in [-1,1]]
s[2], s[3] = s[3], s[2]
for _, l in enumerate(["A", "B", "C", "D"]):
    
    putText(
        image,
        l,
        (D.box[_][0] + (25*s[_][0]), D.box[_][1]+(25*s[_][1])),
        FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        LINE_AA,
    )

for _, l in enumerate(["AB", "AC", "AD"]):
    putText(image, f"{l}: {round(D.get(l),2)}", (D.box[2][0]+25, int(D.diameter+(D.diameter*0.3*(1+_)))), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, LINE_AA)

bkp = image.copy()

def find_angle(origin, point, degrees=True, positive=False):
    angle = np.angle(complex(*(point[0] - origin[0], origin[1] - point[1])), degrees)
    if angle < 0 and positive: angle += 360
    return angle

imshow('image', image)
def onMouse(event, x, y, flags, param):
    if event == EVENT_LBUTTONDOWN:
        angle = find_angle(D.center, (x, y))
        print(angle, True)
        ellipse(image, center=D.center, axes=(20, 20), angle=0, startAngle=angle*-1, endAngle=0.0, color=(255, 0, 255), thickness=1)
        arrowedLine(image, D.center, (x, y), (255, 0, 255), 1)
        drawMarker(image, (x, y), (255, 255, 255), markerType=2, markerSize=10, thickness=1)

setMouseCallback('image', onMouse)

while True:
    key = waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        image = bkp.copy()
    imshow('image', image)

destroyAllWindows()





