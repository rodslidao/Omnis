from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from os import environ
from src.manager import logger
from pandas import DataFrame
# get environment variable "NODE_ENV"
#environment = os.environ.get("NODE_ENV", "DEV")


db_port = environ.get("DB_PORT", "27017")
db_ip = environ.get("SERVER_IP", "localhost")

url = f"mongodb://{db_ip}:{db_port}/"

_db = None
requiredCollections = ["node-configs", "node-templates", "last-values", "node-history"]

def getDb():
    global _db
    if _db is None:
        _db = MongoOBJ("Teste", url)
    return _db

def connectToMongo(database="Teste"):
    getDb()
    for collectionName in requiredCollections:
        if collectionName not in _db.list_collection_names():
            _db.create_collection(collectionName)
            logger.debug(f"Created collection {collectionName}")

def log_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.critical("MongoDB cant execute function: " + function.__name__ +"reason: " + str(e))
            raise e
    return wrapper
class MongoOBJ():
    def __init__(self, db_name, db_url):
        self.dbo = self.connect(db_name, db_url)

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

    @log_error
    def getDB(self):
        return self.dbo

    @log_error
    def list_collection_names(self):
        return self.dbo.list_collection_names()
    
    @log_error
    def get_collection(self, collectionName):
        return self.dbo.get_collection(collectionName)

    @log_error
    def insert_one(self, collection_name, data):
        return self.dbo[collection_name].insert_one(data)
    
    @log_error
    def insert_many(self, collection_name, data):
        return self.dbo[collection_name].insert_many(data)
    
    @log_error
    def find_one(self, collection_name, query={}):
        return self.dbo[collection_name].find_one(query)
    
    @log_error
    def find_many(self, collection_name, query={}):
        return self.dbo[collection_name].find(query)
    
    @log_error
    def update_one(self, collection_name, query, data):
        return self.dbo[collection_name].update_one(query, data)
    
    @log_error
    def update_many(self, collection_name, query, data):
        return self.dbo[collection_name].update_many(query, data)
    
    @log_error
    def delete_one(self, collection_name, query={}):
        return self.dbo[collection_name].delete_one(query)

    @log_error
    def delete_many(self, collection_name, query={}):
        return self.dbo[collection_name].delete_many(query)

    @log_error
    def find_one_and_update(self, collection_name, query, data):
        return self.dbo[collection_name].find_one_and_update(query, data)
    
    @log_error
    def find_one_and_delete(self, collection_name, query={}):
        return self.dbo[collection_name].find_one_and_delete(query)
    
    @log_error
    def find_one_and_replace(self, collection_name, query, data):
        return self.dbo[collection_name].find_one_and_replace(query, data)
    
    @log_error
    def collection2csv(self, collection):
        arr = self.find_many(collection)
        variables = arr[0].keys()
        df = DataFrame([[i.get(j) for j in variables] for i in arr], columns = variables)
        return df.to_csv(index=False)
