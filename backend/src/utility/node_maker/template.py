from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "node_type"


class class_name(BaseNode):
    """
    node_description
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.auto_run = options["auto_run"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        self.onSuccess()

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "option_name": "option_accepted_values",
            }
        }
