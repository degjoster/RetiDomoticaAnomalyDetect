import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest


def signals_selection(logs, groups):
    # Funzione che rimuove le rilevazioni di tipo boolean, quelle non mappate nel dataset "group" e quelle che non presentano un valore nei
    # campi "Data", "Value" e "Id". Restituisce un dataframe di segnali che saranno effettivamente preprocessati e passati
    # come input al modello per l'addestramento o la predizione
    
    # Unità di misura da tenere e tipologie di rilevazioni da rimuovere
    measures_to_keep = ['ppm', 'C°', '%', 'W', 'Wh']
    description_to_remove = ['Daikin Active Power Total','Consumo enel di E1 + Villa']
    
     # Rimuovo i record associati a rilevazioni di tipo booleano
    logs = logs[logs['ValueType'].isin(measures_to_keep) == True]
    
    # Rimuovo i record associati a rilevazioni di tipo "Daikin Active Power Total" e "Consumo Enel di E1 + Villa"
    logs = logs[logs['Description'].isin(description_to_remove) == False]
    
    # Effettuo il left join con la tabella group per ricavare l'ID della rilevazione
    logs = logs.merge(groups[['Description', 'Id']], how='left', on='Description')
    logs = logs.dropna(subset=['Data', 'Id', 'Value']).reset_index(drop=True)
    
    # Converto la colonna 'Data' in formato datetime
    logs['Data'] = pd.to_datetime(logs['Data'])
    
    # Converto la colonna 'Value' in formato numerico
    logs["Value"] = pd.to_numeric(np.char.replace(logs['Value'].to_numpy().astype(str),',','.'))
    
    return logs


def preprocessing(sel_logs):
    # Funzione che rimuove le features non inerenti all'addestramento/predizione del modello e ricava le features riguardanti
    # il mese e il giorno della settimana di ciascuna rilevazione
    
    # Ricavo il mese e il giorno della settimana della rilevazione
    sel_logs['Month'] = pd.DatetimeIndex(sel_logs['Data']).month
    sel_logs['Weekday'] = pd.DatetimeIndex(sel_logs['Data']).weekday
    
    # 3) Rimuovo le features che non servono ad addestrare il modello
    features_to_drop = ['Data', 'IdBuilding', 'IndividualAddress', 'GroupAddress', 'TelegramType', 'ValueType', 'Description']
    sel_logs = sel_logs.drop(columns=features_to_drop)   
    print(sel_logs.head())
    return sel_logs

def forest_train(train_logs, num_est=100, cnt_rate=0.01):
    # Funzione che addestra il modello sulla base dei log preprocessati e degli iperparametri passati in ingresso
    iso_forest = IsolationForest(n_estimators=num_est, random_state=19, contamination=cnt_rate, 
                                 behaviour='deprecated').fit(train_logs)
    
    return iso_forest