import re
from tkinter.font import BOLD
from src.nodes.base_node import BaseNode
from src.nodes.node_manager import NodeManager
from src.nodes.matrix.matrix_obj import Blister, Slot
from bson import ObjectId
from api import logger, exception, dbo
from api.decorators import for_all_methods
from numpy import array

NODE_TYPE = "MATRIX"


@for_all_methods(exception(logger))
class MatrixNode(BaseNode):
    """
    Inputs:
        matrix - Receives a matrix of data.
        next - iterate through the matrix.
    Outputs:
        Slot - A slot that contains the data.
        End - The end of the matrix.

    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.blister_id = options["blister_id"]["value"]
        self.blister = Blister(
            **dbo.find_one("blister-manager", {"_id": ObjectId(self.blister_id)})
        )

        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    def __next__(self):
        garbage = next(self.blister)
        self.on("item", garbage)
        return garbage

    def execute(self, message):
        target = message.targetName.lower()
        match target:
            case "reset":
                self.reset()
            case "next":
                return next(self)
            case "in_roi":
                garbage = self.blister.roi(message.payload)
                self.on(
                    "out_roi", garbage
                )  # ! Send data, or blister object? what is the best way?
                return garbage()
            case "end":
                self.reset()
                self.on("end", True)
            case "draw":
                self.blister.draw(message.payload)
            case _:
                return self.onFailure(message)
        if self.auto_run:
            return next(self)

    def reset(self):
        self.blister.reset_iterator()

    @staticmethod
    def get_info():
        return {
            "options": list(
                map(
                    MatrixNode.normalize_blister_get_info,
                    dbo.find_many("blister-manager", {}),
                )
            ),
        }

    @staticmethod
    def normalize_blister_get_info(blister):
        def set_X_Y(list_, sas=["X", "Y"]):
            return dict(zip(sas, list_))

        def verify(divisor):
            if divisor[1] == 0:
                return 1
            return array(blister["shape"])[divisor[0]] / divisor[1]

        sub = array(list(map(verify, enumerate(blister["slot_config"]["counter"]))))

        return {
            "_id": str(blister["_id"]),
            "name": blister["name"],
            "slot": {
                "qtd": set_X_Y((array(blister["shape"]) / sub).astype(int).tolist()),
                "margin": set_X_Y(blister["slot_config"]["borders"]),
                "size": set_X_Y(blister["slot_config"]["sizes"][:2]),
            },
            "subdivision": {
                "qtd": set_X_Y(sub.astype(int).tolist()),
                "margin": set_X_Y(blister["slot_config"]["extra"]),
            },
        }


if __name__ == "__main__":
    S2 = Slot(
        [6, 5, 0],
        [87.08, 80.68, 0],
        [23, 23, 0],
        [42.54, 19.5, 0],
        counter=[5, 3, 2],
        extra=[92.54, 93, 0],
        item="X",
    )

    print(vars(Blister(shape=[6, 6, 0], slot_config=S2)))
