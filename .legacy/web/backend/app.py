import os
import json
import flask
from flask import Flask,request
from flask_cors import CORS

os.environ["FLASK_APP"]="app.py"
app=Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "flask.backend"

@app.route("/cafes",methods=["GET","POST"])
def cafes():
    with open("cafes.json","w",encoding="utf-8-sig") as jsonfile:
        try:
            jsondata=json.load(jsonfile)
        except:
            jsondata=[]
        if request.method=="GET":
                return flask.jsonify(jsondata)
        elif request.method=="POST":
            sendData=request.get_json()
            sendData_=json.dumps(sendData)
            print(sendData_)
            jsondata.append(sendData_)
            return flask.Response(response=f"got name({sendData['name']})",status=201)
        json.dump(jsondata,jsonfile,indent=2)

if __name__=="__main__":
    app.run("localhost",11115)