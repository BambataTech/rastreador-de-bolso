from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import logging
import coloredlogs
import os
import pathlib
import time

import twitter as tt
from utils import retry
from fetch_likes import get_user_likes, login
from conf.settings import USER_ID, USERNAME, PASSWORD

CURR_PATH = pathlib.Path(__file__).parent.absolute()
TWEETS_FOLDER = os.path.join(CURR_PATH, 'screenshots')
LIKED_FOLDER = os.path.join(CURR_PATH, 'screenshots', 'liked')


class TwitterListener():
    def __init__(self, user_id=USER_ID, search_base=40):
        # Configure log
        coloredlogs.install()
        logging.basicConfig()
        self.logger = logging.getLogger('TwitterListener')
        self.logger.setLevel(logging.DEBUG)

        # Set chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        login(self.driver, USERNAME, PASSWORD)

        # Create formatter, file handler and add they to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler('twitter.log')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.search_base = search_base
        self.user_id = user_id
        self.target = tt.get_username_from_id(user_id)
        self.previous_tweets_ids = tt.get_ids_from_tweets(
            tt.get_tweets(user_id=user_id, count=search_base))
        self.previous_friends = tt.get_friends_ids(user_id=user_id)
        self.previous_likes_ids = get_user_likes(
            self.driver, self.target, count=search_base/2)

    def _get_new_tweets(self):
        last_tweets = tt.get_tweets(user_id=self.user_id,
                                    count=self.search_base)
        last_tweets_ids = tt.get_ids_from_tweets(last_tweets)

        diff_tweets = self._get_new_diff(
            last_tweets_ids, self.previous_tweets_ids)

        if diff_tweets:
            new_tweets = [last_tweets[i] for i in range(len(diff_tweets))]
            self.previous_tweets_ids = last_tweets_ids
            new_tweets.reverse()
            return new_tweets
        return []

    def _get_new_likes(self):
        new_likes_ids = get_user_likes(
            self.driver, self.target, count=self.search_base/2)
        diff_tweets = self._get_new_diff(
            new_likes_ids, self.previous_likes_ids)

        if diff_tweets:
            self.previous_likes_ids = new_likes_ids
            diff_tweets.reverse()
            return diff_tweets

        return []

    def _get_new_diff(self, curr, old):
        count = len(old)
        return list(set(curr[:count//2]) -
                    set(old))

    def _get_abs_diff(self, first_list, second_list):
        return list(set(first_list) - set(second_list))

    def print_new_tweets(self):
        try:
            new_tweets = self._get_new_tweets()
            for tweet in new_tweets:
                tweet_id = str(tweet['id'])
                tweet_url = tt.get_url(tweet)

                # Get image
                self.logger.info('New tweet %s', tweet_url)
                img_path = os.path.join(TWEETS_FOLDER, f'{tweet_id}.png')
                retry(tt.print_tweet, tweet_url,
                      self.driver, output_path=img_path)
                self.logger.debug('Take a screenshot of tweet')

                # Tweet image

                tweet_msg = 'Jair Bolsonaro acabou de twittar'
                self.logger.debug(
                    f'Is a retweet: {"retweeted_status" in tweet}')
                if('retweeted_status' in tweet):
                    tweet_msg = 'Jair Bolsonaro acabou de retweetar'

                tt.tweet_print(img_path, tweet_url, tweet_msg)
                self.logger.debug('Tweet the screenshot')
        except Exception as e:
            self.logger.error(e)

    def print_new_likes(self):
        try:
            new_likes = self._get_new_likes()
            for t_id in new_likes:
                t_url = f'https://twitter.com/{self.target}/status/{t_id}'

                # Get image
                self.logger.info('New like %s', t_url)
                img_path = os.path.join(LIKED_FOLDER, f'{t_id}.png')
                retry(tt.print_tweet, t_url, self.driver, output_path=img_path)
                self.logger.debug('Take a screenshot of tweet')

                # Tweet image
                t_msg = 'Jair Bolsonaro acabou de curtir esse tweet'
                tt.tweet_print(img_path, t_url, t_msg)
                self.logger.debug('Tweet the screenshot')
        except Exception as e:
            self.logger.error(e)

    def watch_friends(self):
        try:
            last_friends = tt.get_friends_ids()

            new_friends = self._get_abs_diff(
                last_friends, self.previous_friends)
            unfriends = self._get_abs_diff(self.previous_friends, last_friends)

            for user_id in new_friends:
                username = tt.get_username_from_id(user_id=user_id)
                self.logger.info(f'New friend: @{username}')
                retry(
                    tt.update_status,
                    status=(
                        f'Jair Bolsonaro aparentemente está seguindo @{username}.'
                        '\n(Esse bot não consegue verificar se essa atualização foi gerada '
                        'por um follow ou por uma reativação de conta)'
                    )
                )

            for user_id in unfriends:
                username = tt.get_username_from_id(user_id=user_id)
                self.logger.info(f'Unfriend: @{username}')
                retry(
                    tt.update_status,
                    status=(
                        f'Jair Bolsonaro aparentemente deixou de seguir @{username}.'
                        '\n(Esse bot não consegue verificar se essa atualização foi gerada '
                        'por um unfollow, suspensão ou block.)'
                    )
                )

            self.previous_friends = last_friends
        except Exception as e:
            self.logger.error(e)
