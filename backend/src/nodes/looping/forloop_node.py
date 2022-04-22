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
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.iterator = enumerate(options["iterator"]["value"])
        self.backup = options["iterator"]["value"][:]
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        target = message.targetName
        if target == "iterator":
            self.iterator = enumerate(message.payload)
            self.backup = self.iterator
        elif target == "next" or "auto_run":

            # Is important itereate the iterator before or back up it, before send signal to avoid infinite loop or empty list.
            if not self.stop_event.is_set():
                try:
                    self.item_id, self.item = next(self.iterator)
                    self.on("item", self.item)
                except StopIteration:
                    self.iterator = enumerate(self.backup[:])
                    self.on("end", "")
        else:
            #? This is necessary?
            raise "Target not found"

    @exception(logger)
    def reset(self):
        super().reset()
        self.iterator = enumerate(self.backup[:])