import logging
import os
#import request
import pandas as pd
import pyodbc
import pickle


def connect_azure_database():
    # Funzione che crea una connessione con il database SQL CampusData presente nella sottoscrizione di Microsoft Azure
    try:
        conn = pyodbc.connect(
            r'Driver={ODBC Driver 17 for SQL Server};'
            r'Server=tcp:aiengineerserver.database.windows.net,1433;'
            r'Database=CampusData;Uid=AzureUser;Pwd=PasswordReti01;Encrypt=yes'
        )
        return conn
    except pyodbc.Error as err: # Only error I wanted passed for the test!
        logging.warn(err)


#def load_azure_data(sql = "SELECT * FROM dbo.Log_newData"):
def load_azure_data(sql = "SELECT * FROM dbo.log_newData"):
    # Funzione che si connette al database SQL CampusData presente in Microsoft Azure e restituisce un DataFrame pandas  
    # sulla base della query passata come input
    try:    
        conn = connect_azure_database()       
        data = pd.read_sql(sql,conn)
        return data
    except:
        #raise ValueError('Error pd.read_sql')
        logging.warn('Error pd.read_sql')


def load_local_building():
     # Funzione che carica il file "building.csv" salvato in locale nella cartella di progetto "datasets"
     path = os.path.join(os.path.abspath('.'),'datasets', 'building.csv')
     df_building = pd.read_csv(path, sep=',', encoding='cp1252')
     return df_building


def load_local_group():    
    # Funzione che carica il file "group.csv" salvato in locale nella cartella di progetto "datasets"
    path = os.path.join(os.path.abspath('.'),'datasets', 'group.csv')
    df_group = pd.read_csv(path, sep=',', encoding='cp1252')
    return df_group


def load_local_log():
    # Funzione che carica il file "log2.csv" salvato in locale nella cartella di progetto "datasets"
    path = os.path.join(os.path.abspath('.'),'datasets', 'log2.csv')
    df_log = pd.read_csv(path, sep=';', encoding='cp1252')
    return df_log


def load_model_url():
    # Funzione che carica l'URL del modello Isolation Forest salvato in Databricks
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/Iso_Forest_Project/1/invocations"


def load_databricks_token():
    # Funzione che carica il token per la connessione a DataBricks
    return "dapi36147c32e3c159bff19c1e3d1195baef-2"


def load_modelurl_CO2():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'ppm'
    return "https://adb-1383651973845496.16.azuredatabricks.net/model/team1_CO2/1/invocations"


def load_modelurl_temperatura():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'C°'
    return "https://adb-1383651973845496.16.azuredatabricks.net/model/team1_temperatura/1/invocations"


def load_modelurl_umidita():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in '%'
    return "https://adb-1383651973845496.16.azuredatabricks.net/model/team1_umidita/1/invocations"


def load_modelurl_W():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'W'
    return "https://adb-1383651973845496.16.azuredatabricks.net/model/team1_W/1/invocations"


def load_modelurl_Wh():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'Wh'
    return "https://adb-1383651973845496.16.azuredatabricks.net/model/team1_Wh/1/invocations"


# Funzioni per il caricamento dei modelli di backup in formato pickle

def load_model_pickle_CO2():
    path_model = os.path.join(os.path.abspath('.'), 'TeamLibraries', 'model_pickle_CO2.pkl')
    model = pickle.load(open(path_model, 'rb'))
    return model

def load_model_pickle_temperatura():
    path_model = os.path.join(os.path.abspath('.'), 'TeamLibraries', 'model_pickle_temperatura.pkl')
    model = pickle.load(open(path_model, 'rb'))
    return model

def load_model_pickle_umidita():
    path_model = os.path.join(os.path.abspath('.'), 'TeamLibraries', 'model_pickle_umidita.pkl')
    model = pickle.load(open(path_model, 'rb'))
    return model

def load_model_pickle_W():
    path_model = os.path.join(os.path.abspath('.'), 'TeamLibraries', 'model_pickle_W.pkl')
    model = pickle.load(open(path_model, 'rb'))
    return model

def load_model_pickle_Wh():
    path_model = os.path.join(os.path.abspath('.'), 'TeamLibraries', 'model_pickle_Wh.pkl')
    model = pickle.load(open(path_model, 'rb'))
    return model