from TwitterListner import TwitterListener

import schedule
import time
import sys
import json

tl = TwitterListener()


def monitoring_tweets():
    tl.print_new_tweets()
    tl.watch_friends()


schedule.every(60).seconds.do(monitoring_tweets)


while True:
    schedule.run_pending()
    time.sleep(1)
