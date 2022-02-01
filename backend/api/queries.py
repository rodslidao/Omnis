from .models import *
from ariadne import QueryType
from .store import queues, alerts
query = QueryType()

payload = {"success": False, "errors": None}

# Alert("info", "Info - 1", "This is an info alert", "You can solve this alert by doing something")
@defaultException
@query.field("getNodeSheet")
def getNodeSheet_resolver(obj, info, **kwargs):
    """Get a NodeSheet by id and return it like a payload"""
    result = NodeSheet().getNodeSheetById(id=kwargs.get("id"))
    payload["success"] = True
    payload["data"] = result
    return payload

@defaultException
@query.field("getProcess")
def getProcess_resolver(obj, info):
    return {"status":{"success": True },"data": process.dict()}
