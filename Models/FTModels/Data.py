__author__ = 'Daniyar'

class Data(dict):
    name = ""
    value = ""

    def __init__(self, name, value):
        self.name = name
        self.value = value

