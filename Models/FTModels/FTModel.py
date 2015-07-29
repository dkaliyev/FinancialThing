import datetime

__author__ = 'Daniyar'

class FTModel(dict):
    company_name = ""
    date_created = datetime.datetime.utcnow()
    data = {}

    def __init__(self, company_name, perYear):
        self.company_name = company_name
        self.data = perYear
