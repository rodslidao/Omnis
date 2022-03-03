from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "DRAWDIMENSIONALDATA"

draw_options = {
    'box':'drawBox',
    'corners':'drawCorners',
    'circle':'drawCircle',
    'center':'drawCenter',
    'vertices':'drawVertices',
    'sizes':'drawRectSize',
    'angle':'drawAngles'
}

class DrawdimensionaldataNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.proplist = options.drawable_properties
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        for n in self.proplist:
            if n in draw_options:
                self.onSuccess(getattr(self, draw_options[n])(message))
            else:
                self.onFailure("No such drawable property: {}".format(n))

    @staticmethod
    @exception(logger)
    def get_info():
        return {
            "options": {
                "drawable_properties":list(draw_options.keys()),
            }
        }
