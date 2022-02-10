if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Message:
    def __init__(
        self,
        sourceId,
        targetId,
        sourceName,
        targetName,
        sourceNodeId,
        targetNodeId,
        payload,
        additional=None,
    ):
        self.sourceId = sourceId
        self.targetId = targetId
        self.sourceName = sourceName
        self.targetName = targetName
        self.sourceNodeId = sourceNodeId
        self.targetNodeId = targetNodeId
        self.payload = payload
        self.additional = additional
    def __str__(self) -> str:
        return f"[{self.sourceName}] -> [{self.targetNodeId}|{self.targetName}] : {self.payload}"