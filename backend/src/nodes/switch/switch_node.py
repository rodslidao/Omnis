from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception
from api.decorators import for_all_methods

NODE_TYPE = "IfNode"


@for_all_methods(exception(logger))
class SwitchNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, output_connections, input_connections):
        super().__init__(name, NODE_TYPE, id, options, output_connections)
        self.input_connections = input_connections
        self.variables = list(map(lambda x: x["name"], options["inputlist"]))#[chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.inputs = {}
        setattr(self, "True", options["onsuccess"])
        setattr(self, "False", options["onfailure"])
        self.expression = options["expression"]
        self.auto_run = options.get(["auto_run"], False)
        NodeManager.addNode(self)

    def execute(self, message=""):
        target = message.targetName
        if target in self.variables:
            self.inputs[str(target)] = message.payload
            logger.info("{} received {}".format(self.name, message.payload[1].item is not None))
        elif target in ["True", "False"]:
            setattr(self, target, self.inputs.get(message.payload, message.payload))
        # elif target == "expression":
        result = eval(self.expression, self.inputs.copy())
        # if result != False:
        #     logger.warning(list(map(type, self.inputs['A'][1].item)))
        # opt_result = getattr(self, str(result))
        self.on("Sucesso" if result else "Falha", True)

    @staticmethod
    def get_info(**kwargs):
        return {
            "options": {
                "option_name": "option_accepted_values",
            }
        }