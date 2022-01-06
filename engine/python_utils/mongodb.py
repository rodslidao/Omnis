from pymongo import MongoClient, collection
from pprint import pprint
from common_classes import *
class MongoDB(json):
    def __init__(self, host, port, initialDB="admin") -> None:
        self.port = port
        self.host = host
        self.client = MongoClient(f"mongodb://{self.host}:{self.port}", connect=True)
        self.database = self.client.get_database(initialDB)
    
    def get_collections(self):
        return self.database.list_collection_names()

    def acces_db_function(self, function, *args, **kwargs):
        return getattr(self.database, function)(*args, **kwargs)
    
    def acces_collection_function(self,collection, function, *args, **kwargs):
        return getattr(self.database[collection], function)(*args, **kwargs)

    def insert_one(self, collection, data):
        self.database[collection].insert_one(data).inserted_id

    def insert_many(self, collection, data):
        pprint(data)
        self.database[collection].insert_many(data)
    
    def find_one(self, collection, query):
        return self.database[collection].find_one(query)
    
    def find_many(self, collection, query):
        return self.database[collection].find(query)

import os
from os.path import isfile, join
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
mypath = fr"{script_dir}\data\json\config\editable\data"
onlyfiles = [f.split(".")[0] for f in os.listdir(mypath) if isfile(join(mypath, f))]
mongo = MongoDB("192.168.1.31", 27017, "Omnis")
for name in onlyfiles:
    if name not in mongo.get_collections():
        json_file = json(fr"{mypath}\{name}.json")()
        mongo.insert_many(name, json_file)
