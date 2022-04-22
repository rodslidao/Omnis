from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception, for_all_methods

NODE_TYPE = "DIFFERENCE"


@for_all_methods(exception(logger))
class DifferenceNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections

        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    def execute(self, message=""):
        try:
            self.onSuccess()
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))
