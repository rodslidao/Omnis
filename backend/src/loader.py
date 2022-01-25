if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from enum import Enum
from datetime import datetime

from nodes.node_manager import NodeManager
from nodes.node_registry import NodeRegistry
from src.manager.mongo_manager import getDb
from flask_socketio import emit


class LodingMode(Enum):
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


def getNodeByInterfaceId(nodeConfig, interfaceId):
    a = next(
        n
        for n in nodeConfig.get("nodes")
        if any([i[1]["id"] == interfaceId for i in n.get("interfaces")])
    )
    return a


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


def extractOptionsFromNode(node):
    node_options = node.get("options")
    options = {}
    for option in node_options:
        options[option[0].lower()] = option[1]
    return options


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


def loadConfig(dbo, mode=LodingMode):
    print("loading config")
    numberOfNodesTotal = 0
    numberOfNodesChanged = 0
    numberOfNodesInit = 0
    nodesChanged = []

    nodeConfigs = list(dbo.get_collection("node-configs").find({}))

    for nodeConfig in nodeConfigs:
        connectionList = extractConnections(nodeConfig)
        for node in nodeConfig.get("nodes"):

            try:
                newCls = NodeRegistry.getNodeClassByName(node.get("type"))
            except Exception:
                print("Node type '{}' not found".format(node.get("type")))

            options = extractOptionsFromNode(node)
            existingNode = NodeManager.getNodeById(node.get("id"))

            # outputConnections is a list of connections that has same node.id in value from.id
            outputConnections = list(
                filter(
                    lambda connection: connection.get("from").get("nodeId")
                    == node.get("id"),
                    connectionList,
                )
            )
            inputConnections = list(
                filter(
                    lambda connection: connection.get("to").get("nodeId")
                    == node.get("id"),
                    connectionList,
                )
            )

            if not existingNode:
                newCls(
                    node.get("name"),
                    node.get("id"),
                    options,
                    outputConnections,
                    inputConnections,
                )
                numberOfNodesInit += 1

                if mode == LodingMode.RUNNING:
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
                nodeSettingsChanged = existingNode.get("options").get(
                    "settings"
                ) != options.get("settings")
                outputChanged = (
                    existingNode.get("outputConnections") != outputConnections
                )
                nameChanged = existingNode.get("name") != node.get("name")

                # Input only relevant for existing nodes with inputConnections !== undefined
                inputChanged = (
                    existingNode.get("inputConnections") is not None
                    and existingNode.get("inputConnections") != inputConnections
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
                                existingNode.get("options").get("settings"),
                                options.get("settings"),
                            )
                        )

        numberOfNodesTotal += len(nodeConfig.get("nodes"))


def saveNodeChange(nodeChange):
    print("saving node change")
    dbo = getDb()
    # try insert nodeChange in node-history collection of dbo, if can't insert, by any reason, inform
    try:
        dbo.get_collection("node-history").insert_one(nodeChange)
        emit("node-change", nodeChange)
    except Exception as e:
        print("Can't save node change: {}".format(e))
