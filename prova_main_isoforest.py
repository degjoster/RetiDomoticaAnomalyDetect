import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest

if __name__ == "__main__":
    
    # Lettura dei dati (da inserire in apposite funzioni nella cartella "TeamLibraries")
    df_building = pd.read_csv('datasets/building.csv', sep=',', encoding='cp1252');
    df_group = pd.read_csv('datasets/group.csv', sep=',', encoding='cp1252')
    df_log = pd.read_csv('datasets/log2.csv', sep=';', encoding='cp1252')
    
    #prova head
    print(df_log.head())
    