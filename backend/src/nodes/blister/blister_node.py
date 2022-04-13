from backend.src.nodes.base_node import BaseNode
from src.nodes.node_manager import NodeManager
from src.nodes.blister.blister_obj import Blister, Slot
from src.manager.blister_manager import BlisterManager
from numpy import ndenumerate
from api import logger, exception

NODE_TYPE = "BLISTER"


class BlisterNode(BaseNode):
    """
    Inputs:
        matrix - Receives a matrix of data.
        next - iterate through the matrix.
    Outputs:
        Slot - A slot that contains the data.
        End - The end of the matrix.

    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.shape = options.get("shape")
        self.slot_config = options.get("slot_config")
        self.blister = Blister(self.shape, BlisterManager.get_by_id(self.slot_config))
        # self.blister = Blister(shape=options["shape"], slot_config=options["S2"])
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    def __next__(self):
        self.on("item", next(self.slot_config))

    @exception(logger)
    def execute(self, message):
        target = message.targetName.lower()
        match target:
            case "reset":
                self.reset()
            case "next":
                return next(self)
            case "in_roi":
                self.on("out_roi", self.blister.roi(message.payload))
                return
            case "config":
                self.blister = Blister(
                    shape=self.shape,
                    slot_config=message.payload
                    if isinstance(message.payload, (dict, Slot))
                    else BlisterManager.get_by_id(message.payload),
                )
                return self.reset()
            case "end":
                self.reset()
                self.on("end", True)
            case _:
                return self.onFailure(message)
        if self.auto_run:
            return next(self)

    def reset(self):
        self.blister.reset_iterator()

    # def order(self, message):
    #     return message.payload.flatten()[0]

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "option_name": "option_accepted_values",
            }
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
