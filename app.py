from flask import Flask,request,render_template
import pickle


app = Flask(__name__)
model = pickle.load(open('flight_dt.pkl','rb'))


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
    y_pred = model.predict(total)
    
    print(y_pred)
    

    if(y_pred==[0.]):
        ans = "The Flight will be on time"
    else:
        ans = "The Flight will be delayed"
    return render_template("index.html",showcase= ans)

if __name__ == "__main__":
    app.run(debug=False)