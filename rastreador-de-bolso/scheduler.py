from twitter import TwitterListener

import schedule
import time
import sys

tl = TwitterListener()


def monitoring_tweets():
    tl.print_new_tweets()


schedule.every(15).seconds.do(monitoring_tweets)


while True:
    schedule.run_pending()
    time.sleep(1)
