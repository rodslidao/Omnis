from bson import ObjectId
from numpy import array, matrix, ndenumerate

#! Slot should be a self-contained class or Node?
class Slot:
    def __init__(
        self,
        position,
        origin,
        sizes,
        borders,
        counter=[1, 1, 1],
        extra=[0, 0, 0],
        item=None,
        _id=None,
        **kwargs,
    ):
        self._id = ObjectId(_id)
        self.sizes = array(sizes)
        self.borders = array(borders)
        self.width, self.height, self.depth = sizes
        self.origin = array(origin)
        self.item = item
        self.empty = bool(item)
        self.position = array(position)
        self.counter = array(counter)
        self.extra = array(extra)
        M = (self.position / self.counter).astype(int)
        self.center = (
            (self.borders * self.position)
            + (self.origin + (((self.sizes) * (self.position + 1)) - (self.sizes / 2)))
            + ((self.extra * M) - (self.borders * M))
        )
        self.start = tuple((self.center[:2]-(self.sizes[:2]/2)).astype(int))
        self.end =   tuple((self.center[:2]+(self.sizes[:2]/2)).astype(int))
        # (BN * P)+(O + (S / 2)) + int((BE * (P / C)) - (BN * (P / C)))
    def set_origin(self, origin):
        self.origin = origin
        return self

    def __call__(self):
        return vars(self)

    def __str__(self) -> str:
        return f"{self.item} at {self.center}"


class Blister():
    def __init__(self, shape, slot_config, **kwargs) -> None:
        self.rows, self.columns, self.layers = shape
        self.slot_config = slot_config
        self.data = matrix(
            [
                [
                    Slot(
                        position=[x, y, 0],
                        origin=slot_config.origin,
                        sizes=slot_config.sizes,
                        borders=slot_config.borders,
                        counter=slot_config.counter,
                        extra=slot_config.extra,
                    )
                    for x in range(shape[0])
                ]
                for y in range(shape[1])
            ]
        )

    def __call__(self, i=None, j=None, v=None):
        if i is not None and j is not None:
            if v is not None:
                self.data[i, j] = Slot(
                    *self.slot_dim, [i, j], self.slot_origin, item=v
                )
            return self.data[i, j]
        else:
            return self.data
    """
    # ! Change do draw_node, but how? 
    def draw(self, image=None):
        for index, slot in np.ndenumerate(self.data):
            cv2.drawMarker(image, tuple((slot.center[:2].astype(int))), (0,0,255))
            cv2.rectangle(image, slot.start, slot.end, (0, 1,0), 1)
            cv2.putText(image, str(index), tuple((slot.center[:2].astype(int))+[5,-5]), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, lineType=cv2.LINE_AA)
        return image
    """            
    def ROI(self, image):
        data = array([[None for _ in range(self.rows)] for _ in range(self.columns)])
        for index, slot in ndenumerate(self.data):
            data[index] = image[slot.start[1]:slot.end[1], slot.start[0]:slot.end[0]]
            """
            # ! If you want to draw the slots, uncomment the line below, and add the draw function to the Blister class.
            # ! waitKey('n' | n >= 500), will be needed to see the window, can be here on in another part of the code.
            cv2.imshow(str(index), data[index])
            cv2.moveWindow(str(index), *slot.start)
            """
        return data

