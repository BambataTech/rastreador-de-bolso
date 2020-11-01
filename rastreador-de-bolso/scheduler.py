from TwitterListener import TwitterListener

import schedule
import time
import sys
import json

tl = TwitterListener()


schedule.every(15).seconds.do(tl.print_new_tweets)
schedule.every(60).seconds.do(tl.watch_friends)
schedule.every(60).seconds.do(tl.print_new_likes)


while True:
    schedule.run_pending()
    time.sleep(1)
