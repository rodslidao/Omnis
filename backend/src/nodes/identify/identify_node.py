if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from nodes.base_node import BaseNode

from identify_functions import identifyObjects

NODE_TYPE = "IDENTIFY"


class IdentifyNode(BaseNode):
    def __init__(self, name, id, options, outputConnections, inputConnections) -> None:
        super().__init__(name, type, id, options, outputConnections)
        self.inputConnections = inputConnections
        self.filters = options["filters"]
        self.propertie = options["propertie"]
        NodeManager.addNode(self)

    def execute(self, message):
        try:
            object_data_list = identifyObjects(message, **self.filters)
            property_data_list = []
            for object_data in object_data_list:
                if object_data.get(self.propertie) is not None:
                    property_data_list.append(object_data)
            self.on("onSuccess", property_data_list)
            self.onSignal()
        except Exception as e:
            self.onFailure(e, pulse=True)
