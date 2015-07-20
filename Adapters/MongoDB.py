from bson import ObjectId

__author__ = 'Daniyar'

import pymongo
from pymongo import MongoClient

class MongoDB:
    db_name = "FT"
    collection_name = "ftdata"
    companies_collection_name = "companies"
    client = {}
    collection = {}
    companies_collection = {}
    limit = 50

    def __init__(self, _db_name=None, _collection_name=None, _companies_collection_name=None):
        self.client = MongoClient()
        if _db_name is not None:
            self.db_name = _db_name
        if _collection_name is not None:
            self.collection_name = _collection_name
        if _companies_collection_name is not None:
            self.companies_collection_name = _companies_collection_name
        db = self.client[self.db_name]
        self.collection = db[self.collection_name]
        self.companies_collection = db[self.companies_collection_name]
        print "instance of MongoDB created"

    def select_by_id(self, _id):
        return self.collection.find_one({"_id": ObjectId(_id)})

    def select_by_page(self, page, _filter=None):
        ls = []
        collection = self.collection.find(filter=_filter, skip=(page-1)*self.limit, limit=self.limit)
        for item in collection:
            ls.append(item)
        return ls

    def save(self, data):
        if data is not None:
            return self.collection.insert_one(data).inserted_id
        else:
            raise ValueError

    def save_many(self, data):
        return self.collection.insert_many(data).inserted_ids

    def update(self, data):
        return self.collection.update(data)

    def update(self, data):
        return self.collection.update_many(None, data)

    def delete(self, _id):
        return self.collection.delete_one({"_id": ObjectId(_id)})

    def select_companies(self):
        return [x for x in self.companies_collection.find()]

    def save_company(self, name, exg):
        return self.companies_collection.insert_one({"company_name": name, "stock_exc": exg}).inserted_id
