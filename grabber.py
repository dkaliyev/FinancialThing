__author__ = 'Daniyar'


import requests
from bs4 import BeautifulSoup
import re
import numpy
import pandas as pd
import time


headers = ["BalanceSheet", "IncomeStatement", "CashFlow"]

def get_page(urlLink):
    page = requests.get(urlLink)
    return page

def remove_unicode(html):
    without_unic_re = re.compile('([^\x00-\x7F]|\\n)+')
    without_unic = without_unic_re.sub('', html)
    return without_unic

def parse_html(url):
    page = get_page(url)
    return BeautifulSoup(page.text)

def get_table_rows(html):
    odd_trs = html.find_all('tr', {'class': 'odd'})

    test1 = html.find_all('tr', {'class': 'even'})
    test2 = []
    for test in test1:
        if 'section' not in test['class']:
            test2.append(test)
    odd_trs+=test2
    return odd_trs

def create_df_and_dic(rows):
    data = dict()
    years = dict()
    years['2012'] = dict()
    years['2013'] = dict()
    years['2014'] = dict()

    year_2014 = []
    year_2013 = []
    year_2012 = []

    names = []

    mapping = dict()

    ind = 0

    for tr in rows:
        tds =  tr.select("td")
        key = tds[0].text
        mapping[key] = ind
        names.append(key)
        years['2014'][key] = tds[1].text
        years['2013'][key] = tds[2].text
        years['2012'][key] = tds[3].text

        year_2014.append(tds[1].text)
        year_2013.append(tds[2].text)
        year_2012.append(tds[3].text)

        ind+=1

    df = pd.DataFrame(index=names)
    #df["names"] = names
    df["2014"] = year_2014
    df["2013"] = year_2013
    df["2012"] = year_2012

    data["df"] = df

    data["years"] = years

    return data

def get_data(url):
    urlLink = "http://markets.ft.com/research/Markets/Tearsheets/Financials?s=IMT%3ALSE&subview=" + url
    html_page = parse_html(urlLink)

    odd_trs = get_table_rows(html_page)

    data = create_df_and_dic(odd_trs)

    return data

def get_all():
    datas = dict()
    for header in headers:
            datas[header] = get_data(header)
    return datas

def display_data(data):
    for header in data:
        print "--------------------------------------------------" + header + "--------------------------------------------------",
        print "\n"
        print data[header]["df"],
        print "\n"

def write_to_excel(data):
    with pd.ExcelWriter("data" + ".xls") as writer:
        for header in data:
            data[header]["df"].to_excel(writer, sheet_name=header)



def run():

    # (df_BalanceSheet, years_BalanceSheet) = get_data("BalanceSheet")
    #
    # print df_BalanceSheet
    #
    # print "-------------- Income Statement---------"
    # (df_IncomeStatement, years_IncomeStatement) = get_data("IncomeStatement")
    #
    # print df_IncomeStatement

    datas = get_all()
    #display_data(datas)
    write_to_excel(datas)

    #print datas[headers[0]]["df"]["2014"]["Total Inventory"]



if __name__ == "__main__":
    run()