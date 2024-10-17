import requests
import json
import couchdb
import pandas as pd
from requests.auth import HTTPBasicAuth


def call_aurin_api(api_url):

    with open("config\\aurinInstance_details.json", 'r') as f:
        jsonData = json.load(f)

    response = requests.get(api_url, auth=HTTPBasicAuth(jsonData.user, jsonData.password))
    response_json = json.loads(response.content)
    return response_json

    