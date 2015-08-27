import datetime
from DataAccess.FT import FT

__author__ = 'Daniyar'

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from Adapters.MongoDB import *

class DataGrabber:
    headers = ["IncomeStatement", "BalanceSheet", "CashFlow"]
    titles = ["ASSETS", "LIABILITIES", "SHAREHOLDERS EQUITY", "OPERATIONS", "INVESTING", "FINANCING", "NET CHANGE IN CASH",
              "SUPPLEMENTAL INCOME","REVENUE AND GROSS PROFIT", "OPERATING EXPENSES",
              "INCOME TAXES, MINORITY INTEREST AND EXTRA ITEMS", "EPS RECONCILIATION", "COMMON STOCK DIVIDENDS",
              "PRO FORMA INCOME", "SUPPLEMENTAL INCOME", "NORMALIZED INCOME"]

    companies = [("IMT", "LSE"), ("BARC", "LSE")]

    def get_page(self, urlLink):
        page = requests.get(urlLink)
        return page

    def remove_unicode(self, html):
        without_unic_re = re.compile('([^\x00-\x7F]|\\n)+')
        without_unic = without_unic_re.sub('', html)
        return without_unic

    def parse_html(self, url):
        page = self.get_page(url)
        return BeautifulSoup(page.text)

    @staticmethod
    def find_table(tag):
        return tag.has_attr('data-ajax-content')

    def get_table_rows(self, html):
        table = html.find_all(DataGrabber.find_table)
        odd_trs = []
        tbodies = table[0].find_all('tbody')

        for i in range(0, len(tbodies)):
            odd_trs.extend(tbodies[i].find_all('tr'))
        return odd_trs

    def parse_rows(self, rows):
        data = {}
        subtype = "default"
        subtype_ls = []
        for row in rows:
            tds = row.select("td")
            key = tds[0].text
            if key in self.titles:
                #data.append({"subtype": subtype, "data": subtype_ls})
                subtype = key
                #subtype_ls = []
                data[subtype] = {}
            else:
                #subtype_ls.append({"item_name": key, "items": [{"value": tds[1].text, "year": "2014"},
                #                                               {"value": tds[2].text, "year": "2013"},
                #                                               {"value": tds[3].text, "year": "2012"}]})
                data[subtype].setdefault(key, {
                    "2014": tds[1].text,
                    "2013": tds[2].text,
                    "2012": tds[3].text
                    })
        #obj = [x for x in data if x["subtype"] == "default"][0]
        #data.remove(obj)
        #del data.default
        return data

    def create_df_and_dic(self, rows):
        data = dict()
        years = dict()
        #ft = FTModel(company)
        years['2012'] = dict()
        years['2013'] = dict()
        years['2014'] = dict()

        year_2014 = []
        year_2013 = []
        year_2012 = []

        names = []

        mapping = dict()

        ind = 0
        data_type = "default"
        for tr in rows:
            tds = tr.select("td")
            key = tds[0].text
            names.append(key)

            if key in self.titles:
                year_2014.append("")
                year_2013.append("")
                year_2012.append("")

                data_type = key
                years["2014"][data_type] = dict()
                years["2012"][data_type] = dict()
                years["2013"][data_type] = dict()
                continue
            mapping[key] = ind

            years['2014'][data_type][key] = tds[1].text
            years['2013'][data_type][key] = tds[2].text
            years['2012'][data_type][key] = tds[3].text

            year_2014.append(tds[1].text)
            year_2013.append(tds[2].text)
            year_2012.append(tds[3].text)

            ind+=1
        #print names
        df = pd.DataFrame(index=names)
        #df["names"] = names
        df["2014"] = year_2014
        df["2013"] = year_2013
        df["2012"] = year_2012

        data["df"] = df

        data["years"] = years

        return data

    def get_data(self, header, company):
        urlLink = "http://markets.ft.com/research/Markets/Tearsheets/Financials?s=" + company[0] + ":"+company[1]\
                  +"&subview=" + header
        html_page = self.parse_html(urlLink)
        odd_trs = self.get_table_rows(html_page)

        #data = self.create_df_and_dic(odd_trs)
        data = self.parse_rows(odd_trs)
        return data

    def get_all(self, companies):
        ls = []
        for company in companies:
            datas = dict()
            datas["company_name"] = company[0]
            datas["date_added"] = str(datetime.datetime.now())
            datas['title'] = company[2]
            datas["data"] = {}
            for header in self.headers:
                tmp_dat = self.get_data(header, company)
                #datas["data"].append({"report_type": header, "data": tmp_dat})
                datas["data"].setdefault(header, tmp_dat)
            #datas["ratios"] = 
            ls.append(datas)
        return ls

    def get_ratios(self, data):
        ratios = {}
        for report_type in data:
            for subtype in report_type["data"]:
                for items in subtype["data"]:
                    for item in items["items"]:
                        return {
                            ""
                        }
        ratios['rt'] = data['']

    def display_data(self, data):
        for company in data:
            print "--------------------------------------------------" + company + "--------------------------------------------------"
            for header in data[company]:
                print "--------------------------------------------------" + header + "--------------------------------------------------",
                print "\n"
                print data[company][header]["df"],
                print "\n"

    def write_to_excel(data):
        for company in data:
            path = "data/" + company
            with pd.ExcelWriter(path+".xls") as writer:
                for header in data[company]:
                    data[company][header]["df"].to_excel(writer, sheet_name=header)
                    #data[header]["df"].to_excel(writer)

    def encode(self, data):
        datas = list()
        for company in data:
            report_types = []
            for header in data[company]:
                years = []
                for year in data[company][header]["years"]:
                    subtypes = []
                    for data_type in data[company][header]["years"][year]:
                        values = []
                        for key in data[company][header]["years"][year][data_type]:
                            #ls.append(Data(key, data[company][header]["years"][year][data_type][key]))
                            values.append({'name': key, 'value': data[company][header]["years"][year][data_type][key]})
                        #ft = FTEncoder.FTEncoder.Encode(FTModel(company, PerYear.PerYear(year, Report(header, DataType(data_type, ls)))))
                        #datas.append(ft)
                        subtypes.append({'subtype': data_type, 'data': values})
                    years.append({'year': year, 'data': subtypes})
                report_types.append({'report_type': header, 'data': years})
            datas.append({'company_name': company, 'date_created': str(datetime.datetime.now()), 'date_updated': str(datetime.datetime.now()), 'data': report_types})
        return datas

    def run(self):
        datas = self.get_all()
        #self.display_data(datas)
        #write_to_excel(datas)
        client = MongoClient()
        db = client["FT"]
        collection = db.ftdata
        ids = self.save_to_db(datas, collection)
        #print(ids)
        #print datas[headers[0]]["df"]["2014"]["Total Inventory"]


    def companies_to_tuple(self, companies):
        conv_companies = [(obj['company_name'], obj['stock_exc'], obj['title']) for obj in companies['data']]
        return conv_companies

    def generate_data(self, companies):
        print "hit grabber"
        #dataAccess = FT()
        #companies = dataAccess.get_companies()
        print companies
        conv_companies = self.companies_to_tuple(companies)
        data = self.get_all(conv_companies)
        return data

def stub_insert_companies(companies, client):
    for company in companies:
        print client.save_company(company[0], company[1])



if __name__ == "__main__":
    dataAccess = DataGrabber()
    res = dataAccess.generate_data()
    print res
    #print dataAccess.get_data_count()
    #dataAccess.save_company('AAPL', 'NSQ')
    #dataAccess.save_company('BARC', 'LSE')
    #companies = dataAccess.get_companies()
    #print companies['data']
    #conv_companies = companies_to_tuple(companies)
    #tmp_data = grabber.get_all(conv_companies)
    #print tmp_data
    #encoded = grabber.encode(data)
    #print len(encoded)
    #print isinstance(encoded, list)

    #data = dataAccess.get_data(1, "AAPL")
    #print data
    #print len(data['data'])
    #obj = dataAccess.select_by_page(2)
    # for object in obj:
    #     print object
    #ids = dataAccess.save_data(tmp_data)
    #print ids
    #stub_insert_companies(grabber.companies, dataAccess)

    #grabber.run()
    # ft = FTModel("IMT", PerYear.PerYear("2012", Report("balance sheet", DataType("Assets", []))))
    # print ft
    # print FTEncoder.FTEncoder.Encode(ft)
