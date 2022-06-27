from cv2 import log
from pandas import value_counts
from api import dbo
from bson import ObjectId
from api import logger
class variable:
    def __init__(self, _id=None) -> None:
        self.update(_id)

    @property
    def value(self):
        return self.__value
    
    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def update(self, _id):
        self._id = ObjectId(_id)
        self.__dict = dbo.find_one('variables', {'_id':self._id})
        self.__atual = self.__dict['atual']
        self.collection = self.__atual.get('collection')
        self.__value = self.__atual if not self.__atual.get('_id') else dbo.find_one(self.collection, {'_id':ObjectId(self.__atual['_id'])})

    def get(self, attr):
        return self.__dict.get(attr)


class target:
    def __init__(self, _id):
        self.update(_id)

    @property
    def variables_ids(self):
        return self.__dict['variables']

    def get(self, attr):
        return self.__dict.get('attr')
    
    def update(self, _id):
        self._id = ObjectId(_id)
        self.__dict = dbo.find_one('targets', {'_id': self._id})
        self.variables = [variable(ObjectId(_id_['_id'])) for _id_ in self.variables_ids]


class targets:
    def __init__(self, *ids) -> None:
        self.values = {}
        self(*ids)
    
    def __call__(self, *values):
        self.values.clear()
        for value in values:
            for var in value.variables:
                self.values[var.get('name')] = var

targets = targets()