import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "vYcMJSsetjmAszl1wlvzsw2ogISgi3FABAwZAvYBj3Np"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], "values": [[320,100,2,3,4,8.23,0]]}]}
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a5037cc3-64cd-410e-9acc-2bd9da728164/predictions?version=2022-11-17',
json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
import pickle
from flask import Flask , request, render_template
from math import ceil
app = Flask(__name__)
app = Flask(__name__, template_folder='template',static_folder='static') 
model = pickle.load(open("model(1).pkl","rb"))

@app.route('/')
def home():
	return render_template('demo.html')

@app.route('/predict',methods = ['GET','POST'])
def admin():
    gre=(eval(request.form["gre"])-290)/(340-290)
    tofl=(eval(request.form["tofel"])-92)/(120-92)
    rating=(eval(request.form["university_rating"])-1.0)/4.0
    sop=(eval(request.form["sop"])-1.0)/4.0
    lor=(eval(request.form["lor"])-1.0)/4.0
    cgpa=(eval(request.form["cgpa"])-6.7)/(10.0-6.7)
    research=request.form["yes_no_radio"]
    print("byeeee")
    if (research=="Yes"):
        print("yesss")
        research=1
    else:
        print("nooo")
        research=0
    preds=[[gre,tofl,rating,sop,lor,cgpa,research]]
    #payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], "values": [[gre,tofl,rating,sop,lor,cgpa,research]]}]}
    xx=model.predict(preds)
    if (xx>0.5):
        return render_template("chance.html",p=str(ceil(xx[0]*100))+"%")
    return render_template("nochance.html")
if __name__ == '__main__':
    app.run(debug = False, port=4000)
