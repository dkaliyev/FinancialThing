__author__ = 'Daniyar'

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, jsonify, request
from grabber.grabber import DataGrabber
from Adapters.MongoDB import MongoDB
from Helpers import JSONHelper
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
repo = MongoDB()

@app.route('/data/<int:page>', methods=['GET'])
def hello_world(page=1):
    models = repo.select_by_page(page)
    return JSONHelper.JSONEncoder().encode({"data": models})

@app.route('/data', methods=['POST'])
def save_data():
    obj = request.json['data']
    if obj is not None:
        return JSONHelper.JSONEncoder().encode({'result': repo.save_many(obj)})
    else:
        return '-1'

@app.route('/data/generate', methods=['GET'])
def save_data_from_FT():    
    companies = repo.select_companies()
    codes = repo.select_codes()['mapping']
    code = {}
    for obj in codes:
        code[obj['name']] = obj['code']
    grabber = DataGrabber({"data":companies}, code)
    data = grabber.generate_data()
    return JSONHelper.JSONEncoder().encode({'result': repo.save_many(data)})

@app.route('/data/count', methods=['GET'])
def get_data_count():
    return str(repo.get_data_count())

@app.route('/companies', methods=['GET'])
def get_companies():
    companies = repo.select_companies()
    return JSONHelper.JSONEncoder().encode({"data": companies})

@app.route('/data/<name>/<int:page>')
def get_company_by_name(name, page):
    data = repo.select_by_page(page, {'company_name': name})
    return JSONHelper.JSONEncoder().encode({"data": data})

@app.route('/companies/add', methods=["POST"])
def save_company():
    obj = request.json['data']
    if obj is not None and obj['name'] is not None and obj['exch'] is not None:
        company_page = requests.get("http://markets.ft.com/research/Markets/Tearsheets/Summary?s="+obj['name']+":"+obj['exch']).text
        html = BeautifulSoup(company_page)
        name = html.find_all('span', 'formatIssueName')
        if len(name) != 0:
            return JSONHelper.JSONEncoder().encode(repo.save_company(obj['name'], obj['exch'], name[0].text))
    else:
        return JSONHelper.JSONEncoder().encode({'status': -1, 'message': 'Specify name and stock exchange'})

@app.route('/companies/remove', methods=["POST"])
def delete_company():
    obj = request.json['data']
    name = obj['name']
    return JSONHelper.JSONEncoder().encode(repo.remove_company(name))

@app.route('/companies/update', methods=['POST'])
def update_company():
    obj = request.json['data']
    return JSONHelper.JSONEncoder().encode(repo.update_company(obj))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5001)
