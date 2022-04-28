from api import dbo
from bson.objectid import ObjectId
from json import load
from api import logger, exception, for_all_methods


def defaultException(function):
    """Decorator to catch exceptions and return a payload with success=False and errors=exception message"""

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
        if target:
            self.create_node_sheet(_id, **kwargs)
        else:
            self.update_node_sheet(_id, **kwargs)
        return self.getNodeSheetById(kwargs.get("_id"))

    def create_node_sheet(self, _id, **kwargs):
        """Create a new NodeSheet object"""
        logger.info(f"Creating new NodeSheet with id: {_id}")
        dbo.insert_one("node-sheets", {"_id": ObjectId(_id), **kwargs})
        return self.getNodeSheetById(kwargs.get("_id"))

    def getNodeSheetById(self, _id):
        """Get a NodeSheet by id"""
        logger.debug(f"Getting NodeSheet by id: {_id}")
        self.NodeSheet = dbo.find_one("node-sheets", {"_id": ObjectId(_id)})
        return self._format()

    def update_node_sheet(self, _id, **kwargs):
        """Update a NodeSheet by id"""
        logger.info(f"Updating NodeSheet [{_id}]")
        dbo.update_one("node-sheets", {"_id": ObjectId(_id)}, {"$set": kwargs})
        return self.getNodeSheetById(_id)

    def delete_node_sheet(self, _id):
        """Delete a NodeSheet by id"""
        logger.info(f"Deleting NodeSheet [{}_id]")
        deleted_sheet = self.getNodeSheetById(_id)
        dbo.delete_one("node-sheets", {"_id": ObjectId(_id)})
        return deleted_sheet

    def get_sketch_list(self):
        return dbo.find_many("NodeSheets", data={"content": 0})

    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet
