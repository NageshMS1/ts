import pandas as pd
import sqlite3
from data import *
from flask import Flask, request
from datetime import datetime
app = Flask(__name__)
conn = sqlite3.connect('finance.db')
@app.route('/stocks/<date>')
def get_stocks(Date):
    time = datetime.strptime(time, '%Y-%m-%d')
    df = pd.read_sql_query(f"SELECT * FROM finance WHERE date = '{time}'", conn)
    return df.to_json(orient='records')
@app.route('/stocks/<company>')
def get_company(company):
    df = pd.read_sql_query(f"SELECT * FROM finance WHERE symbol = '{company}'", conn)
    return df.to_json(orient='records')
@app.route('/stocks/<company>/<date>', methods=['POST', 'PATCH'])
def update_stocks(company, date):
    date = datetime.strptime(date, '%Y-%m-%d')
    data = request.get_json()
    que = f"UPDATE finance SET "
    for key, value in data.items():
        que += f"{key} = '{value}', "
    que = que[:-2] + f" WHERE symbol = '{company}' AND date = '{date}'"
    conn.execute(que)
    conn.commit()
    return {'message': 'updated successfully'}
if __name__=='__main__':
    app.run(debug=True)