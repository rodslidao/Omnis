from multiprocessing.sharedctypes import Value
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.compare.compare_funcs import comparatives
from api import logger, exception

NODE_TYPE = "COMPARATIVE"


class CompareNode(BaseNode):
    """
    Node to execute logical operations between values.
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.operation = options["operation"]
        self.value1 = options["value1"]
        self.value2 = options["value2"]
        self.value3 = options["value3"]
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        target = message.targetName.lower()
        getattr(self, target)(message)
        pass

    @exception(logger)
    def value1(self, message):
        self.value1 = message.payload

    @exception(logger)
    def value2(self, message):
        self.value2 = message.payload

    @exception(logger)
    def value3(self, message):
        self.value3 = message.payload

    @exception(logger)
    def trigger(self, message):
        try:
            self.onSuccess(
                comparatives[self.operation](self.value1, self.value2, self.value3)
            )
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))
