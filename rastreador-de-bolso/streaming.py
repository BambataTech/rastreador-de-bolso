from twitter import PrintStream


from conf.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET, USER_ID

stream = PrintStream(TWITTER_APP_KEY, TWITTER_APP_SECRET,
                     TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)

stream.statuses.filter(follow=[USER_ID])
