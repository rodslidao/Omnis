from cv2 import (
    drawContours,
    drawMarker,
    circle,
    arrowedLine,
    line,
    LINE_4,
    ellipse,
    putText,
    FONT_HERSHEY_SIMPLEX,
    LINE_AA
)

from numpy import int0
from src.nodes.identify.identify_functions import dimensional_data

class DrawOBJ(dimensional_data):
    def __init__(self,image=None, area=None, perimeter=None, diameter=None, AB=None, AC=None, AD=None, center=None, edges=None, corners=None, countour=None, box=None, **kwargs):
        super().__init__(
            area,
            perimeter,
            diameter,
            AB,
            AC,
            AD,
            center,
            edges,
            corners,
            countour, 
            box
        )
        self.image = image
    def drawBox(self):
        drawContours(self.image, [self.box], -1, (100, 100, 100), 1, LINE_4)

    def drawCircle(self):
        circle(self.image, self.center, int0(self.diameter / 2), (255, 255, 255), 1)

    def drawCenter(self):
        drawMarker(
            self.image,
            self.center,
            (255, 255, 255),
            markerType=2,
            markerSize=10,
            thickness=1,
        )

    def drawVertices(self):
        for n in self.edges.values():
            arrowedLine(self.image, self.edges['A'], n, (255, 0, 0), 1, line_type=LINE_AA)

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
            putText(self.image, f"{l}: {round(self.get(l),2)}", (self.edges['C'][0], self.edges['B'][1]+25+int(25*_)), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, LINE_AA)
    
    def drawAngles(self):
        print(self.angle)
        ellipse(self.image, center=self.center, axes=(20, 20), angle=0, startAngle=self.angle*-1, endAngle=0.0, color=(255, 0, 255), thickness=1)
        line(self.image, self.center, self.pivot, (255, 255, 0), 1)

        line(self.image, self.center, (self.center[0]+20, self.center[1]), (255, 0, 0), 1)
        putText(self.image, f"{round(self.angle, 2)}", (self.center[0], self.center[1]-25), FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, LINE_AA)
    def drawCountour(self):
        drawContours(self.image, [self.countour], -1, (0, 0, 255), -1, LINE_4)

    def drawCorners(self):
        for i in range(len(self.corners)):
            circle(self.image, self.corners[i], 7, (0,255,0), 2)

    def drawAll(self):
        self.drawCountour()
        self.drawBox()
        self.drawCorners()
        self.drawCircle()
        self.drawCenter()
        self.drawVertices()
        self.drawRectSize()
        self.drawAngles() 
            
        return self.image