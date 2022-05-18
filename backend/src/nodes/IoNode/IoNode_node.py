from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception
from api.decorators import for_all_methods
from api import dbo
from src.manager.serial_manager import SerialManager

NODE_TYPE = "IoNode"


@for_all_methods(exception(logger))
class IoNodeNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.config = options["port"]
        self.board = SerialManager.get_by_id(self.config["board"])
        self.command = self.config["command"].replace("<pin>", str(self.config["port"])).replace("<pwm>", str(255 if self.config["pwm"] else 0))
        self.auto_run = options.get(["auto_run"], False)
        NodeManager.addNode(self)


    def execute(self, message=""):
        target = message.targetName.lower()
        if target == "gatilho":
            self.board.send(self.command)
            self.on("Saida", True)


    @staticmethod
    def get_info(**kwargs):
        return {
            "options": list(dbo.find_many("pins", {"board": kwargs.get("board")}, {"_id": 0}))
        }


# LC - Quad, SU, SIM. Mantem.
# Melhoraram os cortes e pinturas.

# SC
# LC - Quad, DU, SIM.