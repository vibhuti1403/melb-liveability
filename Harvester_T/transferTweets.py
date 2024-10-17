from couchDB_conn import CouchConnector
import requests
import setup
from dotenv import load_dotenv
from pathlib import Path
import os
import json

dbobj = CouchConnector(setup.tweetsdbname)
real_dbobj = CouchConnector(setup.realtime_tweetsdbname)

dotenv_path = Path('.envdb_api')
load_dotenv(dotenv_path=str(dotenv_path))

dbuser = os.getenv("DBuser")
dbpwd = os.getenv("DBpwd")
dburl = os.getenv("DBurl")

url = "http://" + dbuser +":"+dbpwd +"@" + dburl.split("http://")[1]+"/realtime_tweets/_all_docs?include_docs=true"
response = requests.request("GET", url)
response_json = json.loads(response.text)

docs = []
for row in response_json['rows']:
    doc = row['doc']
    doc['_deleted'] = True
    docs.append(doc)

dbobj.db.update(response_json['rows'])
real_dbobj.db.update(docs)


