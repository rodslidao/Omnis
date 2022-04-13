from bson import ObjectId
from src.manager.mongo_manager import CustomEncoder
from src.manager.blister_manager import BlisterManager
from numpy import (
    ndarray,
    ndenumerate,
    generic,
    array
)
from json import loads, dumps

#! Slot should be a self-contained class or Node?
class Slot:
    """
    Slot is a class that represents a slot in a grid/blister of slots.
    all the attributes except (item, empty, counter and _id) are dimensions in an unit 'x' or coordinates in a world of this unit. eg.
    all coordinates are the distance from the origin of the world (0,0) at top left corner.
    
    origin = (20,10), means that the FIRST SLOT start 20mm from the left and 10mm from the top.
    position = (0,0), means that THIS SLOT in the first column and first row in the grid.
    sizes = (100,100), means that the slots is 100mm wide and 100mm high
    borders = (10,10), means that the slots has 10mm of border on the left and top.
    counter = (2, 1), means that every 2 slots at X axis and 1 slot at Y axis will sum extra border.
    extra = (10,0), means that 10mm of extra border will be added to the slots at X axis, after counter.
    Example:
        origin = (20,10)
        sizes = (100,100)
        borders = (10,10)
        counter = (2, 1)
        extra = (10,0)
        
        Slot at postion (0,0):
            start at: (20, 10)
            ends at: (120, 110)
            center at: (70, 60)
        
        Slot at postion (1,0):
            start at: (130, 10) | x not is 120 because of border X10mm
            ends at: (230, 110) | x not is 220 because of border X10mm
            center at: (180, 60)
        
        Slot at postion (0,1):
            (20, 110) (120, 210) [ 70. 160.]
            start at: (20, 110) | y not is 100 because of border Y10mm
            ends at: (120, 210) | y not is 200 because of border Y10mm
            center at: (70, 160)
        
        Slot at postion (1,1):
            (130, 110) (230, 210) [180. 160.]
            start at: (130, 110) | not is (120, 100) because of border at both axis
            ends at: (230, 210) | not is (220, 200) because of border at both axis
            center at: (180, 160)

    """

    def __init__(
        self,
        position,
        origin,
        sizes,
        borders,
        counter=[0, 0],
        extra=[0, 0],
        item=None,
        _id=None,
        **kwargs,
    ):
        self._id = ObjectId(_id)
        self.sizes = array(sizes)
        self.borders = array(borders)
        self.width, self.height = sizes[:2]
        self.origin = array(origin)
        self.item = item
        self.position = array(position)
        self.counter = array(counter)
        self.extra = array(extra)
        M = array(list( (p/c) if c > 0 else 0 for p, c in zip(self.position, self.counter))).astype(int)
        self.center = array(
            (self.borders * self.position)
            + (self.origin + (((self.sizes) * (self.position + 1)) - (self.sizes / 2)))
            + ((self.extra * M) - (self.borders * M))
        )
        self.start = tuple((self.center[:2]-(self.sizes[:2]/2)).astype(int))
        self.end =   tuple((self.center[:2]+(self.sizes[:2]/2)).astype(int))
        # (BN * P)+(O + (S / 2)) + int((BE * (P / C)) - (BN * (P / C)))
        
    def __call__(self):
        return {i:getattr(self, i) for i in vars(self) if i!='_id'}

    def __str__(self) -> str:
        return f"{self.item} at {self.center}."
    
    def export(self):
        _ = loads(dumps(self(), cls=CustomEncoder))
        _['_id'] = self._id
        return _


