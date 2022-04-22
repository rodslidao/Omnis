from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.process.process_obj import process
from api import logger, exception
NODE_TYPE = "PROCESS"

process_options ={
    'stop': process.stopProcess,
    'pause': process.pauseProcess,
    'resume': process.resumeProcess,
    'reset': NodeManager.restart
}

class ProcessNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.function = process_options.get(options["action"].get("value", 'stop'), 'stop')
        self.auto_run = options["auto_run"].get("value", False)
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        pass

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "actions": list(process_options.keys()),
            }
        }
