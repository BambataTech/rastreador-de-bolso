import os
import pathlib

from dotenv import load_dotenv

CURR_PATH = pathlib.Path(__file__).parent.absolute()

load_dotenv(os.path.join(CURR_PATH, '../../.env'))

TWITTER_APP_KEY = os.getenv("TWITTER_APP_KEY")
TWITTER_APP_SECRET = os.getenv("TWITTER_APP_SECRET")
TWITTER_OAUTH_TOKEN = os.getenv("TWITTER_OAUTH_TOKEN")
TWITTER_OAUTH_TOKEN_SECRET = os.getenv("TWITTER_OAUTH_TOKEN_SECRET")
USER_ID = os.getenv('USER_ID')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
