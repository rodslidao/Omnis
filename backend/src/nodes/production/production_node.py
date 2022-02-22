from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from .production_obj import ProductionOBJ
from api import logger, exception

NODE_TYPE = "PRODUCTION"


class ProductionNode(BaseNode):
    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.model = options["model"]["value"]
        self.status = None
        self.production_obj = ProductionOBJ(**options)
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        target = message.targetName.lower()
        if target == "start":
            self.production_obj.start()
        elif target == "finish":
            _ = self.production_obj.finish(model=self.model, status=self.status)
            self.onSuccess(_)
        elif target == "status":
            self.status = message["payload"]
