import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

import json
API_KEY = "yytM9ZbPkkDZ_PWyKzXdHuJvFctkkZUdgcNhP6Caz_U7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction',methods = ["POST"])
def predict():
    name = request.form['name']
    month = request.form['month']
    dayofmonth = request.form['dayofmonth']
    dayofweek = request.form['dayofweek']
    origin = request.form['origin']
    if(origin == "msp"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,0,1,0
    if(origin == "dtw"):
        origin1,origin2,origin3,origin4,origin5 = 0,1,0,0,0
    if(origin == "jfk"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,1,0,0
    if(origin == "sea"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,0,0,1
    if(origin == "alt"):
        origin1,origin2,origin3,origin4,origin5 = 1,0,0,0,0	
    destination = request.form['destination']
    if(destination == "msp"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,0,1,0
    if(destination == "dtw"):
        destination1,destination2,destination3,destination4,destination5 = 0,1,0,0,0
    if(destination == "jfk"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,1,0,0
    if(destination == "sea"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,0,0,1
    if(destination == "alt"):
        destination1,destination2,destination3,destination4,destination5 = 1,0,0,0,0
    dept = request.form['dept']
    arrtime = request.form['arrtime']
    actdept = request.form['actdept']
    dept15 = int(dept)-int(actdept)
    total = [[name,month,dayofmonth,dayofweek,arrtime,dept15,origin1,origin2,origin3,origin4,origin5,destination1,destination2,destination3,destination4,destination5]]
    
    
    payload_scoring = {"input_data": [{"field": [["FL_NUM","MONTH","DAY_OF_MONTH","DAY_OF_WEEK","CRS_ARR_TIME","DEP_DEL15","ORIGIN_ATL","ORIGIN_DTW","ORIGIN_JFK","ORIGIN_MSP","ORIGIN_SEA","DEST_ATL","DEST_DTW","DEST_JFK","DEST_MSP","DEST_SEA"]], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4dd381d7-6e94-47f4-b00c-f01a781d53cb/predictions?version=2021-06-28', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)
    if(pred == 0):
        ans = "The Flight will be on time"
    else:
        ans = "The Flight will be delayed"
    return render_template("index.html",showcase= ans)

if __name__ == "__main__":
    app.run(debug=False)