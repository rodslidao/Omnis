from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from datetime import datetime
from api import logger, exception

NODE_TYPE = "BUTTON"


class ButtonNode(BaseNode):
    """
    Signals ->
    \t:onClick: - Envia um sinal de click. \n
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        """
        Executes the node.
        """

        self.on("onClick", datetime.now())

    @exception(logger)
    def reset(self):
        """
        Resets the node.
        """
        # ExecutionCounter.resetCountType(self._id)
        return True
