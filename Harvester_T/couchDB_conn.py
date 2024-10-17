import couchdb
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('.envdb')
load_dotenv(dotenv_path=str(dotenv_path))



class CouchConnector:
    def __init__(self,table):
        dbuser = os.getenv("DBuser")
        dbpwd = os.getenv("DBpwd")
        dburl = os.getenv("DBurl")


        couch = couchdb.Server(dburl)   
        couch.resource.credentials = (dbuser , dbpwd)

        self.db = couch[table]


