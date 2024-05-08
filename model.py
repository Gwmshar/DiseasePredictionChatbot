import pandas as pd
import numpy as np
from sklearn.metrics import  accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
import pickle
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('./dataset/dataset.csv')
for col in df.columns:
    df[col] = df[col].str.replace('_',' ')
cols = df.columns
data = df[cols].values.flatten()
s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df.shape)
df = pd.DataFrame(s, columns=df.columns)
df = df.fillna(0)
dfx=pd.DataFrame()
dfx["Disease"]=df["Disease"]
for index, row in df.iterrows():
    for symptom in df.columns[1:]:
        if row[symptom] != 0:
            dfx.loc[index, row[symptom]] = 1
dfx = dfx.fillna(0)
dfx[dfx.columns[1:]]=dfx[dfx.columns[1:]].astype('int')
dfx.columns = dfx.columns.str.strip()
print(dfx.head())
data = dfx.iloc[:,1:].values
labels = dfx['Disease'].values
y=df['Disease'].unique()
ar=[df['Disease'].unique()]
disease=ar[0]
x_train, x_test, y_train, y_test = train_test_split(data, labels, train_size = 0.8,random_state=42)
x_train, x_val, y_train,y_val=train_test_split(data,labels,test_size=0.3,random_state=42)

print(x_test.shape)

gnb = MultinomialNB()
gnb.fit(x_train, y_train)
y_pred = gnb.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)*100
print(f'Accuracy: {accuracy}')


RForest_clf = RandomForestClassifier(n_estimators = 100)
RForest_clf.fit(x_train, y_train)
y_pred = RForest_clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)*100
print(f'Accuracy: {accuracy}')

from sklearn.neighbors import KNeighborsClassifier

kn=KNeighborsClassifier(n_neighbors=5)
kn.fit(x_train, y_train)
y_pred = kn.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)*100
print(f'Accuracy: {accuracy}')

precision=precision_score(y_test,y_pred,average='macro')*100
print("Precision:", precision)

recall=recall_score(y_test,y_pred,average='macro')*100
print("Recall:",recall)

f1=f1_score(y_test,y_pred,average='macro')*100
print("F1-score:",f1)

pickle.dump(gnb,open("model.pkl","wb"))


