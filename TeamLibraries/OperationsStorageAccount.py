import os, uuid
import pandas as pd
import datetime
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# Funzione che salva su storage account BLOB CONTINER un file BLOB (in questo caso .JSON)
# In input richiede obbligatoriamente un dataframe pandas da salvare che poi verrà convertito in formato JSON
# Come parametro opzionale il nome del continer su cui salvare i file.
# La funzione restituisce True se tutto è andato a buon fine e False se qualcosa non è andato bene
def saveJsonStorageAccountFromDataframe(df, container_name = "predictcontainerdomoticaad"):
    try:
        #connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        connect_str = "DefaultEndpointsProtocol=https;AccountName=sorageaccountgdeiana;AccountKey=UL8Q31FdBG/jlwDSMds4bgXYn6eQBIpwJ54uN6CjuMxtA8rNAwThZaJdilWE6Wfi6RIrrnJlTYbjH9T4bcsbyQ==;EndpointSuffix=core.windows.net"
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Controllo se il container è già presente e se non esiste lo crea
        existingContiner = False
        for container in blob_service_client.list_containers():
            if container_name == container['name']:
                existingContiner = True
        if existingContiner:
            #Comando per recuperare l'istanza in locale del continer esistente
            container_client = blob_service_client.get_container_client(container_name)
        else:
            #Comando per creare un nuovo container
            container_client = blob_service_client.create_container(container_name)

        #Creo il timestamp per il file da caricare
        utc_timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

        #Creo un dump del file senza salvarlo
        PredictionContentJson = json.dumps(df.to_json(orient="records"))

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"prediction_{utc_timestamp}.json")

        # Carico dump su storage account
        blob_client.upload_blob(PredictionContentJson)
    
    except Exception as ex:
        print('Exception:')
        print(ex)
        return False

    return True