__author__ = 'Daniyar'

import pymongo
from pymongo import MongoClient

class MongoDB:
    db_name = "FT"
    collection_name = "ftdata"
    client = {}
    collection = {}
    limit = 50

    def __init__(self):
        self.client = MongoClient()
        db = self.client[self.db_name]
        self.collection = db[self.collection_name]

    def select_by_id(self, _id):
        return self.collection.find_one({"_id": _id})

    def select_by_page(self, page, _filter=None):
        return self.collection.find(filter=_filter, skip=(page-1)*self.limit, limit=self.limit)

    def save(self, data):
        if data is not None:
            return self.collection.insert(data)
        else:
            raise ValueError

    def update(self, data):
        return self.collection.update(data)

    def delete(self, _id):
        return self.collection.delete_one({"_id": _id})
