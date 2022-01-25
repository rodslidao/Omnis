if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nodes.node_manager import NodeManager
from src.Redis import RedisClient
from datetime import datetime
from flask_socketio import emit


class NodeExecutionCount(object):
    # type, nodeId, triggerCount, succesCount, failureCount, bytesCount, time, date
    def __init__(
        self,
        type,
        nodeId,
        triggerCount,
        successCount,
        failureCount,
        bytesCount,
        time,
        date,
    ):
        self.type = type
        self.nodeId = nodeId
        self.triggerCount = triggerCount
        self.successCount = successCount
        self.failureCount = failureCount
        self.bytesCount = bytesCount
        self.time = time
        self.date = date


class ExecutionCounter(object):
    @staticmethod
    def incrCountType(nodeId, type, incrWidth=1):
        execInfoString = f"exex_info_{type}_{nodeId}"
        execInfoDate = f"exex_info_date_{nodeId}"
        execInfoTime = f"exex_info_time_{nodeId}"

        RedisClient.set(execInfoDate, datetime.now().strftime("%m.%d.%Y"))
        RedisClient.set(execInfoTime, datetime.now().strftime("%H:%M:%S"))

        RedisClient.incrby(execInfoString, incrWidth)
        ExecutionCounter.sendExecutionCountWithoutInfo(nodeId)

    @staticmethod
    def setCountType(nodeId, type, value):
        execInfoString = f"exex_info_{type}_{nodeId}"
        execInfoTime = f"exex_info_time_{nodeId}"
        execInfoDate = f"exex_info_date_{nodeId}"

        RedisClient.set(execInfoDate, datetime.now().strftime("%m.%d.%Y"))
        RedisClient.set(execInfoTime, datetime.now().strftime("%H:%M:%S"))
        RedisClient.set(execInfoString, value)

        ExecutionCounter.sendExecutionCountWithoutInfo(nodeId)

    @staticmethod
    def initialEmitAllCounts():
        activeNodes = NodeManager.getActiveNodes()
        for node in activeNodes:
            ExecutionCounter.sendExecutionCountWithoutInfo(node.id)
            print("Send here to front 'sendExecutionCountWithoutInfo(node.id)' ")

    @staticmethod
    def resetCount(nodeId):
        execInfoTrigger = f"exex_info_trigger_{nodeId}"
        execInfoSuccess = f"exex_info_success_{nodeId}"
        execInfoFailure = f"exex_info_failure_{nodeId}"
        byteInfoTrigger = f"exex_info_bytes_{nodeId}"
        execInfoDate = f"exex_info_date_{nodeId}"
        execInfoTime = f"exex_info_time_{nodeId}"

        RedisClient.set(execInfoTrigger, 0)
        RedisClient.set(execInfoSuccess, 0)
        RedisClient.set(execInfoFailure, 0)
        RedisClient.set(byteInfoTrigger, 0)
        RedisClient.set(execInfoDate, "-")
        RedisClient.set(execInfoTime, "-")

        payload = NodeExecutionCount("ExecutionCount", nodeId, 0, 0, 0, 0, "-", "-")
        emit("EXEC_COUNT", payload)

    @staticmethod
    def sendExecutionCountWithoutInfo(nodeId):
        execInfoTrigger = f"exex_info_trigger_{nodeId}"
        execInfoSuccess = f"exex_info_success_{nodeId}"
        execInfoFailure = f"exex_info_failure_{nodeId}"
        byteInfoTrigger = f"exex_info_bytes_{nodeId}"
        execInfoDate = f"exex_info_date_{nodeId}"
        execInfoTime = f"exex_info_time_{nodeId}"

        triggerCount = RedisClient.get(execInfoTrigger)
        successCount = RedisClient.get(execInfoSuccess)
        failureCount = RedisClient.get(execInfoFailure)
        bytesCount = RedisClient.get(byteInfoTrigger)
        date = RedisClient.get(execInfoDate)
        time = RedisClient.get(execInfoTime)

        payload = NodeExecutionCount(
            type="ExecutionCount",
            nodeId=nodeId,
            triggerCount=triggerCount,
            successCount=successCount,
            failureCount=failureCount,
            bytesCount=bytesCount,
            time=time,
            date=date,
        )

        emit("EXEC_COUNT", payload)
