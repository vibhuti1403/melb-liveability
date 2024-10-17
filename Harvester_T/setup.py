from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=str(dotenv_path))

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

bearer_token = os.getenv('Bearer_Token')
geo = os.getenv("geoCode")
jsonfile = os.getenv("jsonfile")
csvfile = os.getenv("csvfile")
category=os.getenv("categories")

dbuser = os.getenv("DBuser")
dbpwd = os.getenv("DBpwd")
tweetsdbname = os.getenv("tweetsdbname")
archived_dbname = os.getenv("archived_dbname")
bulk_dbname = os.getenv("bulk_dbname")
realtime_tweetsdbname = os.getenv("realtime_tweetsdbname")


xmin = float(os.getenv("melb_bb_x_min"))
ymin = float(os.getenv("melb_bb_y_min"))
xmax = float(os.getenv("melb_bb_x_max"))
ymax = float(os.getenv("melb_bb_y_max"))
