from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from os import environ, getenv
from api import logger, exception
from pandas import DataFrame

from numpy import integer, floating, ndarray
from json import loads, dumps, JSONEncoder
from bson.errors import InvalidDocument
# get environment variable "NODE_ENV"
# environment = os.environ.get("NODE_ENV", "DEV")
from dotenv import load_dotenv
from os import popen

load_dotenv()

db_port = environ.get("DB_PORT", "27017")
db_ip = getenv("DB_HOST")

url = (
    f"mongodb://{db_ip}:{db_port}/"
    if environ.get("ENV_MODE") != "cloud"
    else f"mongodb+srv://{getenv('DB_USER')}:{getenv('DB_PASS')}@cluster0.diykb.mongodb.net/test?retryWrites=true&w=majority"
)

_db = None
requiredCollections = ["node-configs", "node-templates", "last-values", "node-history"]


@exception(logger)
def getDb():
    global _db
    if _db is None:
        _db = MongoOBJ(environ.get("DB_NAME"), url)
    return _db


@exception(logger)
def connectToMongo(database="Teste"):
    getDb()
    for collectionName in requiredCollections:
        if collectionName not in _db.list_collection_names():
            _db.create_collection(collectionName)
            logger.debug(f"Created collection {collectionName}")


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, integer):
            return int(obj)
        elif isinstance(obj, floating):
            return float(obj)
        elif isinstance(obj, ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)


class MongoOBJ:
    @exception(logger)
    def __init__(self, db_name, db_url):
        self.dbo = self.connect(db_name, db_url)

    @exception(logger)
    def connect(self, db_name, db_url):
        try:
            logger.debug(f"Connecting to MongoDB using url: {db_url}")
            self.client = MongoClient(db_url)
            self.client.admin.command("ismaster")
        except ConnectionFailure:
            logger.critical(f"Could not connect to MongoDB using url: {db_url}")
            raise
        else:
            logger.info("Connected to MongoDB")
            return self.client.get_database(db_name)

    @exception(logger)
    def getDB(self):
        return self.dbo

    @exception(logger)
    def list_collection_names(self):
        return self.dbo.list_collection_names()

    @exception(logger)
    def get_collection(self, collectionName):
        return self.dbo.get_collection(collectionName)

    @exception(logger)
    def create_collection(self, collectionName):
        return self.dbo.create_collection(collectionName)

    @exception(logger)
    def insert_one(self, collection_name, data):
        try:
            return self.dbo[collection_name].insert_one(data)
        except InvalidDocument:
            return self.insert_one(collection_name, loads(dumps(data, cls=CustomEncoder)))

    @exception(logger)
    def insert_many(self, collection_name, data):
        try:
            return self.dbo[collection_name].insert_many(data)
        except InvalidDocument:
            return self.insert_many(collection_name, loads(dumps(data, cls=CustomEncoder)))


    @exception(logger)
    def find_one(self, collection_name, query={}):
        return self.dbo[collection_name].find_one(query)

    @exception(logger)
    def find_many(self, collection_name, query={}, data={}):
        return self.dbo[collection_name].find(query, data)

    @exception(logger)
    def update_one(self, collection_name, query, data):
        return self.dbo[collection_name].update_one(query, data)

    @exception(logger)
    def update_many(self, collection_name, query, data):
        return self.dbo[collection_name].update_many(query, data)

    @exception(logger)
    def delete_one(self, collection_name, query={}):
        return self.dbo[collection_name].delete_one(query)

    @exception(logger)
    def delete_many(self, collection_name, query={}):
        return self.dbo[collection_name].delete_many(query)

    @exception(logger)
    def find_one_and_update(self, collection_name, query, data):
        return self.dbo[collection_name].find_one_and_update(query, data)

    @exception(logger)
    def find_one_and_delete(self, collection_name, query={}):
        return self.dbo[collection_name].find_one_and_delete(query)

    @exception(logger)
    def find_one_and_replace(self, collection_name, query, data):
        return self.dbo[collection_name].find_one_and_replace(query, data)

    @exception(logger)
    def distinct(self, collection_name, query="_id"):
        return self.dbo[collection_name].distinct(query)

    @exception(logger)
    def collection2csv(self, collection):
        arr = self.find_many(collection)
        variables = arr[0].keys()
        df = DataFrame([[i.get(j) for j in variables] for i in arr], columns=variables)
        return df.to_csv(index=False)
