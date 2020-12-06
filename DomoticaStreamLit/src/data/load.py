import logging
import os
#import request
import pandas as pd
import pyodbc

def connect_azure_database():
    # Funzione che crea una connessione con il database SQL CampusData presente nella sottoscrizione di Microsoft Azure
    try:
        conn = pyodbc.connect(
            r'Driver={ODBC Driver 17 for SQL Server};'
            r'Server=tcp:aiengserver.database.windows.net,1433;'
            r'Database=CampusData;Uid=AzureUser;Pwd=PasswordReti01;Encrypt=yes'
        )
        return conn
    except pyodbc.Error as err: # Only error I wanted passed for the test!
        logging.warn(err)


def load_azure_data(sql = "SELECT * FROM dbo.Log_newData"):
    # Funzione che si connette al database SQL CampusData presente in Microsoft Azure e restituisce un DataFrame pandas  
    # sulla base della query passata come input
    try:    
        conn = connect_azure_database()       
        data = pd.read_sql(sql,conn)
        return data
    except:
        #raise ValueError('Error pd.read_sql')
        logging.warn('Error pd.read_sql')


def load_model_url():
    # Funzione che carica l'URL del modello Isolation Forest salvato in Databricks
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/Iso_Forest_Project/1/invocations"

def load_modelurl_CO2():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'ppm'
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/model_team1_CO2/Production/invocations"

def load_modelurl_temperatura():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'C°'
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/model_team1_temperatura/Production/invocations"

def load_modelurl_umidita():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in '%'
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/model_team1_umidita/Production/invocations"


def load_modelurl_W():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'W'
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/model_team1_W/Production/invocations"


def load_modelurl_Wh():
    # Restituisce l'URL per la chiamata del modello salvato in Databricks addestrato su rilevazioni in 'Wh'
    return "https://adb-5873545433774891.11.azuredatabricks.net/model/model_team1_Wh/Production/invocations"

def load_databricks_token():
    # Funzione che carica il token per la connessione a DataBricks
    return "dapi9d493adb582d4a93953ce7a2d790b9d6"

def load_local_group():
    # Import sklearn pickle objects from training pipeline (model and feature eng pipelines)
   # folder_path = os.path.abspath(".")
    datasets_path = os.path.abspath("..")

    group_object_path = os.path.join(datasets_path,"datasets" ,"group.csv")

    print(f"group_object_path: {group_object_path}")

    object_result = pd.read_csv(group_object_path, encoding= 'unicode_escape')

    return object_result