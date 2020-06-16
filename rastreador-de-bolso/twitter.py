
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


def get_favorites(user_id=USER_ID, ):
    return twitter.get_favorites(user_id=user_id, sort_by="source")


def get_tweets(user_id=USER_ID, count=20, screen_name=''):
    username = screen_name if screen_name else get_username_from_id(user_id)
    return twitter.search(q=f'from:{username}', count=count, result_type='recent')['statuses']


def get_ids_from_tweets(tweets):
    return [tweet['id'] for tweet in tweets]


def get_username_from_id(user_id=USER_ID):
    return twitter.show_user(user_id=user_id)['screen_name']


def get_url(tweet_data):
    return 'https://twitter.com/{}/status/{}'.format(
        tweet_data['user']['screen_name'], tweet_data['id'])


class TwitterListener():
    def __init__(self, user_id=USER_ID):
        # Configure log
        FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('TwitterListener')

        self.user_id = user_id
        self.previous_tweets_ids = get_ids_from_tweets(
            get_tweets(user_id=user_id))

        # Set chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')

    def get_new_tweets(self):
        last_tweets = get_tweets(user_id=self.user_id)
        last_tweets_ids = get_ids_from_tweets(last_tweets)

        diff_tweets = list(set(last_tweets_ids) -
                           set(self.previous_tweets_ids))
        if diff_tweets:
            new_tweets = [last_tweets[i] for i in range(len(diff_tweets))]
            self.previous_tweets_ids = last_tweets_ids
            return new_tweets
        return []

    def print_new_tweets(self):
        # Get webdriver
        driver = webdriver.Chrome(options=self.chrome_options)

        new_tweets = self.get_new_tweets()
        for tweet in new_tweets:
            tweet_id = str(tweet['id'])
            tweet_url = get_url(tweet)

            # Get image
            img_path = os.path.join(TWEETS_FOLDER, f'{tweet_id}.png')
            print_tweet(tweet_url, driver, img_path,)

            # Tweet image
            tweet_print(img_path, tweet_url)

            self.logger.info('New tweet')
            self.logger.info(f'text: {tweet["text"]}')
            self.logger.info(f'url: {tweet_url}')

        driver.close()


class PrintStream(TwythonStreamer):
    def on_success(self, data):
        print('Receive tweet from: ', data['user']['id_str'])
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
