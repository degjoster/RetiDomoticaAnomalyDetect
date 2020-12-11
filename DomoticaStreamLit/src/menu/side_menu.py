import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import requests
import altair as alt

from ..data.load import load_azure_data
from ..data.load import load_model_url
from ..data.load import load_modelurl_CO2
from ..data.load import load_modelurl_temperatura
from ..data.load import load_modelurl_umidita
from ..data.load import load_modelurl_W
from ..data.load import load_modelurl_Wh
from ..data.load import load_databricks_token
from ..data.load import load_local_group
from ..data.load import load_sklearn_object
from ..features.transform  import signals_selection
from ..features.transform import preprocessing

from ..model.prediction import forest_prediction
from ..model.prediction import prediction_pkl
from ..save.OperationsStorageAccount import saveJsonStorageAccountFromDataframe
#
#from sklearn.preprocessing import LabelEncoder
#from sklearn.ensemble import IsolationForest

def start_side_menu():
    st.sidebar.title("Scegliere Edificio e Descrizione")
    value = st.sidebar.radio("Scegli luogo",("Edificio1","Edificio3","Villa"))

    if value == "Edificio1":
        EId = 1
    elif value == "Edificio3":
        EId = 5
    elif value == "Villa":
        EId = 6

    ####Lettura di group.csv per la generazione di una selectbox per selezionare la misura da testare
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
    Id_descr = st.sidebar.selectbox('Scegli una Descrizione', options, format_func=lambda x: dic[x])
    valueType = df_selectbox["ValueType"][df_selectbox.Id == Id_descr].values
   
    st.sidebar.title("Scegliere valori e data da testare")
    if valueType == 'ppm':
        value_measure =         st.sidebar.slider("CO2 in ppm", 0, 50000, 25, 1)
    elif valueType == 'C°':
        value_measure =         st.sidebar.slider("Gradi in C°", -20, 100, 20, 1)
    elif valueType == '%':
        value_measure =         st.sidebar.slider("%_umidità", 0, 100, 25, 1)
    elif valueType == 'W':
        value_measure =         st.sidebar.slider("produzione fotovoltaico in W", 0, 100000, 5000, 100)
    elif valueType == 'Wh':
        value_measure =         st.sidebar.slider("consumo energetico in Wh", 0, 30000, 2000, 100)
  
   
    ####Creazione calendario
    today =  datetime.date.today()
    day_calendar = st.sidebar.date_input("Selziona data di test", today)
    st.header("Carica dati da db azure")
    day = day_calendar.weekday()
    print("day:", day )
    mese = day_calendar.month
    print("mese:", mese )

    #### array di valori da usare nella funzione "predizione"
    row = [Id_descr,value_measure,mese,day]

    ####Caricamento del modello da usare per la predizione
    if valueType == 'ppm':
        model_url = load_sklearn_object("model_pickle_CO2.pkl")
    elif valueType == 'C°':
        model_url = load_sklearn_object("model_pickle_temperatura.pkl")
    elif valueType == '%':
        model_url = load_sklearn_object("model_pickle_umidita.pkl")
    elif valueType == 'W':
        model_url = load_sklearn_object("model_pickle_W.pkl")
    elif valueType == 'Wh':
        model_url = load_sklearn_object("model_pickle_Wh.pkl")

    
    #####
    #####Carico dati da DB Azure
    
    ####
    ####Funzione per effettuare predizione dei dati scricati da Db
    ####
    def predizione_db():
        # Carico i dati dal database
        df_log = load_azure_data()        
       
        # Seleziono i log che possono essere oggetto di predizione nel modello
        sel_logs = signals_selection(df_log, df_group)
        
        # Effettuo il preprocessing dei log selezionati, ricavando le features necessarie all'Anomaly Detection
        # tramite il modello
        print(Id_descr )
        db_logs = sel_logs[sel_logs.Id == Id_descr]
        print(db_logs.head())
        test_logs = preprocessing(db_logs)
        
        # Prediction
        # model_url = load_model_url()
        databricks_token = load_databricks_token()
        print(' pre prediction')
        print(test_logs)
        #if valueType == 'ppm':
        #    prediction = forest_prediction(model_url, databricks_token, test_logs)
        #else:
        
        prediction = prediction_pkl(model_url, test_logs)

        db_logs['prediction'] = prediction
        print(db_logs.head())
        #stampo a video il dataset con l'aggiunta della colonna "prediction"
        st.dataframe(db_logs)
        
        return db_logs
    ##Bottone per visualizzare a video il dataset con la predizione
    if (st.button('Carica Dati da DB scegliendo Edificio e Descrizione')):
        data = predizione_db()

        '''data['DataDay'] = pd.to_datetime(data['Data'], unit='ms').dt.dayofyear
        chartAltair = alt.Chart(data).mark_point(filled=True).encode(
          x='DataDay:O',
          y='Value:Q',
          color=alt.condition('datum.prediction < 0', alt.ColorValue('red'), alt.ColorValue('lightblue'))
        ).properties(
         width=750,
         height=300
        ).configure_point(
         size=50
        )'''
        
        massimo = data['Value'].max()
        minimo = data['Value'].min()
        chartAltair = alt.Chart(data).mark_point(filled=True).encode(
            alt.X('Data:T'),
            alt.Y('Value:Q',scale=alt.Scale(domain=(minimo, massimo))),
            color=alt.condition('datum.prediction < 0', alt.ColorValue('red'), alt.ColorValue('lightblue'))
        ).properties(
            width=750,
            height=300
        ).configure_point(
            size=20
        )
        
        st.altair_chart(chartAltair)

    ##Bottone per salvare su azure storage il dataset con la predizione in formato json
    if (st.button('Carica Dati da DB di "Edificio e Descrizione" e salva predizione su DB')):
        db_logs = predizione_db()
        print ("valuetype", valueType)
        s_valueType = valueType[0]
        result = saveJsonStorageAccountFromDataframe(db_logs,"predictcontainerdomoticaadsqldb",s_valueType) 
        print ("rislutato salvataggio", result)
        if (result):
            st.text("Predizione salvata") 
        else:
            st.text("Problemi con il salvataggio")     



    ####
    ####Funzione per effettuare predizione dei dati inseriti dall'utente
    ####
    def predizione():    
        print('Button clicked!')
        feat_cols = ['Id', 'Value', 'Month','Weekday']
        
   
        # Create the Dataframe
        features = pd.DataFrame([row], columns = feat_cols)
        print('features',features)
        # Feature Engineering
      
       
        data = pd.DataFrame([row],columns = feat_cols)
        print(data)

        #model_url = load_modelurl_temperatura()
        databricks_token = load_databricks_token()

         # Prediction
        print(' pre prediction')
        #if valueType == 'ppm':
        #    prediction = forest_prediction(model_url, databricks_token, data)
        #else:
        prediction = prediction_pkl(model_url, data)

       # sel_logs['prediction'] = prediction
        print(prediction)
        data["Predizione"] = prediction
        st.text("Predizione:")
        st.dataframe(data)
        if prediction[0] == 1:
            st.text("I valori inseriti non producono anomalia")
        else:
            st.text("'ATTENZIONE!' I valori inseriti generano un'anomalia") 
        return data

    st.header("Oppure analizza i dati di test")
    if(st.button('Effettua predizione')):
        data = predizione()

    if(st.button('Effettua predizione e salva su azure')):
        data = predizione()
        print ("valuetype", valueType)
        s_valueType = valueType[0]
        result = saveJsonStorageAccountFromDataframe(data,"predictcontainerdomoticaaduser",s_valueType)
        print ("rislutato salvataggio", result),
        if (result):
            st.text("Predizione salvata")   
        else:
            st.text("Problemi con il salvataggio")   
    