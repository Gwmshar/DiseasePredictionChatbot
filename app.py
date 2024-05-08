import pandas as pd
import pickle
from flask import Flask,jsonify,request
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy

nlp=spacy.load("en_core_web_md")

df = pd.read_csv('./dataset/originalmini.csv')
disc=pd.read_csv('./dataset/symptom_Description.csv')
descDis=disc['Disease'].unique()
descDiscrip=disc['Description'].unique()
df.columns = [s.replace('_', ' ') for s in df.columns]
symps=df.columns[1:]
diseases=df['Disease'].unique()
app=Flask(__name__)

CORS(app)

model=pickle.load(open("model.pkl","rb"))

disease_symp={}
user_symp=[]

for disease in diseases:
    disease_row = df[df.iloc[:,0] == disease]
    selected_columns = disease_row.iloc[:,1:-1].columns[disease_row.iloc[:,1:-1].eq(1).any()]
    disease_symp[disease] = selected_columns.tolist()

diseases_list = [{"name": disease, "symptoms": symptoms} for disease, symptoms in disease_symp.items()]

def calc_sim(user_symp, data_symp):
    user_vect = nlp(user_symp).vector
    data_vector = [nlp(symptom).vector for symptom in data_symp]
    sim_scores = []
    for dataset_vector in data_vector:
        norm_user = np.linalg.norm(user_vect)
        norm_data = np.linalg.norm(dataset_vector)
        if norm_user != 0 and norm_data != 0:
            sim_score = np.dot(user_vect, dataset_vector) / (norm_user * norm_data)
            sim_scores.append(sim_score)
        else:
            sim_scores.append(0)
    return data_symp[np.argmax(sim_scores)]
def find_most_sim(user_symp,diseases_list):
    all_dataset_symp=[symptom for disease in diseases_list for symptom in disease['symptoms']]
    most_sim_symp=[calc_sim(user_sym,all_dataset_symp) for user_sym in user_symp]
    return most_sim_symp
def suggest(u_symp,diseases_list):
    user_text=' '.join(u_symp)
    disease_text=[' '.join(disease['symptoms']) for disease in diseases_list]
    vectorize=CountVectorizer()
    symp_matrix=vectorize.fit_transform([user_text]+disease_text)
    simi_score=cosine_similarity(symp_matrix)[0][1:]
    most_sim_idx=simi_score.argmax()
    related_symp=[symptom for symptom in diseases_list[most_sim_idx]['symptoms'] if symptom not in user_symp]
    return related_symp
def extract_symp(user_input):
    doc=nlp(user_input)
    u_symp=[]
    if user_input in symps:
        u_symp.append(user_input)
        return u_symp
    for chunk in doc.noun_chunks:
        u_symp.append(chunk.text)
    return u_symp

@app.route('/',methods=['GET'])
def Home():
    data={
        "message":"rthjrhng"
    }
    return jsonify(data)

userHas=[]
userNotHave=[]
related_sym=[]
flag=0
count=0
idx=0

def chatLogic(data):
    global flag,related_sym,userHas,userNotHave,count,idx,symps
    if flag==0:
        user_symp=extract_symp(data)    
        most_sim_symp=find_most_sim(user_symp,diseases_list)
        related_sym=suggest(most_sim_symp,diseases_list)
        print(related_sym)
        for x in range(0,len(most_sim_symp)):
            userHas.append(most_sim_symp[x])
        flag=1
        idx=0    
        while idx < len(related_sym):
            if related_sym[idx] not in userHas and related_sym[idx] not in userNotHave:
                idx=idx+1
                count=count+1
                return("Are you suffuring from "+related_sym[idx-1]+" (yes/no)")
            else:
                idx=idx+1
    if data=="yes" and flag==1 and count<=3:
        most_sim_symp=find_most_sim(userHas,diseases_list)
        related_sym=suggest(most_sim_symp,diseases_list)
        count=count+1
        if idx <= len(related_sym) and related_sym[idx-1] not in userHas:
            userHas.append(related_sym[idx-1])
        if count<=3:
            idx=0
            while idx < len(related_sym):
                if related_sym[idx] not in userHas and related_sym[idx] not in userNotHave:
                    idx=idx+1
                    return ("Are you suffuring from "+related_sym[idx-1]+" (yes/no)")
                else:
                    idx=idx+1
            count=5
            return("Do you have more symptoms ? (yes or no)")
    elif data=="no" and flag==1 and count<=3:
        most_sim_symp=find_most_sim(userHas,diseases_list)
        related_sym=suggest(most_sim_symp,diseases_list)
        count=count+1
        if idx <= len(related_sym) and related_sym[idx-1] not in userNotHave:
            userNotHave.append(related_sym[idx-1])
        if count<=3:
            idx=0
            while idx < len(related_sym):
                if related_sym[idx] not in userHas and related_sym[idx] not in userNotHave:
                    idx=idx+1
                    return ("Are you suffuring from "+related_sym[idx-1]+" (yes/no)")
                else:
                    idx=idx+1
            count=5
            return("Do you have more symptoms ? (yes or no)")
    elif flag==1 and count<=3:
        return ("Please type only yes or no")
    if count==4 or count==5:
        if data=="yes" and count==5:
            count=0
            flag=0
            return ("Ok give more symptoms")
        elif data=="no" and count==5:
            if len(userHas)<=3:
                return ("Sorry we can not detect disese with only those provide symptoms")
            ar=[0]*131
            for i in range(0,len(userHas)):
                for j in range(0,len(symps)):
                    if(userHas[i]==symps[j]):
                        ar[j]=1
            inputtest=[ar]
            index = model.predict(inputtest)
            predicted=index[0]
            result=""
            for x in range(0,len(descDis)):
                if descDis[x]==predicted:
                    result=descDiscrip[x]
                    break
            return ("You may have "+predicted+"\nDescription of "+predicted+": "+result)
        else:
            count=count+1
            return ("Do you have more symptoms ? (yes or no)")
            
@app.route("/reset",methods=['POST'])
def reset():
    global flag,related_sym,userHas,userNotHave,count,idx
    flag=0
    related_sym=[]
    userHas=[]
    userNotHave=[]
    count=0
    idx=0
    return "Restart"

@app.route("/predict",methods=['POST'])
def test():
    temp=request.get_json('symp')
    data=temp['symps']
    result=chatLogic(data)
    return jsonify(result)
if __name__=="__main__":
    app.run(debug=True)