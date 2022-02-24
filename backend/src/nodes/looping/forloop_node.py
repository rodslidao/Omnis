import imp
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode
from api import logger, exception

NODE_TYPE = "FORLOOP"


class ForloopNode(BaseNode):
    """
    Interfaces ->
        :Lista: - Recebe uma lista como payload e salva no iterator. \n
        :Trigger: - Recebe um trigger como payload e executa o next(iterator). \n
    \n
    Signals ->
        :item: - Envia o item atual do iterator. \n
        :Fim: - Envia um sinal de fim de execução, reseta o iterator. \n
    """

    @exception(logger)
    def __init__(self, name, type, id, options, outputConnections) -> None:
        super().__init__(name, type, id, options, outputConnections)
        self.iterator = []
        self.backup = []
        self.auto_run = options["auto_run"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        target = message["targetName"]
        if target == "Lista":
            self.iterator = enumerate(message["payload"])
            self.backup = self.iterator.copy()
        elif target == "Trigger":
            try:
                self._id, self.item = next(self.iterator)
                self.on("item", self.item)
            except StopIteration:
                self.on("Fim")
                self.iterator = self.backup.copy()
            except Exception as e:
                self.onFailure(e)
