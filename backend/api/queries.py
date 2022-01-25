from .models import NodeSheet, defaultException
from ariadne import QueryType

query = QueryType()

payload = {"success": False, "errors": None}


@defaultException
@query.field("getNodeSheet")
def getNodeSheet_resolver(obj, info, **kwargs):
    """Get a NodeSheet by id and return it like a payload"""
    result = NodeSheet().getNodeSheetById(id=kwargs.get("id"))
    payload["success"] = True
    payload["data"] = result
    return payload
