from cv2 import RETR_LIST, RETR_EXTERNAL, RETR_CCOMP, RETR_TREE, RETR_FLOODFILL
from cv2 import (
    CHAIN_APPROX_NONE,
    CHAIN_APPROX_SIMPLE,
    CHAIN_APPROX_TC89_L1,
    CHAIN_APPROX_TC89_KCOS,
)

from cv2 import (
    findContours,
    boundingRect,
    contourArea,
    arcLength,
    boxPoints,
    minAreaRect,
    minEnclosingCircle,
    moments,
    approxPolyDP,
)

from numpy import int0
from bson.objectid import ObjectId

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
        self._id = ObjectId()
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

    def set(self, key, value):
        setattr(self, key, value)

    def __call__(self):
        return vars(self)


# Function to get the contours of an image
def identifyObjects(image, mode="RETR_TREE", method="CHAIN_APPROX_SIMPLE", **parm):

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
    \tAccepted paramters are: [area, radius, diamter, perimeter, vertices, width, height].
    """

    # Define the mode, and method to use for the contour retrieval
    md = modes.get(mode, RETR_TREE)
    mt = methods.get(method, CHAIN_APPROX_SIMPLE)

    # Find the contours in the image
    contours, hierarchy = findContours(image, md, mt)

    # function tha verify if some var need to be tested, and then test it
    def verify(var, name):
        var_d = parm.get(name, False)
        if not var_d:
            return True
        if var and (var > var_d["min"] and var < var_d["max"]):
            return True
        return False

    dimensional_object_list = []
    for component in zip(contours, hierarchy):
        contour = component[0]
        hierarchy = component[1]

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
        sortedBoxX = sorted(box, key=lambda x: x[0])
        sortedBoxY = sorted(box, key=lambda x: x[1])

        A, B, C, D = (
            tuple(sortedBoxX[0]),
            tuple(sortedBoxX[-1]),
            tuple(sortedBoxY[0]),
            tuple(sortedBoxY[-1]),
        )

        # calculate diagonals, and reject contours that are too small or too large

        AB = (abs(A[0] - B[0]) ** 2 + abs(A[1] - B[1]) ** 2) ** 0.5
        if not verify(AB, "AB"):
            continue

        AC = (abs(A[0] - C[0]) ** 2 + abs(A[1] - C[1]) ** 2) ** 0.5
        if not verify(AC, "AC"):
            continue

        AD = (abs(A[0] - D[0]) ** 2 + abs(A[1] - D[1]) ** 2) ** 0.5
        if not verify(AD, "AD"):
            continue

        # calculate center of mass
        M = moments(contour)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        center = {"X": cx, "Y": cy}

        # create dimensional object and append to list
        dimensional_object_list.append(
            dimensional_data(
                area, perimeter, diameter, AB, AC, AD, center, vertices, box
            )
        )

    # return list of dimensional objects that passed all tests
    return dimensional_object_list


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

#     "vertices":{
#         "min":10,
#         "max":100
#     },
# }
