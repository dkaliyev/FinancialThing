from Helpers import JSONHelper

__author__ = 'Daniyar'

import requests

host = "http://127.0.0.1:5001/"

class FT:
    def __init__(self, _host=None):
        if _host is not None:
            self.host = _host

    def get_data_count(self):
        urlLink = host+'data/count'
        result = requests.get(urlLink)
        return result.text

    def get_companies(self):
        urlLink = host+"companies"
        result = requests.get(urlLink).text
        return JSONHelper.JSONDecoder().decode(result)

    def save_company(self, name, exch):
        urlLink = host+"companies"
        result = requests.post(url=urlLink, json={'data': {'name': name, 'exch': exch}})
        return result.text

    def save_data(self, data):
        urlLink = host+'data'
        result = requests.post(url=urlLink, json={'data': data})
        return result.text

    def get_data(self, page, company=None):
        if company is None:
            urlLink = host+'data/'+str(page)
        else:
            urlLink = host+'data/'+company+'/'+str(page)
        result = requests.get(urlLink)
        return JSONHelper.JSONDecoder().decode(result.text)

    def generate_data(self):
        urlLink = host+'data/generate'
        result = requests.get(urlLink)
        return JSONHelper.JSONDecoder().decode(result.text)