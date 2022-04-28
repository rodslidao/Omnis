from math import sqrt
from cv2 import (
    CHAIN_APPROX_TC89_KCOS,
    TERM_CRITERIA_MAX_ITER,
    CHAIN_APPROX_TC89_L1,
    CHAIN_APPROX_SIMPLE,
    CHAIN_APPROX_NONE,
    TERM_CRITERIA_EPS,
    RETR_FLOODFILL,
    RETR_EXTERNAL,
    RETR_CCOMP,
    RETR_LIST,
    RETR_TREE,
)

from cv2 import (
    connectedComponentsWithStats,
    minEnclosingCircle,
    approxPolyDP,
    boundingRect,
    cornerHarris,
    cornerSubPix,
    findContours,
    contourArea,
    minAreaRect,
    arcLength,
    boxPoints,
    threshold,
    moments,
    blur,
)


from numpy import angle, float32, int0, uint8, ndenumerate
from bson.objectid import ObjectId
from api import logger, exception
from api.decorators import for_all_methods
from src.nodes.blister.blister_obj import Blister

# Map of modes to use for the contour retrieval
modes = {
    "RETR_LIST": RETR_LIST,
    "RETR_EXTERNAL": RETR_EXTERNAL,
    "RETR_CCOMP": RETR_CCOMP,
    "RETR_TREE": RETR_TREE,
    "RETR_FLOODFILL": RETR_FLOODFILL,
}

# Map of methods to use for the contour retrieval
methods = {
    "CHAIN_APPROX_NONE": CHAIN_APPROX_NONE,
    "CHAIN_APPROX_SIMPLE": CHAIN_APPROX_SIMPLE,
    "CHAIN_APPROX_TC89_L1": CHAIN_APPROX_TC89_L1,
    "CHAIN_APPROX_TC89_KCOS": CHAIN_APPROX_TC89_KCOS,
}


# class that represent a dimensional object
@for_all_methods(exception(logger))
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
        edges=None,
        corners=None,
        countour=None,
        box=None,
        center_dist=None,
    ):
        self._id = ObjectId()
        self.area = area
        self.perimeter = perimeter
        self.diameter = diameter
        self.AB = AB
        self.AC = AC
        self.AD = AD
        self.center = center
        self.edges = edges
        self.corners = corners
        self.countour = countour
        self.box = box
        self.center_dist = center_dist
        self.angle = self.getAngle()[1]

    def getAngle(self, pivot="A"):
        if pivot in ["A", "B", "C", "D"]:
            self.pivot = self.edges[pivot]
        elif isinstance(pivot, (tuple, list)):
            self.pivot = pivot
        elif pivot <= len(self.corners) - 1:
            self.pivot = self.corners[pivot]
        else:
            return False, 0
        self.angle = find_angle(tuple(self.center.values()), self.pivot)
        return True, self.angle

    def get(self, key):
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)

    def __str__(self) -> str:
        _ = {i: self.__dict__[i] for i in self.__dict__ if i in ["area"]}
        return f"((dimensional_data) {_})"

    def __repr__(self):
        return str(self)

    def __call__(self):
        return vars(self)


@exception(logger)
def find_corners(mask):
    img = blur(mask, (3, 3))
    dst = cornerHarris(img, 10, 3, 0.04)
    dst = threshold(dst, 0.1 * dst.max(), 255, 0)[1]
    centroids = connectedComponentsWithStats(uint8(dst))[3]
    criteria = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 100, 0.001)
    return int0(cornerSubPix(mask, float32(centroids), (5, 5), (-1, -1), criteria))[1:]


@exception(logger)
def find_angle(origin, point, degrees=True, positive=True):
    _a = angle(complex(*(point[0] - origin[0], origin[1] - point[1])), degrees)
    if _a < 0 and positive:
        _a += 360
    return _a


