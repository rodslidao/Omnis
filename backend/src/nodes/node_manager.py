nodes = []

class NodeManager:
    def getNodeById(nodeId):
        for node in nodes:
            if node._id == nodeId:
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
        for node in nodes:
            node.stop()
        nodes = []
    
    def stop():
        NodeManager.reset()

    def pause():
        for node in nodes:
            node.pause()
    
    def resume():
        for node in nodes:
            node.resume()

    def resetNode(nodeId):
        global nodes
        node = NodeManager.getNodeById(nodeId)
        if node:
            node.stop()
            nodes = list(filter(lambda node: node.get("id") != nodeId, nodes))
