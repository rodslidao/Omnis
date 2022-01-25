from pymongo import MongoClient
import os

# get environment variable "NODE_ENV"
environment = os.environ.get("NODE_ENV", "DEV")

url = "mongodb://192.168.1.41:27017/"
if environment == "DEV":
    url = "mongodb://localhost:27017/"
print("url", url)
_db = None
requiredCollections = ["node-configs", "node-templates", "last-values", "node-history"]


def connectToServer(callback):
    global _db
    if _db is None:
        client = MongoClient(url)
        _db = client.get_database("Omnis")

    for collectionName in requiredCollections:
        if collectionName not in _db.list_collection_names():
            _db.create_collection(collectionName)
            print("Collection {} created".format(collectionName))
    callback()


def getDb():
    return _db


def storeLastValue(nodeId, payload):
    query = {"_id": nodeId}

    newvalues = {"$set": {"last": payload}}
    options = {"upsert": True}
    _db.get_collection("last-values").update_one(query, newvalues, options)


def getLastValue(nodeId):
    query = {"_id": nodeId}

    try:
        return _db.get_collection("last-values").find_one(query)
    except Exception as e:
        print(e)
        return None


def deleteLastValue(nodeId):
    query = {"_id": nodeId}
    _db.get_collection("last-values").delete_one(query)
