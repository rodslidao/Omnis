from datetime import datetime
from api import dbo
from bson.objectid import ObjectId
from json import load
from api import logger, exception
from api.decorators import for_all_methods


def defaultException(function):
    """
    Decorator to catch exceptions,
    and return a payload with success=False and errors=exception message
    """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            payload = {"status": {"success": False, "errors": [str(error)]}}
            return payload
    return wrapper


class grok:
    @staticmethod
    def get_url():
        with open(".url_host", "r") as f:
            return load(f)


@for_all_methods(exception(logger))
class NodeSheet:
    def save_node_sheet(self, _id, **kwargs):
        """Save a NodeSheet object"""
        target = dbo.find_one("node-sheets", {"_id": ObjectId(_id)}) is None
        kwargs_whiout_empty = {k: v for k, v in kwargs.items() if v}
        if kwargs_whiout_empty.get("content"):
            kwargs_whiout_empty["node_qtd"] = len(kwargs_whiout_empty["content"]["nodes"])
        if target:
            self.create_node_sheet(_id, **kwargs_whiout_empty)
        else:
            self.update_node_sheet(_id, **kwargs_whiout_empty)
        return self.get_sketch_list()

    def duplicate_node_sheet(self, _id):
        """Duplicate a NodeSheet by id"""
        logger.info(f"Duplicating NodeSheet [{_id}]")
        self.NodeSheet = dbo.find_one("node-sheets", {"_id": ObjectId(_id)})
        self.NodeSheet["_id"] = ObjectId()
        self.NodeSheet["date"] = datetime.utcnow().timestamp()
        self.NodeSheet["node_qtd"] = len(self.NodeSheet["content"]["nodes"])
        self.NodeSheet["label"] = self.NodeSheet["label"]+' - Cópia'
        return dbo.insert_one("node-sheets", self.NodeSheet) is not None
    
    def create_node_sheet(self, _id, **kwargs):
        """Create a new NodeSheet object"""
        logger.info(f"Creating new NodeSheet with id: {_id}")
        return dbo.insert_one("node-sheets", {"_id": ObjectId(_id), **kwargs}) is not None

    def getNodeSheetById(self, _id):
        """Get a NodeSheet by id"""
        logger.debug(f"Getting NodeSheet by id: {_id}")
        self.NodeSheet = dbo.find_one("node-sheets", {"_id": ObjectId(_id)})
        return self._format()

    def update_node_sheet(self, _id, **kwargs):
        """Update a NodeSheet by id"""
        logger.info(f"Updating NodeSheet [{_id}]")
        return dbo.update_one("node-sheets", {"_id": ObjectId(_id)}, {"$set": kwargs}) is not None

    def delete_node_sheet(self, _id):
        """Delete a NodeSheet by id"""
        logger.info(f"Deleting NodeSheet [{_id}]")
        return dbo.delete_one("node-sheets", {"_id": ObjectId(_id)}) is not None

    def get_sketch_list(self):
        """Get a list of all sketches"""
        return dbo.find_many("node-sheets", data={"content": 0})

    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet
