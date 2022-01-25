if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode

NODE_TYPE = "PRINTER"


class PrinterNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.controller = options.hardware.get("controller")
        NodeManager.addNode(self)

    def execute(self, message):
        print(message)
        self.on("Next", message)
        pass
