import json
from datetime import datetime
from pymongo import MongoClient, TEXT

client = MongoClient('bolsona-archive-db', 27017)
tweets_db = client['jairbolsonaro']['tweets']

TWITTER_TIME = '%a %b %d %H:%M:%S +0000 %Y'


def update_id(tweet):
    tweet['_id'] = tweet['id_str']
    return tweet


def update_timestamp(tweet):
    timestamp = tweet['created_at']
    tweet['created_at'] = datetime.strptime(
        timestamp, TWITTER_TIME
    ).isoformat()
    return tweet


def update_fields(tweet):
    return update_timestamp(
        update_id(tweet)
    )


with open('/data/jairbolsonaro.json') as tweets_file:
    tweets = json.load(tweets_file)
    tweets = [update_fields(t) for t in tweets]
    tweets_db.insert_many(tweets)

tweets_db.create_index([("full_text", TEXT)], name="search")