class Blister():
    """
        Blister is a class that represents a 2D matrix of slots.\n
        It is used to store the data of the blister, and dinamicly generate the slots.\n
        It is also used to iterate over the slots.

        blister_example = Blister(shape=(10, 10), slot_config={'origin':[0, 0], 'sizes':[50, 50], 'borders':[15, 0]})

        next(blister_example) -> (0, 0), Slot(position = [0, 0], center = [25., 25.])\n
        next(blister_example) -> (0, 1), Slot(position = [1, 0], center = [90., 25.])
        
        update_all_items(item): Change all slots item the new item.
        update_item(item, position): Change the slot at position with the new item.
        update_data(data): Change the data of the blister. data must be a 2Dnp array of Slot objects.
        generate_data(shape, **kwargs): Generate the data of the blister. kwargs must be a dict with the slot_config.
        reset_iterator(): Reset the iterator to the first slot. (when iterating over the slots this method is called automatically)
        draw(image): Draw the blister slots on the image.
        roi(image): crop all slots for the given image, and return as another blister (same shape and config) with the items as the respective crop.
        get_slot(position): Return the slot at position.
        blister(): Return 2D np array of Slot objects.
        blister(i,j): Return the slot at position (i,j).
        blister(i,j,v): Change the slot at position (i,j) with the new value.
        export(): Return the data of the blister as a dict with numpy types converted.

        ** Note **

        Slots.position is not same as the position of the slot in the blister.
        Slots.position is the position as a coorditane (X,Y) in the blister.
        blister.data[i,j] is the slot at data[i,j] position (y,x).\n
        [[00,10,20,30],  i=0, j(x)=0,1,2,3 | blister.data[0,2].position = (2,0) or 20\n
         [01,11,21,31],  i=1, j(x)=0,1,2,3 |\n
         [02,12,22,32],  i=2, j(x)=0,1,2,3 |\n
         [03,13,23,33]]  i=3, j(x)=0,1,2,3 |\n


    """

    def __init__(self, shape, slot_config,_id=None, **kwargs) -> None:
        self._id=ObjectId(_id)
        self.slot_config = slot_config if not isinstance(slot_config, Slot) else slot_config()
        self.shape = shape
        self.kwargs = kwargs
        self.data = self.generate_data(shape, **self.slot_config) 
        self.reset_iterator()
        BlisterManager.add(self)
    
    @staticmethod
    def is_array(array):
        return isinstance(array, (ndarray, list, generic))
    
    @staticmethod
    def is_slot(slot):
        return isinstance(slot, Slot)

    def update_item(self, item, position):
        self.data[position[0], position[1]].item = item
        self.data[position[0], position[1]].empty = False
        return self.data
    
    def update_all_items(self, item):
        for _, slot in ndenumerate(self.data):
            slot.item = item
            slot.empty = False
        return self.data

    def update_data(self, data):
        #? Map cant iterate over a matrix, soo compare a converted matrix to a ndarray, if pass, update data.
        assert all(map(lambda x: Blister.is_array(x) and all(map(lambda y: Blister.is_slot(y), x)), array(data))), "Data must be a ('N'D | N>=2) arrayof Slot objects."
        self.data = data

    @staticmethod
    def generate_data(shape, origin, sizes, borders, counter=[0,0], extra=[0,0], **kwargs):
        return array(
            [
                [
                    Slot(
                        position=[x, y],
                        origin=origin,
                        sizes=sizes,
                        borders=borders,
                        counter=counter,
                        extra=extra,
                        item=kwargs.get('new_item', kwargs.get('item', None)),
                    )
                    for x in range(shape[0])
                ]
                for y in range(shape[1])
            ]
        )

    def get_slot(self, position):
        return self.data[position[0], position[1]]
    
    def reset_iterator(self):
        self.iterator = ndenumerate(self.data)
        return self.iterator

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.reset_iterator()
            return next(self.iterator)

    def __call__(self, r=None, c=None, v=None):
        if r is not None and c is not None:
            if v is not None:
                self.update_item(v, [r, c])
            return self.data[c, r]
        else:
            return self.data

    # def draw(self, image=None):
    #     for _, slot in ndenumerate(self.data):
    #         cv2.drawMarker(image, tuple((slot.center[:2].astype(int))), (0,0,255))
    #         cv2.rectangle(image, slot.start, slot.end, (0, 1,0), 1)
    #         cv2.putText(image, str(slot.position[:2]), tuple((slot.center[:2].astype(int))+[5,-5]), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    #     return image

    def roi(self, image):
        temp = Blister(shape=self.shape, slot_config=self.slot_config)
        for _, slot in ndenumerate(self.data):
            temp.update_item(image[slot.start[1]:slot.end[1], slot.start[0]:slot.end[0]], slot.position[:2][::-1])
        return temp
    
    def export(self):
        data = loads(dumps({'shape':self.shape, 'slot_config':self.slot_config, 'kwargs':self.kwargs}, cls=CustomEncoder))
        data['_id'] = self._id
        return data