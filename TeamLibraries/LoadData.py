import logging
import os
#import request
import pandas as pd
import pyodbc

cnxn = pyodbc.connect(r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:aiengserver.database.windows.net,1433;Database=CampusData;Uid=AzureUser;Pwd=PasswordReti01;Encrypt=yes')

sql = "SELECT  * FROM dbo.Log_newData"
data = pd.read_sql(sql,cnxn)
print(data.head())



