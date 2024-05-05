import pandas as pd
import pickle
from flask import Flask,jsonify,request
from flask_cors import CORS

df = pd.read_csv('./dataset/training.csv')
disc=pd.read_csv('./dataset/symptom_Description.csv')
prec=pd.read_csv('./dataset/symptom_precaution.csv')
descDis=disc['Disease'].unique()
descDiscrip=disc['Description'].unique()
precDis=prec['Disease'].unique()
prec1=prec['Precaution_1'].unique()
prec2=prec['Precaution_2'].unique()
prec3=prec['Precaution_3'].unique()
prec4=prec['Precaution_4'].unique()
modified_list = [s.replace('_', ' ') for s in df.columns]
symps=modified_list[:-1]
disease=df['prognosis'].unique()
app=Flask(__name__)

CORS(app)

model=pickle.load(open("model.pkl","rb"))

@app.route('/',methods=['GET'])
def Home():
    data={
        "message":"rthjrhng"
    }
    return jsonify(data)

@app.route('/predict',methods=['POST'])
def predict():
    ar=[0]*131
    temp=request.get_json('symp')
    data=temp['symps']
    check=[]
    for i in range(0,len(data)):
        for j in range(0,len(symps)):
            if(data[i]==symps[j]):
                ar[j]=1
                check.append(1)
    inputtest=[ar]
    index = model.predict(inputtest)
    predicted=""
    if(len(check)>=3):
        predicted=index[0]
    return jsonify(predicted)

@app.route('/desc',methods=['POST'])
def desc():
    temp=request.get_json()
    d=temp['data']
    data=d['data']
    result=""
    for x in range(0,len(descDis)):
        if descDis[x]==data:
            result=descDiscrip[x]
            break
    print(result)
    return jsonify(result)
@app.route('/prec',methods=['POST'])
def prec():
    temp=request.get_json()
    d=temp['data']
    data=d['data']
    result=[]
    for x in range(0,len(descDis)):
        if precDis[x]==data:
            result.append(prec1[x])
            result.append(prec2[x])
            result.append(prec3[x])
            result.append(prec4[x])
            break
    print(result)
    return jsonify(result)
if __name__=="__main__":
    app.run(debug=True)