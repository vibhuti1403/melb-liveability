from flask import Flask, request, jsonify
from couchdb.design import ViewDefinition
import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import copy
from flask_cors import CORS, cross_origin



dotenv_path = Path('.envdb_api')
load_dotenv(dotenv_path=str(dotenv_path))

dbuser = os.getenv("DBuser")
dbpwd = os.getenv("DBpwd")
dburl = os.getenv("DBurl")

app = Flask(__name__)
cors = CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'


#Sentiment_Analysis_data 
#methods=['GET']
def getSentimentAnalysis(dbname,designName,viewName,cat,sentiment):
    
    url = "http://" + dbuser +":"+dbpwd +"@" + dburl+dbname+"/_design/"+designName+"/_view/"+viewName+"?startkey=[\""+cat.strip()+"_"+sentiment.strip()+"\"]&endkey=[\""+cat.strip()+"_"+sentiment.strip()+"\"]"
    response = requests.request("GET", url)
    response_json = json.loads(response.text)
    return response_json["rows"][0]["value"]




@app.route('/GetSentiment' , methods=['GET'])
@cross_origin()
def aggregateAnalysis():
    categories = os.getenv("categories").replace("[","").replace("]","").split(",")
    res=dict()
    for cat in categories:
        cat = cat.strip()
        res[cat]={'Positive':getSentimentAnalysis("archived_tweets","sentiments_count","sentiment_archived_tweets",cat,"Positive") + 
                              getSentimentAnalysis("tweets","sentiment_view","sentiment_tweets",cat,"Positive")+
                              getSentimentAnalysis("bulk_tweets","sentiment_view_bulk_tweets","sentiment_bulk_tweets",cat,"Positive"),
        
                'Negative':getSentimentAnalysis("archived_tweets","sentiments_count","sentiment_archived_tweets",cat,"Negative")+
                            getSentimentAnalysis("tweets","sentiment_view","sentiment_tweets",cat,"Negative")+
                            getSentimentAnalysis("bulk_tweets","sentiment_view_bulk_tweets","sentiment_bulk_tweets",cat,"Negative"),

                'Neutral':getSentimentAnalysis("archived_tweets","sentiments_count","sentiment_archived_tweets",cat,"Neutral")+
                            getSentimentAnalysis("tweets","sentiment_view","sentiment_tweets",cat,"Neutral")+
                            getSentimentAnalysis("bulk_tweets","sentiment_view_bulk_tweets","sentiment_bulk_tweets",cat,"Neutral"),
        }
    return res

@app.route('/GetRAI' , methods=['GET'])
@cross_origin()
def getRAI():
    # http://45.113.235.189:5984/housing_rent_aff/_design/getLatestRAI/_view/getRAI?key=%223000%22
    
    url = "http://" + dbuser +":"+dbpwd +"@" + dburl+"housing_rent_aff/_design/getLatestRAI/_view/getRAI"
    response = requests.request("GET", url)
    response_json = json.loads(response.text)

    df =pd.DataFrame()
    for r in response_json['rows']:
        df = df.append(r['value'], ignore_index = True)
    df = df.drop("postcode" ,axis= 1)
    jsondata = json.loads(df.mean(axis=0).to_json(orient = 'columns'))
    return jsondata

@app.route('/GetLiveability' , methods=['GET'])
def getLiveability():
    housingUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"housing_rent_aff/_design/getLatestRAI/_view/getLatestRAI"
    SchoolUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"sch_rank/_design/getTopSchoolInfo/_view/getTopSchoolInfo"
    EnvUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"env_pollutant/_design/getEnvData/_view/getEnvData"
    EntBarUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"ent_bar_seating/_design/getEntBarData/_view/getEntBarData"
    EntCafeUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"ent_cafe_seating/_design/getEntCafeData/_view/getEntCafeData"
    SportUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"ent_sports/_design/getSportsData/_view/getSportsData"
    HospitalUrl= "http://" + dbuser +":"+dbpwd +"@" + dburl+"health_no_beds/_design/getHospitalData/_view/getHospitalData"

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
    jsondata = json.loads(finaldf.to_json(orient = 'records'))
    return jsonify(jsondata)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")