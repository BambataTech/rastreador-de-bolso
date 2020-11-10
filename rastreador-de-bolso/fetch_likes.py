#!/usr/bin/env python3
import os
import sys
import time
import pathlib
import twitter as tt


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from conf.settings import USERNAME, PASSWORD
CURR_PATH = pathlib.Path(__file__).parent.absolute()
TWEETS_FOLDER = os.path.join(CURR_PATH, 'screenshots_liked')

id_selector = 'article > div > div.css-1dbjc4n > div:nth-child(1) > div > div  > div.css-1dbjc4n:nth-child(1) \
    > div.css-1dbjc4n.r-zl2h9q > div > div:nth-child(1) > a'


def login(driver, username, password, delay=1):
    login_url = 'https://twitter.com/login'
    driver.get(login_url)
    usernameInput = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.NAME, "session[username_or_email]"))
    )

    # usernameInput = driver.find_element_by_name(
    #     "session[username_or_email]")
    passwordInput = driver.find_element_by_name("session[password]")
    usernameInput.send_keys(USERNAME)
    passwordInput.send_keys(PASSWORD)
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(delay)


def _get_tweets_ids(driver):
    tweets = driver.find_elements_by_css_selector(id_selector)
    return [tweet.get_attribute('href').split('/')[-1] for tweet in tweets]


def _filter_unique(l):
    return list(dict.fromkeys(l))


def get_user_likes(driver, target, count=20, delay=1):
    try:
        driver.get(f'https://twitter.com/{target}/likes')
        time.sleep(delay)

        screen_height = driver.execute_script("return window.screen.height;")
        liked_ids = _get_tweets_ids(driver)

        i = 1
        while len(liked_ids) < count:
            driver.execute_script(
                f'window.scrollTo(0, {screen_height*i});')
            time.sleep(delay)
            liked_ids += _get_tweets_ids(driver)
            liked_ids = _filter_unique(liked_ids)
            i += 1

        return liked_ids
    except:
        print('Something goes wrong')
        print(sys.exc_info()[1])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Invalid argument, execute with tweet link')
        exit

    target = sys.argv[1]
    start_time = time.time()

    # Set chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")

    # Get webdriver
    driver = webdriver.Chrome(options=chrome_options)

    login(driver, USERNAME, PASSWORD, target)
    liked_tweets = get_user_likes(driver, target)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(liked_tweets)
