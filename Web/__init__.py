from DataAccess.FT import FT

__author__ = 'Daniyar'

from flask import Flask, render_template

app = Flask(__name__)

app.debug = True

dataAccess = FT()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables')
def tables():
    count = dataAccess.get_data_count()
    return render_template('tables.html', obj={'count': count})

if __name__ == '__main__':
    app.run(host='0.0.0.0')