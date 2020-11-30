import logging
import os
#import request
import pandas as pd
import pyodbc

# Funzione che tramite la stringa di connessione crea una connessione con il database CampusData su azure
def get_database():
    try:
        conn = pyodbc.connect(
            r'Driver={ODBC Driver 17 for SQL Server};'
            r'Server=tcp:aiengserver.database.windows.net,1433;'
            r'Database=CampusData;Uid=AzureUser;Pwd=PasswordReti01;Encrypt=yes'
        )
        return conn
    except pyodbc.Error as err: # Only error I wanted passed for the test!
        logging.warn(err)

# Funzione che restituisce un dataset pandas che rappresenta la query passata come argomento
def getDatasetByDB(sql = "SELECT * FROM dbo.Log_newData"):
    try:    
        conn = get_database()       
        data = pd.read_sql(sql,conn)
        return data
    except:
        #raise ValueError('Error pd.read_sql')
        logging.warn('Error pd.read_sql')

#data = getDatasetByDB()
#print(data.head(100))


