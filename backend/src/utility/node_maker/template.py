from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

NODE_TYPE = "node_type"

class class_name(BaseNode):
    """
    node_description
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections

        NodeManager.addNode(self)

    def execute(self, message=""):
        try:
            self.onSuccess()
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))
