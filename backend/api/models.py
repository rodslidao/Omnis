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
