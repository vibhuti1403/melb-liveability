from couchdb.design import ViewDefinition
import requests
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import copy
import couchdb

def getBedCount(cat):
    cat_dict = {0:0,1:25,2:75,3:150,4:250,5:500} #bed category mapping as per AURIN
    return cat * cat_dict[cat]

def getLiveability():

    with open('config/couchDB_config.json', 'r') as f:
            couchdbConfig = json.load(f)

    dbuser = couchdbConfig['user']
    dbpwd = couchdbConfig['password']
    dburl = couchdbConfig['urlnohttp']

    housingUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/housing_rent_aff/_design/getLatestRAI/_view/getLatestRAI"
    SchoolUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/sch_rank/_design/getTopSchoolInfo/_view/getTopSchoolInfo"
    EnvUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/env_pollutant/_design/getEnvData/_view/getEnvData"
    EntBarUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/ent_bar_seating/_design/getEntBarData/_view/getEntBarData"
    EntCafeUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/ent_cafe_seating/_design/getEntCafeData/_view/getEntCafeData"
    SportUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/ent_sports/_design/getSportsData/_view/getSportsData"
    HospitalUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"/health_no_beds/_design/getHospitalData/_view/getHospitalData"

    aggDict = {'latest_rai':'mean','ses': 'mean','enrollments':'sum','activities':'count','properties_trading_name_x':'nunique','properties_trading_name_y':'nunique','facility_name':'nunique','bed_cat':'sum'}

    finaldf =pd.DataFrame()
    groupbyCols=['key']
    for url in [housingUrl ,SchoolUrl,EnvUrl,EntBarUrl, EntCafeUrl,SportUrl,HospitalUrl]:
        response = requests.request("GET", url)
        response_json = json.loads(response.text)
        df = pd.DataFrame(response_json['rows'])
        
        df = df.drop(["id"],axis=1)
        df = df[df['key'].notna()]
        df['key']=df['key'].astype(int)
        df = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)
        if finaldf.empty:
            finaldf = df.fillna(0)
        else:
            finaldf = pd.merge(finaldf, df, on=['key'],how="left")
            finaldf = finaldf.fillna(0)
            if url==HospitalUrl:
                finaldf['bed_cat'] = finaldf['bed_cat'].apply(lambda x: getBedCount(x))
            newAggDict=dict()
            tempCols=copy.deepcopy(groupbyCols)
            for key in aggDict.keys():
                if key in finaldf.columns and aggDict[key]!=0:
                    newAggDict[key] = aggDict[key]
                    aggDict[key]=0
                    tempCols.append(key)
            if len(newAggDict) > 0:               
                finaldf = finaldf.groupby(groupbyCols).agg(newAggDict).reset_index()
            groupbyCols=copy.deepcopy(tempCols)

    finaldf = finaldf.fillna(0)

    
    scaler = MinMaxScaler()
    scaledDF=finaldf.copy(deep=True)
    columns_to_scale=list(set(scaledDF.columns)-set(['key']))
    scaledDF[columns_to_scale]=scaler.fit_transform(scaledDF[columns_to_scale])
    scaledDF['activities']=1-scaledDF['activities']
    scaledDF['Rank']=scaledDF[columns_to_scale].sum(axis=1)
    finaldf=pd.merge(finaldf,scaledDF[['key','Rank']],on='key',how='left')
    finaldf.sort_values(by=['Rank'],inplace=True,ascending=False)
    finaldf.rename(columns={'properties_trading_name_x': 'no_cafe', 'properties_trading_name_y': 'no_bar','facility_name': 'no_sport_facilities','bed_cat':'no_beds'}, inplace=True)
    

    response = requests.request("GET", housingUrl)
    response_json = json.loads(response.text)
    df = pd.DataFrame(response_json['rows'])
    df = df.drop(["id"],axis=1)
    df = df[df['key'].notna()]
    df['key']=df['key'].astype(int)
    df = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)

    finaldf = pd.merge(finaldf,df[['bbox','key']],on=['key'],how="left")

    finaldf['ses'] = finaldf['ses'].round(decimals = 2)
    finaldf['Rank'] = finaldf['Rank'].round(decimals = 2)

    jsondata = json.loads(finaldf.to_json(orient = 'records'))
    couch = couchdb.Server(couchdbConfig['url'])  
    couch.resource.credentials = (couchdbConfig['user'] , couchdbConfig['password'])
    db = couch[couchdbConfig['couch_liveability']]

    db.update(jsondata)