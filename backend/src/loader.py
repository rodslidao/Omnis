from enum import Enum
from datetime import datetime
from bson import ObjectId
from api.models import NodeSheet

from .nodes.node_manager import NodeManager
from .nodes.node_registry import NodeRegistry
# from src.manager.mongo_manager import getDb
from api import logger, exception, dbo


class LoadingMode(Enum):
    STARTUP = "STARTUP"
    RUNNING = "RUNNING"


class NodeChangeType(Enum):
    # Create, Modify, Delete
    CREATE = "CREATE"
    MODIFY = "MODIFY"
    DELETE = "DELETE"


class NodeChange(object):
    # nodeId, nodeName, type, optionsOld, optionsNew, date
    def __init__(self, nodeId, nodeName, nodeType, optionsOld, optionsNew, date):
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.nodeType = nodeType
        self.optionsOld = optionsOld
        self.optionsNew = optionsNew
        self.date = datetime.now()


@exception(logger)
def getNodeByInterfaceId(nodeConfig, interfaceId):
    for n in nodeConfig.get("nodes"):
        for i in n.get("interfaces"):
            if i[1]["id"] == interfaceId:
                return n


@exception(logger)
def getInterfaceByInterfaceId(nodeConfig, interfaceId):
    for id, node in enumerate(nodeConfig.get("nodes")):
        # get first occurrence of interfaceId in node.get("interfaces")
        interface = None
        for i in node.get("interfaces"):
            if i[1]["id"] == interfaceId:
                interface = i
                break

        if interface:
            data = {"id": interface[1].get("id"), "name": interface[0]}
            return data
    return None


@exception(logger)
def extractOptionsFromNode(node):
    node_options = node.get("options")
    options = {}
    for option in node_options:
        options[option[0].lower()] = option[1]
    return options


@exception(logger)
def extractConnections(nodeConfig):
    return map(
        lambda node_con: {
            "from": {
                "id": getInterfaceByInterfaceId(nodeConfig, node_con.get("from")).get(
                    "id"
                ),
                "name": getInterfaceByInterfaceId(nodeConfig, node_con.get("from")).get(
                    "name"
                ),
                "nodeId": getNodeByInterfaceId(nodeConfig, node_con.get("from")).get(
                    "id"
                ),
            },
            "to": {
                "id": getInterfaceByInterfaceId(nodeConfig, node_con.get("to")).get(
                    "id"
                ),
                "name": getInterfaceByInterfaceId(nodeConfig, node_con.get("to")).get(
                    "name"
                ),
                "nodeId": getNodeByInterfaceId(nodeConfig, node_con.get("to")).get(
                    "id"
                ),
            },
        },
        nodeConfig.get("connections"),
    )


@exception(logger)
def cleanNodeManager(nodeConfigs):
    configNodeIds = map(
        lambda nodeConfig: None
        if not nodeConfig
        else map(lambda node: node.get("id"), nodeConfig),
        nodeConfigs,
    )
    configNodeIds = [
        item for sublist in configNodeIds for item in sublist
    ]  # flatten list

    runningNodeIds = map(lambda node: node.get("id"), NodeManager.getActiveNodes())
    # Getting deleted nodeIds by creating delta between the two arrays
    deleted = list(set(runningNodeIds) - set(configNodeIds))

    for nodeId in deleted:
        node = NodeManager.getNodeById(nodeId)
        saveNodeChange(
            NodeChange(
                node.get("id"),
                node.get("name"),
                NodeChangeType.DELETE,
                node.get("options")["settings"],
                {},
            )
        )
        NodeManager.resetNode(nodeId)

    return len(deleted)


@exception(logger)
def loadConfig(NodeSheet, mode=LoadingMode):
    numberOfNodesTotal = 0
    numberOfNodesChanged = 0
    numberOfNodesInit = 0
    nodesChanged = []

    nodeConfigs = [NodeSheet]  # list(dbo.get_collection("node-configs").find({}))

    for nodeConfig in nodeConfigs:
        connectionList = list(extractConnections(nodeConfig))
        # print("connectionList: {}".format(list(connectionList)))
        for node in nodeConfig.get("nodes"):
            newCls = NodeRegistry.getNodeClassByName(node.get("type"))

            options = extractOptionsFromNode(node)
            existingNode = NodeManager.getNodeById(node.get("id"))

            output_connections = list(
                filter(
                    lambda connection: connection.get("from").get("nodeId")
                    == node.get("id"),
                    connectionList,
                )
            )
            input_connections = list(
                filter(
                    lambda connection: connection.get("to").get("nodeId")
                    == node.get("id"),
                    connectionList,
                )
            )

            if existingNode is None:
                newCls(
                    node.get("name"),
                    node.get("id"),
                    options,
                    output_connections,
                    input_connections,
                )
                numberOfNodesInit += 1
                if mode == LoadingMode.RUNNING:
                    saveNodeChange(
                        NodeChange(
                            node.get("id"),
                            node.get("name"),
                            NodeChangeType.CREATE,
                            {},
                            options.get("settings"),
                        )
                    )
            else:
                logger.warning("Node {} EXIST!".format(node.get("name")))
                nodeSettingsChanged = existingNode.options.get(
                    "settings"
                ) != options.get("settings")
                outputChanged = existingNode.output_connections != output_connections
                nameChanged = existingNode.name != node.get("name")

                inputChanged = (
                    existingNode.input_connections is not None
                    and existingNode.input_connections != input_connections
                )

                if existingNode and (
                    nodeSettingsChanged or outputChanged or inputChanged or nameChanged
                ):
                    numberOfNodesChanged += 1
                    nodesChanged.append(node.get("name"))

                    if nodeSettingsChanged:
                        saveNodeChange(
                            NodeChange(
                                node.get("id"),
                                node.get("name"),
                                NodeChangeType.MODIFY,
                                existingNode.options.get("settings"),
                                options.get("settings"),
                            )
                        )

        numberOfNodesTotal += len(nodeConfig.get("nodes"))


@exception(logger)
def saveNodeChange(nodeChange):
    dbo.get_collection("node-history").insert_one(nodeChange)


@exception(logger)
def load(node_id=None):
    try:
        current_loaded_query = {"description": "current-config-loaded-id"}
        if node_id is not None:
            dbo.update_one(
                "last-values",
                current_loaded_query,
                {"$set": {"sheet-id": ObjectId(node_id)}},
            )
            sheet = NodeSheet().getNodeSheetById(node_id)["content"]
        else:
            sheet = NodeSheet().getNodeSheetById(
                dbo.find_one("last-values", current_loaded_query)["sheet-id"]
            )["content"]
        NodeManager.clear()
        loadConfig(sheet, LoadingMode)
        return True
    except Exception as e:
        logger.error("Error loading config: {}".format(e))
        return False

