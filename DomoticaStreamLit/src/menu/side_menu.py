import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import requests

from src.data.load import load_azure_data
from src.data.load import load_model_url
from src.data.load import load_databricks_token
from src.data.load import load_local_group
from src.features.transform import signals_selection
from src.features.transform import preprocessing

from src.model.prediction import forest_prediction

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest

def start_side_menu():
    st.sidebar.title("Test")
    value = st.sidebar.radio("Scegli luogo",("Edificio1","Edificio3","Villa"))

    if value == "Edificio1":
        EId = 1
    elif value == "Edificio3":
        EId = 5
    elif value == "Villa":
        EId = 6

    df_group = load_local_group()
    df_group_descr = df_group[["Id","IdBuilding","Description","ValueType"]][df_group.IdBuilding == EId ]
     # Unità di misura da tenere e tipologie di rilevazioni da rimuovere
    measures_to_keep = ['ppm', 'C°', '%', 'W', 'Wh']
    description_to_remove = ['Daikin Active Power Total','Consumo enel di E1 + Villa']
    
     # Rimuovo i record associati a rilevazioni di tipo booleano
    df_group_descr = df_group_descr[df_group_descr['ValueType'].isin(measures_to_keep) == True]
    
    # Rimuovo i record associati a rilevazioni di tipo "Daikin Active Power Total" e "Consumo Enel di E1 + Villa"
    df_group_descr = df_group_descr[df_group_descr['Description'].isin(description_to_remove) == False]
    df_group_descr = df_group_descr[["Id","Description","ValueType"]]
    #creo la lista di liste per creare la select box
    list_descr = df_group_descr.values.tolist()

    df_selectbox = pd.DataFrame(list_descr, columns=['Id','Description',"ValueType"])

    values = df_selectbox['Description'].tolist()
    options = df_selectbox['Id'].tolist()
     
    dic = dict(zip(options, values))
    Id_descr = st.sidebar.selectbox('Choose a Measure', options, format_func=lambda x: dic[x])
    valueType = df_selectbox["ValueType"][df_selectbox.Id == Id_descr].values
   

    if valueType == 'ppm':
        value_measure =         st.sidebar.slider("CO2", 1, 15000, 25, 1)
    elif valueType == 'C°':
        value_measure =         st.sidebar.slider("Gradi", -10, 500, 20, 1)
    elif valueType == '%':
        value_measure =         st.sidebar.slider("%_umidità", 0, 200, 25, 1)
    elif valueType == 'W':
        value_measure =         st.sidebar.slider("produzione fotovoltaico", -1000, 10000, 5000, 100)
    elif valueType == 'Wh':
        value_measure =         st.sidebar.slider("consumo energetico", 0, 10000, 2000, 100)
  
   
    
    today =  datetime.date.today()
    day_calendar = st.sidebar.date_input("Selziona data di test", today)
    st.text("Carica dati da db azure")
    day = day_calendar.weekday()
    print("day:", day )
    mese = day_calendar.month
    print("mese:", mese )
    row = [Id_descr,value_measure,mese,day]

    if (st.button('Carica Dati da DataBase')):
        # Carico i dati dal database
        df_log = load_azure_data()        
       
        # Seleziono i log che possono essere oggetto di predizione nel modello
        sel_logs = signals_selection(df_log, df_group)
        
        # Effettuo il preprocessing dei log selezionati, ricavando le features necessarie all'Anomaly Detection
        # tramite il modello
        test_logs = preprocessing(sel_logs)

         # Prediction
        model_url = load_model_url()
        databricks_token = load_databricks_token()
        print(' pre prediction')
        prediction = forest_prediction(model_url, databricks_token, test_logs)
        sel_logs['prediction'] = prediction
        print(sel_logs.head())
      #  print("Target 1:" + str(sel_logs.prediction[sel_logs.prediction == 1].count())) 
      #  print("Target -1:" + str(sel_logs.prediction[sel_logs.prediction == -1].count())) 
      #  print(sel_logs["Id","Value","prediction",sel_logs.prediction == -1])
       # sel_logs_val = sel_logs[["IdBuilding","Id","Description","ValueType","Value"]][(sel_logs.prediction == -1) & (sel_logs.ValueType == "Wh") ]
       # print(sel_logs_val)
        st.dataframe(sel_logs)
      
    st.text("Oppure analizza i dati di test")
    if(st.button('Find Anomalies')):
        print('Button clicked!')
        feat_cols = ['Id', 'Value', 'Month','Weekday']
        
   
        # Create the Dataframe
        features = pd.DataFrame([row], columns = feat_cols)
        print('features',features)
        # Feature Engineering
      
       
        data = pd.DataFrame([row],columns = feat_cols)
        print(data)
        # Prediction
        model_url = load_model_url()
        databricks_token = load_databricks_token()
        print(' pre prediction')
        predictions = forest_prediction(model_url, databricks_token, data)
       # sel_logs['prediction'] = prediction
        print(predictions)
        data["Predizione"] = predictions
        st.text("Predizione:")
        st.dataframe(data)

