__author__ = 'Daniyar'

class DataType(dict):
    name = ""
    data = []

    def __init__(self, name, datas):
        self.name = name
        self.data = datas
