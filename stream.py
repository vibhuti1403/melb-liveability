import tweepy
import couchdb
import pandas as pd
couch = couchdb.Server('http://user:user@localhost:5984')
api = "stream"
db = couch[api]
consumer_key = "pHP6ZVJH12cQ6SjhRKxYmerOi"
consumer_secret = "qiKFXfa3CuEVPB8RCsZEw8139YWuazsb49Qnz3Q8f8CmIYuL3w"
access_token = "1511599283509760003-rdkOcja5Y78Fq278PRmIUKgiaZc64p"
access_token_secret = "MruEuVYB7DdSrMAQ82sjAh6466Edy8MrWbF032bggi7Ha"

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        tweetsDumps = []
        tweet_dict=dict()
        tweet_dict['_id'] = status.id_str
        tweet_dict['created_at'] = str(status.created_at)
        tweet_dict['text'] = status.text
        tweet_dict['sentiment_score']=SentimentIntensityAnalyzer().polarity_scores(tweet.full_text)['compound']
        
        
        
        tweetsDumps.append(tweet_dict)
        db.update(tweetsDumps)
        
        #print(status._json)
        #df = pd.json_normalize(status._json)
        #df = df.rename(columns={'id': '_id'})
        #print(df.shape)
        return False


# Initialize instance of the subclass
printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)
tweetsDumps = []
# Filter realtime Tweets by keyword
printer.filter(track=["Twitter"])