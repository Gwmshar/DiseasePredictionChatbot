import pandas as pd
df = pd.read_csv('./dataset/training.csv')
modified_list = [s.replace('_', ' ') for s in df.columns]
symps=modified_list[:-1]
diseases=df['prognosis'].unique()
disease_symp={}

for disease in diseases:
    disease_row=df[df.iloc[:,-1]==disease]
    selected_columns=disease_row.iloc[:,:-1].columns[disease_row.iloc[:,:-1].eq(1).any()]
    disease_symp[disease]=selected_columns.tolist()
diseases_list=[{"name":disease,"symptoms":symptoms} for disease,symptoms in disease_symp.items()]

