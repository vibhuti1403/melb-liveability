import tweepy
import setup
import json
import math
import pandas as pd
import argparse
from couchDB_conn import CouchConnector
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys


nltk.downloader.download('vader_lexicon')
print(setup.tweetsdbname)
dbobj = CouchConnector(setup.tweetsdbname)
real_dbobj = CouchConnector(setup.realtime_tweetsdbname)


class twitterHarvester:

    def __init__(self):
        auth = tweepy.OAuth2BearerHandler(setup.bearer_token)
        self.api = tweepy.API(auth,wait_on_rate_limit=True)


    def getTwitterData(self,category,query,count,limit=math.inf):
        
        tweetsDumps = []

        for tweet in tweepy.Cursor(self.api.search_tweets, q=query , geocode= setup.geo , tweet_mode='extended',count=count).items(limit=limit):
                tweet_dict=dict()
                
                tweet_dict['_id'] = tweet.id_str
                tweet_dict['created_at'] = str(tweet.created_at)
                tweet_dict['text'] = tweet.full_text
                tweet_dict['sentiment_score']=SentimentIntensityAnalyzer().polarity_scores(tweet.full_text)['compound']
                tweet_dict['sentiment']= 'Positive' if tweet_dict['sentiment_score']>0 else ('Negative' if tweet_dict['sentiment_score']<0 else 'Neutral')
                tweet_dict['geo'] = tweet.geo
                tweet_dict['coordinates'] = tweet.coordinates
                if tweet.coordinates is not dict and tweet.place is not None:
                    tweet_dict['coordinates'] = {"type": "Point", "coordinates": tweet.place.bounding_box.origin()}
                tweet_dict['User_id_str'] = tweet.user.id_str
                tweet_dict['screen_name'] = tweet.user.screen_name
                tweet_dict['lang'] = tweet.lang
                tweet_dict['favorite_count'] = tweet.favorite_count
                tweet_dict['retweet_count'] = tweet.retweet_count
                tweet_dict['followers_count'] = tweet.user.followers_count
                tweet_dict['category'] = category

                if tweet_dict['coordinates'] and setup.xmin <= float(tweet_dict['coordinates']['coordinates'][1]) <= setup.xmax and setup.ymin <= float(tweet_dict['coordinates']['coordinates'][0]) <= setup.ymax: #y,x in tweet
                    tweet_dict['relevant'] = True
                else:
                    tweet_dict['relevant'] = False
                tweetsDumps.append(tweet_dict)
    
        dbobj.db.update(tweetsDumps)
        tweetsDumps = []


    def getQueryWords(self,filename,catList,count,limit=math.inf):
        csvFile = pd.read_csv(filename)
        for cat in catList:
            words = csvFile[csvFile['Category']==cat]['Keywords'].to_list()
            for word in words:
                twitterHarvester.getTwitterData(self,cat,"\'" + word + "\'",count,limit)

class getRealTimeTweets(tweepy.Stream):

    #when tweet is recieved on_status is called
    def getCategory(self,text):
        for cat in di:
            if(any(word in text for word in di[cat])):
                return cat
            else:
                return None




    def on_status(self, status):
        #it is called when the tweet arrives into the stream
        tweetsDumps = []
        tweet_dict=dict()
        tweet_dict['_id'] = status.id_str
        tweet_dict['created_at'] = str(status.created_at)
        tweet_dict['text'] = status.text
        tweet_dict['sentiment_score']=SentimentIntensityAnalyzer().polarity_scores(status.text)['compound']
        tweet_dict['sentiment']= 'Positive' if tweet_dict['sentiment_score']>0 else ('Negative' if tweet_dict['sentiment_score']<0 else 'Neutral')
        tweet_dict['geo'] = status.geo
        tweet_dict['coordinates'] = status.coordinates
        if status.coordinates is not dict and status.place is not None:
            tweet_dict['coordinates'] = {"type": "Point", "coordinates": status.place.bounding_box.origin()}
        tweet_dict['User_id_str'] = status.user.id_str
        tweet_dict['screen_name'] = status.user.screen_name
        tweet_dict['lang'] = status.lang
        tweet_dict['favorite_count'] = status.favorite_count
        tweet_dict['retweet_count'] = status.retweet_count
        tweet_dict['followers_count'] = status.user.followers_count
        tweet_dict['category'] =  self.getCategory(status.text)
        if (tweet_dict['category'] is not None) and tweet_dict['coordinates'] and setup.xmin <= float(tweet_dict['coordinates']['coordinates'][1]) <= setup.xmax and setup.ymin <= float(tweet_dict['coordinates']['coordinates'][0]) <= setup.ymax: #y,x in tweet
            tweet_dict['relevant'] = True
        else:
            tweet_dict['relevant'] = False
            return True
        
        tweetsDumps.append(tweet_dict)
        print("Pushing tweets to couchdb")
        real_dbobj.db.update(tweetsDumps)
        return True




if __name__ == "__main__":
    harvObj = twitterHarvester()
    print("Query Categories",setup.category.split(","))
    harvObj.getQueryWords(setup.csvfile,setup.category.split(","),100)

    #twitter real time streaming
    category = setup.category.split(",")
    di = {}
    li=[]
    for cat in category:
        csvFile = pd.read_csv(setup.csvfile)
        words = csvFile[csvFile['Category']==cat]['Keywords'].to_list()
        di[cat] = words
    try:
        for key in di.keys():
            li.extend(di[key])
        GetRealTimeTweets = getRealTimeTweets(setup.consumer_key, setup.consumer_secret,setup.access_token, setup.access_token_secret)
        GetRealTimeTweets.filter(track=li,locations = [setup.ymin,setup.xmin,setup.ymax,setup.xmax])
    except Exception as ex:
        print("Errored out: ",ex)
        GetRealTimeTweets.disconnect()
    finally:
        GetRealTimeTweets.disconnect()
        sys.exit(0)

        
    

