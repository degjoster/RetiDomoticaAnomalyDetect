import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import TeamLibraries.LoadData as tld
import TeamLibraries.ModelFunctions as tmf

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest

import requests
import os


if __name__ == "__main__":

    # Carico i dati salvati in locale
    df_log = tld.load_azure_data()        
    #df_log = tld.load_local_log()
    df_group = tld.load_local_group()
    
    # Carico i dati dal database
        
    # Seleziono i log che possono essere oggetto di predizione nel modello
    sel_logs = tmf.signals_selection(df_log, df_group)
        
    # Effettuo il preprocessing dei log selezionati, ricavando le features necessarie all'Anomaly Detection
    # tramite il modello
    test_logs = tmf.preprocessing(sel_logs)
    
    # Carico il token di DataBricks e l'URL del modello per l'invio della richiesta
    databricks_token = tld.load_databricks_token()
    model_url = tld.load_modelurl_umidita()
    
    # Effettuo la predizione attraverso il modello
    prediction = tmf.forest_prediction(model_url, databricks_token, test_logs)
    sel_logs['prediction'] = prediction
    print(sel_logs.head())