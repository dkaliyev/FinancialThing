__author__ = 'Daniyar'

class PerYear(dict):
    year = ""
    data = {}

    def __init__(self, year, reportType):
        self.year = year
        self.data = reportType
