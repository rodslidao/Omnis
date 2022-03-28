from api import dbo
from bson.objectid import ObjectId
from json import load
from api import logger, exception

def defaultException(function):
    """Decorator to catch exceptions and return a payload with success=False and errors=exception message"""

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            payload = {"status": {"success": False, "errors": [str(error)]}}
            return payload

    return wrapper


class grok():
    @staticmethod
    def get_url():
        with open('.url_host', 'r') as f:
            return load(f)


class NodeSheet:
    @exception(logger)
    def createNodeSheet(self, _id, **kwargs):
        """Create a new NodeSheet object"""
        dbo.insert_one("NodeSheets", {'_id': ObjectId(_id), **kwargs})
        return self.getNodeSheetById(kwargs.get("_id"))

    @exception(logger)
    def getNodeSheetById(self, _id):
        """Get a NodeSheet by id"""
        self.NodeSheet = dbo.find_one("NodeSheets", {"_id": ObjectId(_id)})
        return self._format()

    @exception(logger)
    def updateNodeSheet(self, _id, **kwargs):
        # kwargs["_id"] = ObjectId(kwargs["_id"])
        """Update a NodeSheet by id"""
        print("updatating", kwargs)
        dbo.update_one("NodeSheets", {"_id": ObjectId(_id)}, {"$set": kwargs})
        return self.getNodeSheetById(_id)

    @exception(logger)
    def deleteNodeSheet(self, _id):
        # kwargs["_id"] = ObjectId(kwargs["_id"])
        """Delete a NodeSheet by id"""
        deleted_sheet = self.getNodeSheetById(_id)
        dbo.delete_one("NodeSheets", {"_id": ObjectId(_id)})
        return deleted_sheet

    @exception(logger)
    def getSketchList(self):
        return dbo.find_many("NodeSheets",  data={'content':0})
        
    @exception(logger)
    def _format(self):
        """Format the NodeSheet object"""
        return self.NodeSheet

