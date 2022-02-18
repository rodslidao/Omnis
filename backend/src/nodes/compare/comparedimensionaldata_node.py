from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from src.nodes.compare.compare_obj import data_comparatives

NODE_TYPE = "COMPARATIVE_DIMENSIONAL_DATA"

class CompareNode(BaseNode):
    """
    Node to execute logical operations between values.
    """

    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.operation = options["operation"]
        self.value2 = options["value2"]
        self.value3 = options["value3"]
        NodeManager.addNode(self)

    def execute(self, message=""):
        target = message["targetName"].lower()
        getattr(self, target)(message)
        pass

    def dimensional_obj(self, message):
        self.dimensional_obj = message['payload']

    def value2(self, message):
        self.value2 = message['payload']

    def value3(self, message):
        self.value3 = message['payload']

    def trigger(self, message):
        try:
            self.onSuccess(data_comparatives[self.operation](self.dimensional_obj, self.value2, self.value3))
        except Exception as e:
            self.onFailure(f"{self._id} cant execute.", pulse=True, errorMessage=str(e))

# ! Fazer o node de imagem gerar a imagem apartir de qualquer path.
# ! Usar o node_tester pra testar uma logica simples de identificação.