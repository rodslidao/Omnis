from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.draw.draw_obj import DrawOBJ
from api import logger, exception

NODE_TYPE = "DRAW"

draw_options = {
    'box':'drawBox',
    'corners':'drawCorners',
    'circle':'drawCircle',
    'center':'drawCenter',
    'vertices':'drawVertices',
    'sizes':'drawRectSize',
    'angle':'drawAngles'
}

class DrawNode(BaseNode):
    """
    insert_node_description_here
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.proplist = options["drawable_properties"]
        self.auto_run = options["auto_run"]["value"]
        self.image = None
        self.obj = None
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message=""):
        target = message.targetName.lower()

        if target == 'dimensional_data':
            self.obj = message.payload
        elif target == 'image':
            self.image = message.payload.copy()

        if self.obj is not None and self.image is not None:
            if isinstance(message.payload, list):
                self.onFailure("This node supports only one object at a time, please 'split' the list of objects before using this node.")
            else:
                if self.image is None:
                    self.onFailure("No image has been loaded yet, please load an image before using this node.")
                    return False
                self.draw = DrawOBJ(**self.obj(), image=self.image)
                for n in self.proplist:
                    if n in draw_options:
                        getattr(self.draw, draw_options[n])()
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

    @exception(logger)
    def get_frame(self):
        return self.image