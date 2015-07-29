from bson import ObjectId
from datetime import datetime
__author__ = 'Daniyar'
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

class JSONDecoder(json.JSONDecoder):
    def decode(self, o):

        return json.JSONDecoder.decode(self, o)
