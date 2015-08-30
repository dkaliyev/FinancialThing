from bson import ObjectId

__author__ = 'Daniyar'

import pymongo
from pymongo import MongoClient

class MongoDB:
    db_name = "FT"
    collection_name = "ftdata3"
    companies_collection_name = "companies"
    codes_collection_name = "codes"
    codes_collection = {}
    client = {}
    collection = {}
    companies_collection = {}
    limit = 50
    code_to_names = {}

    def __init__(self, _db_name=None, _collection_name=None, _companies_collection_name=None, _codes_collection_name=None, _limit=None):
        self.client = MongoClient()
        if _db_name is not None:
            self.db_name = _db_name
        if _collection_name is not None:
            self.collection_name = _collection_name
        if _companies_collection_name is not None:
            self.companies_collection_name = _companies_collection_name
        if _codes_collection_name is not None:
            self.codes_collection_name = _codes_collection_name
        if _limit is not None:
            self.limit = _limit
        db = self.client[self.db_name]
        self.collection = db[self.collection_name]
        self.companies_collection = db[self.companies_collection_name]
        self.codes_collection = db[self.codes_collection_name]
        print "instance of MongoDB created"

    def get_data_count(self):
        return self.collection.count()

    def select_by_id(self, _id):
        return self.collection.find_one({"_id": ObjectId(_id)})

    def select_by_page(self, page, _filter=None):
        ls = []
        if not self.code_to_names:
            codes = self.codes_collection.find()[0]['mapping']
            for obj in codes:
                self.code_to_names[obj['code']] = obj['name']
        collection = self.collection.find(filter=_filter, skip=(page-1)*self.limit, limit=self.limit)
        print self.code_to_names
        for item in collection:
            data = MongoDB.Decode(item['data'], self.code_to_names)
            item['data'] = data
            ls.append(item)
        print ls
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

    def select_codes(self):
        return self.codes_collection.find()[0]

    def save_company(self, name, exg, title):
        company = self.companies_collection.find_one({"company_name": name});
        if company is not None:
            return {'status': -1, 'message': "Company already exists"}
        ins_id = str(self.companies_collection.insert_one({"company_name": name, "stock_exc": exg, "title": title, "isVisible": True}).inserted_id)    
        return {'status': 0, 'message': 'Company saved successfully'}

    def remove_company(self, name):
        if name is not None and name != "":
            result = self.companies_collection.delete_one({"company_name":name}).deleted_count
            result2 = self.collection.delete_many({'company_name': name}).deleted_count
            if result>0:
                return {'status': 0}
            else:
                return {'status': -1, 'message': 'Cannot remove company'}
        return {'status': -1, 'message': 'Specify name of the company'}

    def update_company(self, updates):
        if updates is not None:
            for update in updates:
                for key in update:
                    self.companies_collection.update_one({'company_name': key}, {'$set': {'isVisible': update[key]}})
        return {'status': 0, 'message': 'Updated!'}            


    @staticmethod
    def Decode(data, codes):
        newData = {}
        for key, value in data.iteritems():
            if isinstance(value, dict) and key in codes.keys():
                value = MongoDB.Decode(value, codes)
            if key in codes.keys():
                newData[codes[key]] = value
            else:
                newData[key] = value
        return newData