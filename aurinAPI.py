import requests
import json
import couchdb
from requests.auth import HTTPBasicAuth 

#AURIN API URLs
#Housing
housingRentAff = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-SGSEP-UoM_AURIN_DB_sgs_rai_index_national_total_2021&outputFormat=json'

#Environment
envGreenSpace = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-AU_Govt_DEE-UoM_AURIN_DB_national_pollutant_inventory_facilities_2018&outputFormat=json'

#School
schZoneSenSec = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_senior_secondary_college_2020&outputFormat=json'
schZonePri = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_primary_2020&outputFormat=json'
schZone7 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year7_2020&outputFormat=json'
schZone8 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year8_2020&outputFormat=json'
schZone9 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year9_2020&outputFormat=json'
schZone10 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year10_2020&outputFormat=json'
schZone11 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year11_2020&outputFormat=json'
schZone12 = 'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_secondary_year12_2020&outputFormat=json'
schZonePrep = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_prep_junior_secondary_2020&outputFormat=json'
LGAProfile = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DHHS-UoM_AURIN_DB_vic_govt_dhhs_lga_profiles_2015&outputFormat=json'

#Hospital Not Working - Invalid
hospNoBeds = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-NHPA-UoM_AURIN_DB_UNSW_CFRC_NHPA_my_hospital_beds&outputFormat=json'

#Entertainment
entCafeSeating = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_LGovt_COM-UoM_AURIN_DB_com_clue_cafe_restaurant_bistro_seats_2017&outputFormat=json'
entBarSeating = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_LGovt_COM-UoM_AURIN_DB_com_clue_bars_pubs_patron_capacity_2017&outputFormat=json'
entSports = 'https://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DHHS-UoM_AURIN_DB_vic_sport_and_recreation_2015&outputFormat=json'

#aminities
amtCarPark = 'https://data.aurin.org.au/dataset/vic-lgovt-com-com-clue-offstreet-car-parking-2017-na'

def call_aurin_api(api_url):
    response = requests.get(api_url, auth=HTTPBasicAuth('student', 'dj78dfGF'))
    response_json = json.loads(response.content)
    return response_json
    
def create_couch_tables():
    
    #initialize couch server
    couch = couchdb.Server('http://user:user@localhost:5984')
    
    #Housing Dataset
    db = couch.create('rent_affordability')
    data_aurin = call_aurin_api(housingRentAff)
    db.save(data_aurin)
    
    #Environment Dataset
    db = couch.create('env_greenspace')
    data_aurin = call_aurin_api(envGreenSpace)
    db.save(data_aurin)
    
    #School Dataset
    db = couch.create('school_zone_seniorsec')
    data_aurin = call_aurin_api(schZoneSenSec)
    db.save(data_aurin)
    
    db = couch.create('school_zone_pri')
    data_aurin = call_aurin_api(schZonePri)
    db.save(data_aurin)
    
    db = couch.create('school_zone_7')
    data_aurin = call_aurin_api(schZone7)
    db.save(data_aurin)
    
    db = couch.create('school_zone_8')
    data_aurin = call_aurin_api(schZone8)
    db.save(data_aurin)
    
    db = couch.create('school_zone_9')
    data_aurin = call_aurin_api(schZone9)
    db.save(data_aurin)
    
    db = couch.create('school_zone_10')
    data_aurin = call_aurin_api(schZone10)
    db.save(data_aurin)
    
    db = couch.create('school_zone_11')
    data_aurin = call_aurin_api(schZone11)
    db.save(data_aurin)
    
    db = couch.create('school_zone_12')
    data_aurin = call_aurin_api(schZone12)
    db.save(data_aurin)
    
    db = couch.create('school_zone_prep')
    data_aurin = call_aurin_api(schZonePrep)
    db.save(data_aurin)
    
    #LGA Profile
    db = couch.create('lga_profile')
    data_aurin = call_aurin_api(LGAProfile)
    db.save(data_aurin)
    
    #Environment
    db = couch.create('ent_cafe_seating')
    data_aurin = call_aurin_api(entCafeSeating)
    db.save(data_aurin)
    
    db = couch.create('ent_bar_seating')
    data_aurin = call_aurin_api(entBarSeating)
    db.save(data_aurin)
    
    db = couch.create('ent_sports')
    data_aurin = call_aurin_api(entSports)
    db.save(data_aurin)
    
    #aminities
    db = couch.create('amt_car_park')
    data_aurin = call_aurin_api(amtCarPark)
    db.save(data_aurin)