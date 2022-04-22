from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.process.process import process
from api import logger, exception, for_all_methods
NODE_TYPE = "PROCESS"

process_options ={
    'stop': process.stop,
    'pause': process.pause
}


@for_all_methods(exception(logger))
class ProcessNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.function = process_options.get(options["action"].get("value", 'stop'), 'stop')
        self.auto_run = options["auto_run"].get("value", False)
        NodeManager.addNode(self)

    def execute(self, message=""):
        pass

    @staticmethod
    def get_info():
        return {
            "options": {
                "actions": list(process_options.keys()),
            }
        }
