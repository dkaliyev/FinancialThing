__author__ = 'Daniyar'

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from DataAccess.FT import FT
from Helpers import JSONHelper
from grabber.grabber import DataGrabber



from flask import Flask, render_template, request

app = Flask(__name__)

app.debug = True

dataAccess = FT()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables', methods=['GET'])
def tables():
    count = dataAccess.get_data_count()
    companies = dataAccess.get_companies()
    company_list = [{'name': x['company_name'], 'active': False} for x in companies['data']]
    if company_list != []:
        company_list[0]['active'] = True
    return render_template('tables.html', obj={'count': count, 'company_list': company_list})

@app.route('/api/tables/<company_name>', methods=['GET'])
def tables_by_company(company_name):
    #company_name = request.get_json()
    res = dataAccess.get_data(1, company_name)
    company = res['data']
    return JSONHelper.JSONEncoder().encode({"data": company})

@app.route('/api/companies', methods=['POST'])
def save_company():
    obj = request.json['data']
    comp = obj['name']
    ex = obj['ex']
    if comp is not None and ex is not None:
        res = dataAccess.save_company(comp, ex)
    return '1'

@app.route('/api/data/generate', methods=['GET'])
def generate_data():
    grabber = DataGrabber()
    data = grabber.generate_data()
    #return '1'
    if dataAccess.save_data(data) is not []:
        return '1'
    else:
        return '0'

if __name__ == '__main__':
    app.run(host='0.0.0.0')