# Function to get the contours of an image
@exception(logger)
def identifyObjects(
    images_array, mode="RETR_TREE", method="CHAIN_APPROX_SIMPLE", **parm
):

    """
    :image: image to get the contours from\n
    :mode: mode to use for the contour retrieval\n
    :method: method to use for the contour approximation\n
    :parm: additional parameters to pass to the contour retrieval\n
    :returns: a list of contours\n
    \n
    Note: 'parms' need be in the pattern of:\n
        {\n
            parameter: {\n
                min: value,\n
                max: value\n
            }\n
        }\n
    \n
    \tAccepted parameters are: [area, radius, diamter, perimeter, vertices, width, height].
    """

    # Define the mode, and method to use for the contour retrieval
    md = modes.get(mode, RETR_TREE)
    mt = methods.get(method, CHAIN_APPROX_SIMPLE)

    # function tha verify if some var need to be tested, and then test it
    @exception(logger)
    def verify(var, name):
        var_d = parm.get(name, False)
        if not var_d:
            return True
        if var and (var > var_d["min"] and var < var_d["max"]):
            return True
        return False

    for index, slot in (
        ndenumerate(images_array)
        if not isinstance(images_array, Blister)
        else images_array
    ):
        dimensional_object_list = []
        image = slot.item
        # Find the contours in the image
        contours, _ = findContours(image, md, mt)
        for contour in contours:
            # calculate area, and reject contours that are too small or too large
            area = contourArea(contour)
            if not verify(area, "area"):
                continue
            # calculate radius, and reject contours that are too small or too large
            (x, y), radius = minEnclosingCircle(contour)
            if not verify(radius, "radius"):
                continue

            # calculate diameter, and reject contours that are too small or too large
            diameter = 2 * radius
            if not verify(diameter, "diameter"):
                continue

            # calculate perimeter, and reject contours that are too small or too large
            perimeter = arcLength(contour, True)
            if not verify(perimeter, "perimeter"):
                continue

            # calculate width, and reject contours that are too small or too large
            vertices = approxPolyDP(contour, 0.01 * perimeter, True)
            if not verify(len(vertices), "vertices"):
                continue

            # calculate width and height, and reject contours that are too small or too large
            x, y, w, h = boundingRect(contour)
            if not verify(w, "width") or not verify(h, "height"):
                continue

            box = int0(boxPoints(minAreaRect(contour)))
            A, B, C, D = box
            edges = {"A": A, "B": B, "C": C, "D": D}

            # Improve corners detection
            n = 10  # px off-set from image boundaries to avoid errors.
            corners = [
                [cord[0] + A[0] - n, cord[1] + B[1] - n]
                for cord in find_corners(
                    image[
                        A[1] - n if A[1] >= n else 0 : D[1] + n,
                        B[0] - n if B[0] >= n else 0 : C[0] + n,
                    ]
                )
            ]

            # calculate diagonals, and reject contours that are too small or too large
            def distance(p1, p2):
                return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            AB = distance(A, B)
            if not verify(AB, "AB"):
                continue

            AC = distance(A, C)
            if not verify(AC, "AC"):
                continue

            AD = distance(A, D)
            if not verify(AD, "AD"):
                continue

            if AB is None or AC is None or AD is None:
                continue

            # calculate center of mass
            M = moments(contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            center = {"X": cx, "Y": cy}
            center_dist = {
                "X": int(cx - (image.shape[1] / 2)),
                "Y": int(cy - (image.shape[0] / 2)),
            }

            if len(corners) == 0:
                corners = [
                    [int(center["X"] - (diameter / 2)), center["Y"]],
                    [center["X"], int(center["Y"] - (diameter / 2))],
                    [int(center["X"] + (diameter / 2)), center["Y"]],
                    [center["X"], int(center["Y"] + (diameter / 2))],
                ]

            # ! Define an output shape, and pre-allocate an array for the result.
            # ! shape is used to define a ROI of the image.
            # ! The ROI is a rectangle, where (x, y) is the top left corner, and (w, h) is the width and height.
            # ! The shape is defined by the center of the object, and the width and height of the object.
            # ! Create a ROI class or use IMAGE
            dimensional_object_list.append(
                dimensional_data(
                    area,
                    perimeter,
                    diameter,
                    AB,
                    AC,
                    AD,
                    center,
                    edges,
                    corners,
                    contour,
                    box,
                    center_dist,
                )
            )
        # return list of dimensional objects that passed all tests
        # ? dimensional_object_list if parm.get("return_list", False) else dimensional_object_list[0]

        slot.item = dimensional_object_list if not parm.get("boolean", False) else True
    return images_array


# parameters to filter contours (Example)
# parm = {

#     "area":{
#         "min":10,
#         "max":100
#     },

#     "perimeter":{
#         "min":10,
#         "max":100
#     },

#     "diameter":{
#         "min":10,
#         "max":100
#     },

#     "radius":{
#         "min":10,
#         "max":100
#     },

#     "AB":{
#         "min":10,
#         "max":100
#     },

#     "AC":{
#         "min":10,
#         "max":100
#     },

#     "AD":{
#         "min":10,
#         "max":100
#     },

#     "width":{
#         "min":10,
#         "max":100
#     },

#     "height":{
#         "min":10,
#         "max":100
#     },
# }
# -- not included yet --
#     "edges":{
#         "min":10,
#         "max":100
#     },

#    "corners":{
#         "min":10,
#         "max":100
#     },
# }
