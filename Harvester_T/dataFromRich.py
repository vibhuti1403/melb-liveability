import json
import pandas as pd
import nltk
import setup
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from couchDB_conn import CouchConnector
nltk.downloader.download('vader_lexicon')

dbobj = CouchConnector(setup.archived_dbname)

with open('../../twitter-melb.json',encoding='utf=8') as inputFile: 
            tweetsDumps = []
            csvFile = pd.read_csv(setup.csvfile)
            category = list(set(csvFile['Category']))
            print(category)

            for lineNum,line in enumerate(inputFile):
                if lineNum == 0:
                    print(line)
                else:
                    if line != None and lineNum>0  and len(line)>3:
                        line = line.rstrip("," + "\n") 
                    if line[-2:] == "]}":
                       line=line[:-2]
                    tweet = json.loads(line)
                    tweet=tweet['doc']
                    tweet_dict=dict()
            
                    
                    for cat in category:
                         words = csvFile[csvFile['Category']==cat]['Keywords'].to_list()
                         for word in words:
                            if re.search(r"\b" +  re.escape(word) +r"\b" , tweet['text']):
                                tweet_dict['category'] = cat
                                tweet_dict['_id'] = tweet['id_str']
                                tweet_dict['created_at'] = str(tweet['created_at'])
                                tweet_dict['text'] = tweet['text']
                                tweet_dict['sentiment_score']=SentimentIntensityAnalyzer().polarity_scores(tweet['text'])['compound']
                                tweet_dict['sentiment']= 'Positive' if tweet_dict['sentiment_score']>0 else ('Negative' if tweet_dict['sentiment_score']<0 else 'Neutral')
                                tweet_dict['geo'] = tweet['geo']
                                tweet_dict['coordinates'] = tweet['coordinates']
                                tweet_dict['User_id_str'] = tweet['user']['id_str']
                                tweet_dict['screen_name'] = tweet['user']['screen_name']
                                tweet_dict['lang'] = tweet['lang']
                                tweet_dict['favorite_count'] = tweet['favorite_count']
                                tweet_dict['retweet_count'] = tweet['retweet_count']
                                tweet_dict['followers_count'] = tweet['user']['followers_count']
                                if tweet_dict['coordinates'] and setup.xmin <= float(tweet_dict['coordinates']['coordinates'][1]) <= setup.xmax and setup.ymin <= float(tweet_dict['coordinates']['coordinates'][0]) <= setup.ymax: #y,x in tweet
                                    tweet_dict['relevant'] = True
                                else:
                                    tweet_dict['relevant'] = False
                                    
                                tweetsDumps.append(tweet_dict)
                                if len(tweetsDumps) == 100:
                                    dbobj.db.update(tweetsDumps)
                                    tweetsDumps = []
 
inputFile.close()
