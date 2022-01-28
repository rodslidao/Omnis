from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from os import environ
from src.manager import logger
# get environment variable "NODE_ENV"
#environment = os.environ.get("NODE_ENV", "DEV")


db_port = environ.get("DB_PORT", "27017")
db_ip = environ.get("SERVER_IP", "192.168.1.30")
url = f"mongodb://{db_ip}:{db_port}/"

_db = None
requiredCollections = ["node-configs", "node-templates", "last-values", "node-history"]


def connectToMongo(database="Teste"):
    global _db
    if _db is None:
        try:
            logger.debug(f"Connecting to MongoDB using url: {url}")
            client = MongoClient(url)
            client.admin.command("ismaster")
        except ConnectionFailure:
            logger.critical(f"Could not connect to MongoDB using url: {url}")
            raise
        else:
            logger.info("Connected to MongoDB")

            
        _db = client.get_database(database)

    for collectionName in requiredCollections:
        if collectionName not in _db.list_collection_names():
            _db.create_collection(collectionName)
            logger.debug(f"Created collection {collectionName}")


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
