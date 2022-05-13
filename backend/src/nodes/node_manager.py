from api import logger, exception
from api.decorators import for_all_methods

# from src.enums import loadConfig, LoadingMode
import threading


nodes = {}
auto_run_nodes = {}


@for_all_methods(exception(logger))
class NodeManager:
    def getNodeById(nodeId):
        return nodes.get(nodeId, None)

    def getNodesByType(nodeType):
        return list(filter(lambda node: node.get("type") == nodeType, nodes))

    def addNode(BaseNode):
        nodes[BaseNode._id] = BaseNode
        if BaseNode.auto_run:
            auto_run_nodes[BaseNode._id] = BaseNode._id

    def removeNode(nodeId):
        global nodes, auto_run_nodes
        del nodes[nodeId]
        if nodeId in auto_run_nodes:
            del auto_run_nodes[nodeId]

    def getActiveNodes():
        return nodes

    def start():
        ths = {}
        for node_id in auto_run_nodes.keys():
            node = NodeManager.getNodeById(node_id)
            # logger.info(f"[{node}] STARTED WITHOUT REQUEST.")
            ths[node._id] = threading.Thread(
                name=f"{node._id}_auto_run_start", target=node.AutoRun
            )
            ths[node._id].start()

        for _ in ths.values():
            _.join()

    def stop(context="external"):
        ths = {}
        global nodes, auto_run_nodes
        for node in list(nodes.values()):
            ths[node._id] = threading.Thread(
                name=f"{node._id}_auto_run_stop", target=node.stop
            )
            ths[node._id].start()

        for _ in ths.values():
            _.join

    def pause():
        for node in nodes.values():
            node.pause()

    def resume():
        for node in nodes.values():
            node.resume()

    def reset():
        global nodes, auto_run_nodes
        # NodeManager.stop()
        # nodes, auto_run_nodes = {}, []

    def clear():
        global nodes, auto_run_nodes
        nodes, auto_run_nodes = {}, {}

    def restart():
        NodeManager.stop()
        NodeManager.start()
