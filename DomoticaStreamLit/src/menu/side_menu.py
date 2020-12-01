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
    
    CO2 =                        st.sidebar.slider("CO2", 1, 15000, 25, 1)
    Gradi =                      st.sidebar.slider("Gradi", -10, 50, 20, 1)
    umidita =                    st.sidebar.slider("%_umidità", 0, 200, 25, 1)
    produzione_fotovoltaico =    st.sidebar.slider("produzione fotovoltaico", 0, 10000, 5000, 100)
    consumo_energetico =         st.sidebar.slider("consumo energetico", 0, 10000, 2000, 100)
   
   
    
    row = [CO2, Gradi, umidita, produzione_fotovoltaico, consumo_energetico]
   # row = [age,sex,cp,trestbps,chol]
    today =  datetime.date.today()
    st.date_input("Selziona data di test", today)
    st.text("Oppure carica dati da db azure")
    day = today.weekday()
    print("day:", day )
    mese = today.month
    print("mese:", mese )
    row_co2 = [CO2,1,mese,day]

    if (st.button('Carica Dati da DataBase')):
        # Carico i dati dal database
        df_log = load_azure_data()        
        df_group = load_local_group()
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
        print("Target 1:" + str(sel_logs.prediction[sel_logs.prediction == 1].count())) 
        print("Target 0:" + str(sel_logs.prediction[sel_logs.prediction == -1].count())) 
        print(sel_logs["Id","Value","prediction",sel_logs.prediction == -1])
        #print(sel_logs.head())

      

    if(st.button('Find Anomalies')):
        print('Button clicked!')
        feat_cols = ['Value', 'Id', 'Month','Weekday']
        
   
        # Create the Dataframe
        features = pd.DataFrame([row_co2], columns = feat_cols)
        print('features',features)
        # Feature Engineering
      
       
        data = pd.DataFrame([row_co2],columns = feat_cols)
        print(data)
        # Prediction
        model_url = load_model_url()
        databricks_token = load_databricks_token()
        print(' pre prediction')
        predictions = forest_prediction(model_url, databricks_token, data)
       # sel_logs['prediction'] = prediction
        print(predictions)
        #print(sel_logs.head())

