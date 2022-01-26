from inspect import Attribute
from .models import NodeSheet, defaultException, ProcessManager
from ariadne import MutationType

mutation = MutationType()


@defaultException
@mutation.field("createNodeSheet")
def createNodeSheet_resolver(obj, info, **kwargs):
    """Create a new NodeSheet object and return it like a payload"""
    returns = NodeSheet().createNodeSheet(**kwargs.get("input", {}))
    return {"success": True, "data": returns}


@defaultException
@mutation.field("updateNodeSheet")
def updateNodeSheet_resolver(obj, info, **kwargs):
    """Update a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().updateNodeSheet(kwargs.get("id"), **kwargs.get("input", {}))
    return {"success": True, "data": returns}


@defaultException
@mutation.field("deleteNodeSheet")
def deleteNodeSheet_resolver(obj, info, id):
    """Delete a NodeSheet by id and return it like a payload"""
    returns = NodeSheet().deleteNodeSheet(id)
    return {"success": True, "data": returns}

@defaultException
@mutation.field("startProcess")
def startProcess_resolver(obj, info):
    """Start a process by id and return it like a payload"""
    # try:
    ProcessManager().startProcess()
    returns = ProcessManager().dict()
    print(returns)
    # except AttributeError:
    #     raise AttributeError("Id in last-values colletions does not match with any process")
    return {"success": True, "data": returns}