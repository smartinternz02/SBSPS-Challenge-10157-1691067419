from flask import Flask,request,render_template
import requests
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('svc_classifier.pkl')


@app.route('/')
def home():
    return render_template('input.html')


@app.route('/input',methods = ['POST'])
def pred():
    input = pd.DataFrame({
    'gender':[float(request.form.get('gender'))],
    'ssc_p' : [float(request.form.get('ssc'))],
    'hsc_p'  : [float(request.form.get('hsc'))],
    'degree'  : [float(request.form.get('degree'))],
    'workex'  : [float(request.form.get('experience'))],
    'specialisation'  : [float(request.form.get('specialization'))],
    'mba_p'  : [float(request.form.get('mba'))],
    'etest_p'  : [float(request.form.get('etest'))]
    })
    
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "fjV56-SpxhgN_4YMPTOvbFBbDK4NzhgqLr4DNQefeCRU"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ "f0","f1","f2","f3","f4","f5","f6","f7"], 
                                       "values": [[input["gender"][0],input["ssc_p"][0],
                                       input["hsc_p"][0],input["degree"][0],input["workex"][0],
                                       input["specialisation"][0],input["mba_p"][0],
                                       input["etest_p"][0]]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/38f4a172-9a51-437a-a158-33c565666f9f/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()["predictions"][0]["values"][0][0]
    input["status"]=[float(op)]





    print(input)

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "lKG-jN4zm3kYgXXHfRazkdLwyikNkrREYgC2KofrgQ4O"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ "gender",
                                "ssc_p",
                                "hsc_p",
                                "degree_p",
                                "workex",
                                "specialisation",
                                "mba_p",
                                "status",
                                "etest_p"],
                            "values": [
                                [input["gender"][0],input["ssc_p"][0],
                                       input["hsc_p"][0],input["degree"][0],input["workex"][0],
                                       input["specialisation"][0],input["mba_p"][0],
                                       input["status"][0],input["etest_p"][0]]
                                ]
                                }
                                ]
                                }
    print("Second-------------------------------->")
    print(input)
    print(type(payload_scoring))
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e4c7341a-fb57-42e3-8155-f4d5d5aae19a/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())

    op2=response_scoring.json()["predictions"][0]["values"][0][0]





    if op==1:
        op="Placed"
        op2='₹'+str(op2).split(".")[0]
    else:
        op="Not Placed"
        op2=""
    #print(op)
    return render_template('input.html',Output=str(op),sal=str(op2))

if __name__ == '__main__':
    app.run()

'''lKG-jN4zm3kYgXXHfRazkdLwyikNkrREYgC2KofrgQ4O'''