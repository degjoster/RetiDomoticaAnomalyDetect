import os, uuid
import pandas as pd
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# Funzione che restituisce un'istanza di BlobServiceClient tramite la stringa di connessione
def getBlobServiceClientByConnectionString():
    try:
        connect_str = "DefaultEndpointsProtocol=https;AccountName=storageaccountprogteam1;AccountKey=uJFo5/ibPFsUqCUgXXxL7Uj1GWSAN8SG89fcv71SDwdobTnu0V4Eg52XX3nUgDDwV/50U9WzyTElNKHeJ5Yo7A==;EndpointSuffix=core.windows.net"    
        #Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    except Exception as ex:
        print('Exception:')
        print(ex)
        pass  
    
    return blob_service_client
  
# Funzione che restituisce una lista di nomi dei continer presenti in Storage Account
# Utilizzabile per far decidere all'utente su che container salvare la predizione oppure da vove prenderla
def getNameContainerList():
    try:
        blob_service_client = getBlobServiceClientByConnectionString()
        listNameContainers = []
        for container in blob_service_client.list_containers():
            listNameContainers.append(container['name'])
    except Exception as ex:
        print('Exception:')
        print(ex)
        pass
    return listNameContainers

# Funzione che restituisce una lista di nomi dei file blob presenti in uno specifico container dello Storage Account
# Utilizzabile per far decidere all'utente su che file blob salvare o caricare la predizione.
def getNameBlobList(container_name):
    try:
        blob_service_client = getBlobServiceClientByConnectionString()
        container_name_lower = container_name.lower()
        container_client = blob_service_client.get_container_client(container_name_lower)
        blob_list = container_client.list_blobs()
        listNameBlob = []
        for blob in blob_list:
            listNameBlob.append(blob.name)     
    except Exception as ex:
        print('Exception:')
        print(ex)
        pass
    return listNameBlob     

# Funzione che permette di recuperare dallo Storage Account la predizione indicata tramite i parametri
# Questa viene salvata nella cartella locale DataLocalPrediction
# Se la predizione json è già presente nella cartella locale, questa viene sempre sovrascritta. 
def saveLocalJsonPredictionFromStorageAccount(container_name, blob_name):
    try:
        # Create a file in local data directory to upload and download
        blob_service_client = getBlobServiceClientByConnectionString()
        container_name_lower = container_name.lower()
        blob_client = blob_service_client.get_blob_client(container=container_name_lower, blob=blob_name)
        local_path = "dataLocalPrediction"
        local_file_name = blob_name
        local_file_path_download = os.path.join(os.path.abspath('..'),local_path, local_file_name)
    
        with open(local_file_path_download, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
    except Exception as ex:
        print('Exception:')
        print(ex)
        return False
    
    return True

# Funzione che salva su Storage Account BLOB CONTAINER un file BLOB (in questo caso .JSON)
# In input richiede obbligatoriamente un dataframe pandas da salvare che poi verrà convertito in formato JSON
# Come primo parametro opzionale richiede il nome del container in cui salvare i file.
# Come secondo parametro opzionale richiede il nome dell'unità di misura per inserirlo nel nome del file blob JSON.
# Il nome del Container deve essere in minuscolo perchè Azure storage account proibisce i cacatteri maiuscoli
# La funzione restituisce True se tutto è andato a buon fine e False se qualcosa non è andato bene
def saveJsonStorageAccountFromDataframe(df, container_name = "predictcontainerdomoticaad", unita_misura = "general"):
    try:
        blob_service_client = getBlobServiceClientByConnectionString()
        # Azure storage accetta solo container in minuscolo
        container_name_lower = container_name.lower()
        unita_misura_lower = unita_misura.lower()

        # Controllo se il container è già presente e se non esiste lo crea
        existingContiner = False
        for container in blob_service_client.list_containers():
            if container_name_lower == container['name']:
                existingContiner = True  
        if not existingContiner:
            container_client = blob_service_client.create_container(container_name_lower)
        
        #Creo il timestamp per il file da caricare
        utc_timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        
        #Creo un dump del file senza salvarlo
        PredictionContentJson = df.to_json(orient="records")
        
        # Creo blob client con nome univoco. Il file non è locale ma dumpato
        blob_client = blob_service_client.get_blob_client(container=container_name_lower, blob=f"prediction_{utc_timestamp}-{unita_misura_lower}.json")
        
        # Carico dump su storage account
        blob_client.upload_blob(PredictionContentJson)
        
    except Exception as ex:
        print('Exception:')
        print(ex)
        return False

    return True