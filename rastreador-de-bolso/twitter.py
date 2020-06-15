
import os
import pathlib
import json
import logging
import time

from twython import Twython, TwythonStreamer

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from print_tweet import print_tweet

from conf.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET, USER_ID


CURR_PATH = pathlib.Path(__file__).parent.absolute()
TWEETS_FOLDER = os.path.join(CURR_PATH, 'screenshots')
twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET,
                  TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)


def tweet_print(img_path, url):
    photo = open(img_path, 'rb')
    response = twitter.upload_media(media=photo)
    status = 'Jair Bolsonaro acabou de twittar: ' + url
    twitter.update_status(status=status,
                          media_ids=[response['media_id']])


def get_favorites(user_id=USER_ID):
    return twitter.get_favorites(user_id=user_id, sort_by="source")


def get_url(tweet_data):
    return 'https://twitter.com/{}/status/{}'.format(
        tweet_data['user']['screen_name'], tweet_data['id'])


class PrintStream(TwythonStreamer):
    def on_success(self, data):
        # print('Receive tweet from: ', data['user']['id_str'])
        if(data['user']['id_str'] == USER_ID):
            try:
                print('---------')
                url = 'https://twitter.com/{}/status/{}'.format(
                    data['user']['screen_name'], data['id'])

                # Set chrome options
                chrome_options = Options()
                chrome_options.add_argument('--headless')

                # Get webdriver
                driver = webdriver.Chrome(options=chrome_options)

                # Get image
                img_path = os.path.join(
                    TWEETS_FOLDER, str(data['id']) + '.png')
                print_tweet(url, driver, img_path,)
                tweet_print(img_path, url)
                print('\ttext: ', data['text'])
                print('\turl: ', url)
                print('---------')
            finally:
                driver.close()

    def on_error(self, status_code, data):
        print(status_code)
