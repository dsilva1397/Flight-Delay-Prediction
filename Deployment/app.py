import os
from flask import redirect, send_from_directory     
from flask import Flask, render_template, request
import pandas as pd
import pickle as pkl
from datetime import datetime


app = Flask(__name__)
model = pkl.load(open('model.pkl', 'rb'))
dest_col = []

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST" :
        ref_df = pd.read_csv("refData.csv")
        df = pd.read_json("sample.json")
        df.drop(df.index, inplace=True)
        df.loc[len(df)] = 0
        destination = request.form['dest']
        year = int(request.form['year'])
        df["Year"] = year
        month = int(request.form['month'])
        df["Month"] = month
        day = int(request.form['day'])
        df["DayofMonth"] = day
        day_of_week = datetime(year =year, month = month, day = day).weekday()
        df["DayOfWeek"] = day_of_week
        act = float(int(request.form['aet']))
        df["ActualElapsedTime"] = float(int(request.form['aet']))
        crse = float(int(request.form['cet']))
        df["CRSElapsedTime"] = crse
        art = float(int(request.form['at']))
        df["AirTime"] =  art
        depd = float(int(request.form['dd']))
        df["DepDelay"] = depd
        df["Distance"] = int(ref_df["Distance"].where(ref_df["Dest"] == destination).dropna().iloc[0])
        txin = float(int(request.form['ti']))
        df["TaxiIn"] = txin
        txot = float(int(request.form['to']))
        df["TaxiOut"] = txot
        crd = float(int(request.form['cd']))
        df["CarrierDelay"] = crd
        wed = float(int(request.form['wd']))
        df["WeatherDelay"] = wed
        nad = float(int(request.form['nad']))
        df["NASDelay"] = nad
        sedy = float(int(request.form['sd']))
        df["SecurityDelay"] = float(int(request.form['sd']))
        lady = float(int(request.form['lad']))
        df["LateAircraftDelay"] = lady
        df["Dest_" + destination] = 1
        value = model.predict(df)
        return render_template("index.html", predicted  = round(value[0], 2), ACT  = round(act, 2), ET = round(crse, 2), AT = round(art, 2), DPD =  round(depd, 2), Txin = round(txin, 2), Txot = round(txot, 2), CD = round(crd, 2), SD = round(sedy, 2), LAD = round(lady, 2), WD = round(wed, 2), NAD = round(nad, 2) )
    else:
        return redirect("/")


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)