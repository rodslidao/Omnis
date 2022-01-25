if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode
from nodes.timer.task_time import setInterval
import builtins

NODE_TYPE = "VARIABLE"


class VariableNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        name, _type, value = options.settings
        self.var = {name: getattr(builtins, _type)(value)}
        self.stop_event = self.execute()
        NodeManager.addNode(self)

    @setInterval(0.5)
    def execute(self, message="None"):
        self.on("Value", self.var)

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.stop_event = self.execute()
