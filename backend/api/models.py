from api import db
from bson.objectid import ObjectId


def defaultException(function):
    """Decorator to catch exceptions and return a payload with success=False and errors=exception message"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            payload = {"success": False, "errors": [str(error)]}
            return payload

    return wrapper


class NodeSheet:
    def createNodeSheet(self, **kwargs):
        """Create a new NodeSheet object"""
        _id = ObjectId()
        db.NodeSheets.insert_one({"_id": _id, **kwargs})
        return self.getNodeSheetById(_id)

    def getNodeSheetById(self, id):
        """Get a NodeSheet by id"""
        self.NodeSheet = db.NodeSheets.find_one({"_id": ObjectId(id)})
        return self._format()

    def updateNodeSheet(self, id, **kwargs):
        """Update a NodeSheet by id"""
        db.NodeSheets.update_one({"_id": ObjectId(id)}, {"$set": kwargs})
        return self.getNodeSheetById(id)

    def deleteNodeSheet(self, id):
        """Delete a NodeSheet by id"""
        deleted_sheet = self.getNodeSheetById(id)
        db.NodeSheets.delete_one({"_id": ObjectId(id)})
        return deleted_sheet

    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet
