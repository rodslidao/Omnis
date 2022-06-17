from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode, Wizard
from api import logger, exception
from api.decorators import for_all_methods
from src.utility.system.sleep_alternative import sleep
NODE_TYPE = "DelayNode"


@for_all_methods(exception(logger))
class DelayNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        NodeManager.addNode(self)

    @Wizard._decorator
    def execute(self, message=""):
        sleep(float(self.options["delay"]))
        self.on("Saida", message)