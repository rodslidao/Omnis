from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from datetime import datetime
from api import logger, exception, for_all_methods

NODE_TYPE = "BUTTON"


@for_all_methods(exception(logger))
class ButtonNode(BaseNode):
    """
    Signals ->
    \t:onClick: - Envia um sinal de click. \n
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    def execute(self, message):
        """
        Executes the node.
        """

        self.on("onClick", datetime.now())

    def reset(self):
        """
        Resets the node.
        """
        # ExecutionCounter.resetCountType(self._id)
        return True
