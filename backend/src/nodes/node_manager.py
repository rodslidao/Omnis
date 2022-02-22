from api import logger, exception

nodes = []


class NodeManager:
    @exception(logger)
    def getNodeById(nodeId):
        for node in nodes:
            if node._id == nodeId:
                return node
        return None

    @exception(logger)
    def getNodesByType(nodeType):
        return list(filter(lambda node: node.get("type") == nodeType, nodes))

    @exception(logger)
    def addNode(BaseNode):
        nodes.append(BaseNode)

    @exception(logger)
    def getActiveNodes():
        return nodes

    @exception(logger)
    def reset():
        global nodes
        for node in nodes:
            node.stop()
        nodes = []

    @exception(logger)
    def stop():
        NodeManager.reset()

    @exception(logger)
    def pause():
        for node in nodes:
            node.pause()

    @exception(logger)
    def resume():
        for node in nodes:
            node.resume()

    @exception(logger)
    def resetNode(nodeId):
        global nodes
        node = NodeManager.getNodeById(nodeId)
        if node:
            node.stop()
            nodes = list(filter(lambda node: node.get("id") != nodeId, nodes))
