__author__ = 'Daniyar'

class DataEncoder:
    @staticmethod
    def Encode(data):
        return {"name": data.name, "value": data.value}