from src.manager.base_manager import BaseManager
from src.crud import CRUD
from src.nodes.matrix.matrix_obj import Blister as Matrix
from api import logger, dbo
from numpy import fromiter
from bson import ObjectId


def convert_to_array(dict_, type_=float):
    return fromiter(dict_.values(), dtype=type_)


def adapter(**kwargs):
    slots = kwargs["input"]["slots"]
    subdivisions = kwargs["input"]["subdivisions"]
    kwargs.update({'input':{
        "name": kwargs["input"]["name"],
        "shape": (convert_to_array(slots["qtd"], int) * convert_to_array(subdivisions["qtd"], int)).tolist(),
        "order": kwargs["input"].get("order", "TLR"),
        "slot_config": {
            "sizes": convert_to_array(slots["size"]).tolist(),
            "borders": convert_to_array(slots["margin"]).tolist(),
            "origin": convert_to_array(kwargs["input"]["origin"]).tolist(),
            "counter": convert_to_array(slots["qtd"], int).tolist(),
            "extra": convert_to_array(subdivisions["margin"]).tolist(),
            "scale": float(kwargs["input"].get("scale", 1)),
        },
        "_id": ObjectId(kwargs["input"].get("_id", kwargs['_id']))
    }})
    return kwargs


class MatrixObjectManager(CRUD):
    def __init__(self, collection, auth_level):
        super().__init__(collection=collection, auth_level=auth_level)

    def change_collection(name, conversor):
        def resolver(func):
            def wrapper(*args, **kwargs):
                _id = func(*args, **kwargs)
                kwargs.update({"_id": _id})
                _kwargs = conversor(**kwargs) if kwargs.get("input") else kwargs
                _kwargs.update({"collection": name})
                func(*args, **_kwargs)
                return True
            return wrapper
        return resolver

    @change_collection("matrix-manager", adapter)
    def create(self, *args, **kwargs):
        return CRUD.create(self, *args, **kwargs)

    @change_collection("matrix-manager", adapter)
    def update(self, *args, **kwargs):
        return CRUD.update(self, *args, **kwargs)

    @change_collection("matrix-manager", adapter)
    def delete(self, *args, **kwargs):
        return CRUD.delete(self, *args, **kwargs)

    def __call__(self, matrix=None):
        if matrix:
            self.matrix = matrix
        return self.matrix

    @property
    def matrix(self):
        return self.store[self.selected_matrix_id]

    @matrix.setter
    def matrix(self, _id):
        self.selected_matrix_id = _id


MatrixManager = MatrixObjectManager("matrix", "operator")