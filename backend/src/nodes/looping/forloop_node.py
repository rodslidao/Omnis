if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

NODE_TYPE = "FORLOOP"


class ForLoopNode(BaseNode):
    def __init__(self, name, type, id, options, outputConnections) -> None:
        super().__init__(name, type, id, options, outputConnections)
        self.iterator = []
        self.backup = []
        NodeManager.addNode(self)

    def execute(self, message):
        target = message["targetName"]
        if target == "Lista":
            self.iterator = enumerate(message["payload"])
            self.backup = self.iterator.copy()
        elif target == "Trigger":
            try:
                self.id, self.item = next(self.iterator)
                self.on("item", self.item)
            except StopIteration:
                self.on("Fim")
            except Exception as e:
                self.onFailure(e)
