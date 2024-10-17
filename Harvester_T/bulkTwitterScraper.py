import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from couchDB_conn import CouchConnector
import setup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')
print('-----Running Bulk harvestor-----')
csvFile = pd.read_csv(setup.csvfile)
category = list(set(csvFile['Category']))
dbobj = CouchConnector(setup.bulk_dbname)

countPrev=999
iteration=1
maxId=''
while countPrev!=0:
    tweets_list = []
    counter=0
    if(iteration==1):
        tweet_items=sntwitter.TwitterSearchScraper('since:2020-01-01 until:2022-05-05 near:"Melbourne" within:50km').get_items()
    else:
        tweet_items=sntwitter.TwitterSearchScraper('since:2020-01-01 until:2022-05-05 near:"Melbourne" within:50km max_id:'+maxId).get_items()
    for i,tweet in enumerate(tweet_items):
        if(counter>1000):
            print("Here")
            break

        processedTweet={
            "_id": str(tweet.id),
            "created_at": tweet.date.strftime("%m/%d/%Y, %H:%M:%S"),
            "text": tweet.content,
            "User_id_str": tweet.user.id, 
            "geo": tweet.user.location,
            "screen_name": tweet.user.displayname,
            "lang": tweet.lang,
            "favorite_count": tweet.likeCount,
            "retweet_count": tweet.retweetCount,
            "followers_count": tweet.user.followersCount
        }
        counter+=1
        for cat in category:
            words = csvFile[csvFile['Category']==cat]['Keywords'].to_list()
            for word in words:
                if re.search(r"\b" +  re.escape(word) +r"\b" , processedTweet['text']):
                    processedTweet['category'] = cat
        
        processedTweet['sentiment_score']=SentimentIntensityAnalyzer().polarity_scores(tweet.content)['compound']
        processedTweet['sentiment']= 'Positive' if processedTweet['sentiment_score']>0 else ('Negative' if processedTweet['sentiment_score']<0 else 'Neutral')
                            
        tweets_list.append(processedTweet)
    dbobj.db.update(tweets_list)
    countPrev=len(tweets_list)
    iteration+=1
    if(countPrev>0):
        maxId=tweets_list[-1]['_id']
