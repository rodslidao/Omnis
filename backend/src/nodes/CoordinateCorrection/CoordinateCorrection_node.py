from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "COORDINATECORRECTION"


class CoordinateCorrectionNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        
        self.cords = {}
        self.scale = options["scale"]
        self.offset = options["offset"]
        
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        self.output = {}

        if message.targetName == "coords":
            self.cords = message.payload

        # multuiply by scale and sum offset in each dimension
        print("original cords: ", self.cords)
        if self.cords is not None:
            for c,s,v in zip(self.cords.items(), self.scale.values(), self.offset.values()):
                self.output[c[0]] = (c[1] * s) + v
        print("scaled cords: ", self.output)
        self.onSuccess(self.output)

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {}
        }
