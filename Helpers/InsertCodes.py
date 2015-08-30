import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pymongo
from pymongo import MongoClient
from Models.Encoders.DataEncoder import DataEncoder

if __name__ == "__main__":
	db_name = "FT"
	collection_name = "codes"
	ls = []
	nameTocode = DataEncoder.name_to_code
	client = MongoClient()
	db = client[db_name]
	collection = db[collection_name]
	keys = nameTocode.keys()
	for key in keys:
		ls.append({"code": nameTocode[key], "name": key})

	collection.insert_one({"mapping": ls})