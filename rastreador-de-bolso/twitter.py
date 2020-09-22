
import os
import sys
import json
import logging
import time

from twython import Twython, TwythonStreamer

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from print_tweet import print_tweet

from utils import retry

from conf.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET, USER_ID


twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET,
                  TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)


def tweet_print(img_path, url, msg):
    photo = open(img_path, 'rb')
    response = twitter.upload_media(media=photo)
    status = f'{msg}: {url}'
    twitter.update_status(status=status,
                          media_ids=[response['media_id']])


def get_favorites(user_id=USER_ID, ):
    return twitter.get_favorites(user_id=user_id, sort_by="source")


def get_tweets(user_id=USER_ID, count=20, screen_name=''):
    username = screen_name if screen_name else get_username_from_id(user_id)
    return twitter.search(q=f'from:{username} include:nativeretweets', count=count, result_type='recent')['statuses']


def update_status(status):
    twitter.update_status(status=status)


def get_timeline():
    return twitter.get_home_timeline()


def get_friends_ids(user_id=USER_ID):
    response = twitter.get_friends_ids(user_id=user_id)
    return response['ids']


def get_ids_from_tweets(tweets):
    return [tweet['id'] for tweet in tweets]


def get_username_from_id(user_id=USER_ID):
    return twitter.show_user(user_id=user_id)['screen_name']


def get_url(tweet_data):
    user = tweet_data['user']['screen_name']
    tweet_id = tweet_data['id']

    if 'retweeted_status' in tweet_data:
        tweet_id = tweet_data['retweeted_status']['id']
        print(tweet_id)

    return f'https://twitter.com/{user}/status/{tweet_id}'
