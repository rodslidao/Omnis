if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

nodes = []


class NodeManager:
    def getNodeById(nodeId):
        for node in nodes:
            if node.id == nodeId:
                return node
        return None

    def getNodesByType(nodeType):
        return list(filter(lambda node: node.get("type") == nodeType, nodes))

    def addNode(BaseNode):
        nodes.append(BaseNode)

    def getActiveNodes():
        return nodes

    def reset():
        global nodes
        if len(nodes) > 0:
            for node in nodes:
                node.stop()
            nodes = []

    def resetNode(nodeId):
        global nodes
        node = NodeManager.getNodeById(nodeId)
        if node:
            node.stop()
            nodes = list(filter(lambda node: node.get("id") != nodeId, nodes))
