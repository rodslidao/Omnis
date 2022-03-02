from cv2 import (
    drawContours,
    drawMarker,
    circle,
    arrowedLine,
    LINE_4,
    ellipse,
    imread,
    putText,
    FONT_HERSHEY_SIMPLEX,
    LINE_AA,
    imshow,
    waitKey,
    destroyAllWindows
)

import numpy as np
from src.nodes.identify.identify_functions import dimensional_data, identifyObjects

class draw(dimensional_data):
    def __init__(self,image=None, area=None, perimeter=None, diameter=None, AB=None, AC=None, AD=None, center=None, vertices=None, box=None, **kwargs):
        super().__init__(
            area,
            perimeter,
            diameter,
            AB,
            AC,
            AD,
            center,
            vertices,
            box,
        )
        self.image = image
    def drawBox(self):
        drawContours(self.image, [self.box], -1, (100, 100, 100), 1, LINE_4)

    def drawCircle(self):
        circle(self.image, tuple(self.center.values()), np.int0(self.diameter / 2), (255, 255, 255), 1)

    def drawCenter(self):
        drawMarker(
            self.image,
            tuple(self.center.values()),
            (255, 255, 255),
            markerType=2,
            markerSize=10,
            thickness=1,
        )

    def drawVertices(self):
        for k, n in self.vertices[1].items():

            drawMarker(self.image, tuple(n), (255, 255, 255), markerType=2, markerSize=10, thickness=1)
            putText(self.image, f"{k}", tuple(n), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, LINE_AA)
        # arrowedLine(self.image, self.box[0], self.box[1], (255, 0, 0), 1)
        # arrowedLine(self.image, self.box[0], self.box[2], (0, 255, 0), 1)
        # arrowedLine(self.image, self.box[0], self.box[3], (0, 0, 255), 1)

    def drawVerticesName(self):
        s = [[b, a] for a in [-1,1] for b in [-1,1]]
        s[2], s[3] = s[3], s[2]
        for _, l in enumerate(["A", "B", "C", "D"]):
            putText(
                self.image,
                l,
                (self.box[_][0] + (25*s[_][0]), self.box[_][1]+(25*s[_][1])),
                FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                LINE_AA,
            )
    def drawRectSize(self):
        for _, l in enumerate(["AB", "AC", "AD"]):
            putText(self.image, f"{l}: {round(self.get(l),2)}", (self.box[2][0]+25, int(self.diameter+(self.diameter*0.3*(1+_)))), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, LINE_AA)
    
    def drawAngles(self, _angle):
        ellipse(self.image, center=tuple(self.center.values()), axes=(20, 20), angle=0, startAngle=_angle*-1, endAngle=0.0, color=(255, 0, 255), thickness=1)
    

    
    def drawAll(self):
        self.drawBox()
        # self.drawCircle()
        # self.drawCenter()
        self.drawVertices()
        # self.drawVerticesName()
        # self.drawRectSize()
        # self.drawAngles(90)
        return self.image

def find_angle(origin, point, degrees=True, positive=False):
    angle = np.angle(complex(*(point[0] - origin[0], origin[1] - point[1])), degrees)
    if angle < 0 and positive: angle += 360
    return angle