__author__ = 'Daniyar'

class Report(dict):
    name = ""
    data = {}

    def __init__(self, name, dataType):
        self.name = name
        self.data = dataType

