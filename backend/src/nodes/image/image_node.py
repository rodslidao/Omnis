from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.image.image_obj import Image

NODE_TYPE = "IMAGE"

class ImageNode(BaseNode):
    """
    Node to manipulate an image with mos common operations.
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.image = Image(options.image.get("path", './src/imgs/no_image.jpg'))
        self.properties = options.image.get("properties", [])
        NodeManager.addNode(self)
        
    def execute(self, message=""):
        target = message["targetName"].lower()
        
        try:
            getattr(self, target)(message)
        except:
            pass

        for prop in self.properties:
            self.on(prop, getattr(self.image, prop))

    def get_frame(self):
        return self.image()
        
    def update_image(self, message):
        try:
            self.image = Image(image=message['payload'])
            self.onSuccess(self.image)
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))
