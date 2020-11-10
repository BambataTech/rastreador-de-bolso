from TwitterListener import TwitterListener

import schedule
import time
import sys
import json

tl = TwitterListener()


def monitor():
    tl.watch_friends()
    tl.print_new_likes()
    tl.print_new_tweets()


schedule.every(60).seconds.do(monitor)


while True:
    schedule.run_pending()
    time.sleep(1)
