import json
import requests
import couchdb
import pandas as pd
from requests.auth import HTTPBasicAuth
from geopy.geocoders import Nominatim
import hashlib
from utils import getLiveability

def call_aurin_api(api_url):

    with open("config/aurinInstance_config.json", 'r') as f:
        jsonData = json.load(f)

    response = requests.get(api_url, auth=HTTPBasicAuth(jsonData['user'], jsonData['password']))

    #checking AURIN Api response
    if(response.status_code == 200):
        responseJson = json.loads(response.content)
    else:
        print ("Error " + response.status_code)
    return responseJson

def initialize_couchdb():

    with open('config/couchDB_config.json', 'r') as f:
        couchdbConfig = json.load(f)
        
    #initialize couch server
    couch = couchdb.Server(couchdbConfig['url'])  
    couch.resource.credentials = (couchdbConfig['user'] , couchdbConfig['password'])
    return couch

def remove_dot_column_name(df):
    df.columns=df.columns.str.replace('.','_')
    return df

def generate_id(s):
    return str(hashlib.sha256(s.encode()).hexdigest())

def get_location(address):
    try:
        geolocator = Nominatim(user_agent="test")
        location = geolocator.geocode(address)
        if((hasattr(location,'longitude') == False) or (hasattr(location,'latitude') == False)):
            return "Not Found"
        else:
            location_info = str(location.latitude) + "," + str(location.longitude)
            return location_info
    except:
        return "Not Found"

def update_couch_external(couch):
    print("Updating external tables")
    #school rank table
    df = pd.read_excel('data_files/Better_Education.xlsx',engine = 'openpyxl') #data from better education
    df['_id'] = df['School'].apply(generate_id) #renaming id as per couchdb standards
    df['location'] = df['School'].apply(get_location) #get location based on school names
    df['properties.lat'], df['properties.long'] = df['location'].str.split(',', 1).str
    df.drop('location', axis=1, inplace=True)
    df=remove_dot_column_name(df)
    out = df.to_json(orient='records')
    outJson = json.loads(out)
    db = couch['sch_rank'] 
    db.update(outJson) #updating database

    #no of hospital bed
    #data received from AURIN (API was not available)
    with open("data_files/my_hospital_beds.json", 'r') as f:
        jsonData = json.load(f)
    df = pd.json_normalize(jsonData['features'])
    df = df.drop('geometry.coordinates', 1)
    df = df.rename(columns={' id': '_id'})
    df = remove_dot_column_name(df)
    out = df.to_json(orient='records')
    outJson = json.loads(out)
    db = couch['health_no_beds']
    db.update(outJson)

    return 0

def update_postcode_bbox(couch,df):
    
    couchTable = 'postcode_bbox'
    db = couch[couchTable]
    df = df[['id','properties.geography_name','bbox']]
    df = df.loc[df.astype(str).drop_duplicates().index]
    df = df.rename(columns={'id': '_id','properties.geography_name':'post_code'})
    out = df.to_json(orient='records')
    outJson = json.loads(out)
        
    #update database
    db.update(outJson)

    return outJson

def update_postcode_ent(x,y,bbox_postcode):
    if x and y:
        for value in bbox_postcode:
            x_min = float(value['bbox'][0])
            y_min = float(value['bbox'][1])
            x_max = float(value['bbox'][2])
            y_max = float(value['bbox'][3])
        
            if ((x_min <= float(x) <= x_max) and (y_min <= float(y) <= y_max)):
                return value['post_code']
    return "Null"




def update_couch_tables():

    with open("config/aurinAPI_list.json", 'r') as f:
        aurinApiList = json.load(f)

    #initialize couch server
    couch = initialize_couchdb()

    #update from external files
    update_couch_external(couch)

    for api in aurinApiList:
        print("Updating aurin tables")
        #Dataset
        db = couch[api]
        dataAurin = call_aurin_api(aurinApiList[api])
        df = pd.json_normalize(dataAurin['features'])
        
        #initial preprocessing
        if(api == 'housing_rent_aff'):
            df = df.loc[df['properties.state'] == 'VIC']
            #update bbox data for each postcode
            bbox_postcode=update_postcode_bbox(couch,df)

        if(api == 'env_pollutant'):
            df = df.loc[df['properties.state'] == 'VIC']
            df.rename(columns = {'properties.latitude':'properties.lat', 'properties.longitude':'properties.long'}, inplace = True)

        if(api == 'ent_cafe_seating'):
            df.rename(columns = {'properties.y_coordinate':'properties.lat', 'properties.x_coordinate':'properties.long'}, inplace = True)
            df['post_code'] = df.apply(lambda x: update_postcode_ent(x["properties.long"], x["properties.lat"],bbox_postcode), axis=1)

        if(api == 'ent_bar_seating'):
            df.rename(columns = {'properties.y_coordinate':'properties.lat', 'properties.x_coordinate':'properties.long'}, inplace = True)
            df['post_code'] = df.apply(lambda x: update_postcode_ent(x["properties.long"], x["properties.lat"],bbox_postcode), axis=1)
        
        if(api == 'ent_sports'):
            df.rename(columns = {'properties.latitude':'properties.lat', 'properties.longitude':'properties.long'}, inplace = True)

        if(api == 'ent_car_park'):
            df.rename(columns = {'properties.y_coordinate':'properties.lat', 'properties.x_coordinate_2':'properties.long'}, inplace = True)
            df['post_code'] = df.apply(lambda x: update_postcode_ent(x["properties.long"], x["properties.lat"],bbox_postcode), axis=1)
        
        
        


        df = df.drop('geometry.coordinates', 1)
        df = df.rename(columns={'id': '_id'})
        df = remove_dot_column_name(df)
        out = df.to_json(orient='records')
        outJson = json.loads(out)
        
        #update database
        db.update(outJson)
    getLiveability.getLiveability() #calculating liveability score

    return 0