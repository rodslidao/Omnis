from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode, Wizard
from api import logger, exception
from api.decorators import for_all_methods

NODE_TYPE = "node_type"


@for_all_methods(exception(logger))
class class_name(BaseNode):
    """
    node_description
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.auto_run = options.get("auto_run", False)
        NodeManager.addNode(self)

    @Wizard._decorator
    def execute(self, message=""):
        self.onSuccess()

    @staticmethod
    def get_info(**kwargs):
        return {
            "options": {
                "option_name": "option_accepted_values",
            }
        }
