from .nodes.node_manager import NodeManager
from datetime import datetime
from time import sleep

RedisClient = None


class NodeExecutionCount(object):
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
        execInfoString = f"exec_info_{type}_{nodeId}"
        execInfoDate = f"exec_info_date_{nodeId}"
        execInfoTime = f"exec_info_time_{nodeId}"

        RedisClient.set(execInfoDate, datetime.now().strftime("%m.%d.%Y"))
        RedisClient.set(execInfoTime, datetime.now().strftime("%H:%M:%S"))
        RedisClient.incrby(execInfoString, incrWidth)

    @staticmethod
    def setCountType(nodeId, type, value):
        execInfoString = f"exec_info_{type}_{nodeId}"
        execInfoTime = f"exec_info_time_{nodeId}"
        execInfoDate = f"exec_info_date_{nodeId}"

        RedisClient.set(execInfoDate, datetime.now().strftime("%m.%d.%Y"))
        RedisClient.set(execInfoTime, datetime.now().strftime("%H:%M:%S"))
        RedisClient.set(execInfoString, value)

    @staticmethod
    def initialEmitAllCounts():
        activeNodes = NodeManager.getActiveNodes()
        for node in activeNodes:
            sleep(2)
            # ExecutionCounter.sendExecutionCountWithoutInfo(node.id)
            # print("Send here to front 'sendExecutionCountWithoutInfo(node.id)' ")

    @staticmethod
    def resetCount(nodeId):
        execInfoTrigger = f"exec_info_trigger_{nodeId}"
        execInfoSuccess = f"exec_info_success_{nodeId}"
        execInfoFailure = f"exec_info_failure_{nodeId}"
        byteInfoTrigger = f"exec_info_bytes_{nodeId}"
        execInfoDate = f"exec_info_date_{nodeId}"
        execInfoTime = f"exec_info_time_{nodeId}"

        RedisClient.set(execInfoTrigger, 0)
        RedisClient.set(execInfoSuccess, 0)
        RedisClient.set(execInfoFailure, 0)
        RedisClient.set(byteInfoTrigger, 0)
        RedisClient.set(execInfoDate, "-")
        RedisClient.set(execInfoTime, "-")

        payload = NodeExecutionCount("ExecutionCount", nodeId, 0, 0, 0, 0, "-", "-")
        return payload
        # emit("EXEC_COUNT", payload)

    @staticmethod
    def sendExecutionCountWithoutInfo(nodeId):
        execInfoTrigger = f"exec_info_trigger_{nodeId}"
        execInfoSuccess = f"exec_info_success_{nodeId}"
        execInfoFailure = f"exec_info_failure_{nodeId}"
        byteInfoTrigger = f"exec_info_bytes_{nodeId}"
        execInfoDate = f"exec_info_date_{nodeId}"
        execInfoTime = f"exec_info_time_{nodeId}"

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
        return payload
