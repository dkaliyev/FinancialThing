import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Adapters.MongoDB import MongoDB

if __name__ == "__main__":
	client = MongoDB()
	#data = client.select_by_page(1, {'company_name': "BARC"})
	data = client.collection.find()[0]['data']
	print data
	codes = client.codes_collection.find()[0]['mapping']
	mapping = {}
	for obj in codes:
		mapping[obj['code']] = obj['name']
	ts = MongoDB.Decode(data, mapping)
	print "-----------------------------"
	print ts
	#obj = {"one": 1, "two": 2, "three":3, "four": {"e": 4, "f": 3}}
	#newObj = MongoDB.Decode(obj, {"one": "new one", "two": "new two", "three": "new three", "four": "new four", "f": "s", "e": "a"})
	#print newObj