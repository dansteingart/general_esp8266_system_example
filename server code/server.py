#Data Imports
from pymongo import MongoClient as mc
import pandas as pd
import time
from numpy import *
import json
from commands import getoutput as go


#Flask Imports
from flask import Flask,request,Response,send_file
from functools import wraps

sets = json.load(open("settings.json"))
mip  = sets['mongo_ip']
port = sets['port']


cli = mc(mip)

#Instantiate Server
app = Flask(__name__)

#This pulls the node data
@app.route("/data/",methods=['POST'])
def out(var=None):
    form = json.loads(request.get_data())
    out = {}
    try:
        db  = form['db']
        col = form['col']
        q = form['q']
        #data['time'] = time.time()
        df = pd.DataFrame(list(cli[db][col].find(q)))
        del df['_id']
        data = df.to_dict(orient='records')
        out = {'status':'success','data':data}

    except Exception as E:
        out['status']  = 'error'
        out['message'] = str(E)

    return json.dumps(out)


#This puts the individual test data
@app.route("/input/",methods=['POST'])
def inp(var=None):
    form = json.loads(request.get_data())
    out = {}
    try:
        db  = form['db']
        col = form['col']
        data = form['data']
        data['time'] = time.time()
        cli[db][col].insert_one(data)
        del data['_id']
        out = {'status':'success','data':data}

    except Exception as E:
        out['status']  = 'error'
        out['message'] = str(E)

    return json.dumps(out)


#this pulls the line infrom from "last_write"
@app.route("/")
def home(): return "hey there fucko"


if __name__ == "__main__": app.run(host="0.0.0.0",port=port,debug=True)
