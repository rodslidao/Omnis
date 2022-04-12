from src.nodes.node_manager import NodeManager
from src.nodes.blister.blister_obj import Blister, Slot
from src.nodes.looping.forloop_node import ForloopNode
from api import logger, exception

NODE_TYPE = "BLISTER"


class BlisterNode(ForloopNode):
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
        self.matrix = options["matrix"]
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        target = message.targetName
        if target == "iterator":
            message.payload = self.order(message)
            self.iterator = enumerate(message.payload)
        super.execute(message)

    def order(self, message):
        return message.payload.flatten()[0]

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
    item='X',
)

    print(vars(Blister(shape=[6, 6, 0], slot_config=S2)))



