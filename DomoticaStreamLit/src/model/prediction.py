import requests


def forest_prediction(model_url, databricks_token, data):
    # Funzione che effettua la predizione sui dati richiamando il modello Isolation Forest
    # versionato in DataBricks
    
    headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json; format=pandas-records",
    }
    
    data_json = data if isinstance(data, list) else data.to_dict(orient="records")
    response = requests.request(method='POST', headers=headers, url=model_url, json=data_json)
    
    #if response.status_code != 200:
    #  raise Exception(f"Request failed with status {response.status_code}, {response.text}")
    return response.json()