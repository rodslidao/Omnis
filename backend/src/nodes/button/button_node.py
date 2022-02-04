if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
#from src.exec_info import ExecutionCounter
from datetime import datetime

NODE_TYPE = "BUTTON"


class ButtonNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        NodeManager.addNode(self)

    def execute(self, message):
        self.on("onClick", datetime.now())

    def reset(self):
        #ExecutionCounter.resetCountType(self._id)
        return True
