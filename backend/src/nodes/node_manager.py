from api import logger, exception
#from src.enums import loadConfig, LoadingMode
import threading


nodes = {}
auto_run_nodes = {}

class NodeManager:

    @exception(logger)
    def getNodeById(nodeId):
        return nodes.get(nodeId, None)

    @exception(logger)
    def getNodesByType(nodeType):
        return list(filter(lambda node: node.get("type") == nodeType, nodes))

    @exception(logger)
    def addNode(BaseNode):
        nodes[BaseNode._id] = BaseNode
        if BaseNode.auto_run:
            auto_run_nodes[BaseNode._id] = BaseNode._id

    @exception(logger)
    def getActiveNodes():
        return nodes

    @exception(logger)
    def start():
        ths = {}
        for node_id in auto_run_nodes.keys():
            node = NodeManager.getNodeById(node_id)
            logger.info(f"~[[{node}]]~ start automatically.")
            ths[node._id] = threading.Thread(name=f"{node._id}_auto_run_start",target=node.AutoRun)
            ths[node._id].start()
        
        for _ in ths.values(): _.join()

    @exception(logger)
    def stop(context="external"):
        ths = {}
        global nodes, auto_run_nodes
        for node in list(nodes.values()):
            ths[node._id]=threading.Thread(name=f"{node._id}_auto_run_stop",target=node.stop)
            ths[node._id].start()
        
        for _ in ths.values(): _.join

    @exception(logger)
    def pause():
        for node in nodes.values():
            node.pause()

    @exception(logger)
    def resume():
        for node in nodes.values():
            node.resume()

    @exception(logger)
    def reset():
        global nodes, auto_run_nodes
        #NodeManager.stop()
        #nodes, auto_run_nodes = {}, []   

    def restart():
        NodeManager.stop()
        NodeManager.start()
