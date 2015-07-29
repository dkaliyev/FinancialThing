__author__ = 'Daniyar'

class TablesFetcher:
    def fetch(self, model):
        new_list = []
        for report in model['data']:
            for year in report['data']:
                for subtype in year['data']:
                    for data in subtype['data']:
            new_list.append({'subtype': subtypes})