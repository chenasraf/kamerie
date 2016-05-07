import pymongo

MONGO_CONN_STRING = "mongodb://localhost:27017"
MONGO_DB = "kamerie"


class Model(object):

    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(MONGO_CONN_STRING)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[self.collection_name]
