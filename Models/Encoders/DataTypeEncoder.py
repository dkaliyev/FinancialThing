from Models.Encoders import DataEncoder

__author__ = 'Daniyar'

class DataTypeEncoder:
    @staticmethod
    def Encode(datatype):
        return {"name": datatype.name, "data": [DataEncoder.DataEncoder.Encode(x) for x in datatype.data]}