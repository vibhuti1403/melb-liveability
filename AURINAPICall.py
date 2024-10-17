import requests
from requests.auth import HTTPBasicAuth
response = requests.get(
  'http://openapi.aurin.org.au/wfs?version=1.1.0&request=GetFeature&typeNames=aurin:datasource-VIC_Govt_DET-UoM_AURIN_DB_vic_det_school_zone_primary_2020&outputFormat=json', 
  auth=HTTPBasicAuth('student', 'password')
)

print(response)