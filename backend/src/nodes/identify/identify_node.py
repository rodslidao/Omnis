from tkinter import image_names
from src.nodes.node_manager import NodeManager
from src.nodes.base_node import BaseNode

from .identify_functions import identifyObjects
from api import logger, exception

NODE_TYPE = "IDENTIFY"


class IdentifyNode(BaseNode):
    """
    Find a list of countours in an image that match a giver filters.

    Signals ->
        "onSuccess" -> returns a list of dimensional countour data.
    """

    @exception(logger)
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, NODE_TYPE, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.filters = options["filters"]
        self.propertie = options["propertie"]
        self.auto_run = options["auto_run"]["value"]
        NodeManager.addNode(self)

    @exception(logger)
    def execute(self, message):
        print(f"{self.name} - triggered")
        object_data_list = identifyObjects(message.payload, **self.filters)
        for object_data in object_data_list:
            for prop_key in self.propertie:
                if object_data.get(prop_key) is not None:
                    self.on(prop_key, object_data.get(prop_key))

            self.on("object", object_data)
            self.onSuccess(object_data())

        #property_data_list.add(object_data)
        #self.on("onSuccess", list(property_data_list))
        #self.onSignal()
        # except Exception as e:
        #     self.onFailure(e, pulse=True)


"""

Pegar imagem
Filtrar imagem
Identificar objetos

Manipular informações

Informações de validação
 - Dimensões e etc

Informações de manipulação fisica
    - Coordenadas







"""