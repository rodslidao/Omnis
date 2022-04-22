from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception, for_all_methods

NODE_TYPE = "SWITCH"


@for_all_methods(exception(logger))
class SwitchNode(BaseNode):
    """
    insert_node_description_here
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.auto_run = options["auto_run"]["value"]
        self.varaibles = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.inputs = {}
        setattr(self, "True", options["true"]["value"])
        setattr(self, "False", options["false"]["value"])
        self.expression = options["expression"]["value"]
        NodeManager.addNode(self)
        

    def execute(self, message=""):
        target = message.targetName
        if target in self.varaibles:
            self.inputs[str(target)] = message.payload
        elif target in ['True','False']:
            setattr(self, target, self.inputs.get(message.payload, message.payload))
        elif target == "expression":
            result = eval(self.expression, self.inputs.copy())
            opt_result = getattr(self, str(result))
            self.on(str(result), opt_result if opt_result is not None else result)
            return opt_result if opt_result is not None else result

    @staticmethod
    def get_info():
        return {
            "options": {
                "option_name": "option_accepted_values",
            }
        }
