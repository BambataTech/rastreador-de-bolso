#!/usr/bin/env python3
import os
import sys
import time
import pathlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image


CURR_PATH = pathlib.Path(__file__).parent.absolute()


def print_tweet(url, web_driver, *args, **kwargs):
    if kwargs.get('output_path'):
        output_path = kwargs.get('output_path')
    else:
        output_path = os.path.join(CURR_PATH, 'screenshots/tweet.png')

    with open(os.path.join(CURR_PATH, 'templates/tweet.html')) as tweet_template:
        with open(os.path.join(CURR_PATH, 'views/tweet.html'), 'w') as tweet_view:
            for line in tweet_template:
                tweet_view.write(line.replace('{{ tweet_link }}', url))

    # Open tweet view
    web_driver.get(
        'file://{}/views/tweet.html'.format(CURR_PATH))

    # Wait page to load element
    element = WebDriverWait(web_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'twitter-tweet'))
    )

    # Change window size
    location = element.location
    size = element.size
    initial_x = location['x']
    initial_y = location['y']
    final_x = location['x']+size['width']
    final_y = location['y']+size['height']
    web_driver.set_window_size(900, final_y)

    # Save screenshot
    time.sleep(3)
    web_driver.save_screenshot(output_path)

    # Crop image
    im = Image.open(output_path)
    im = im.crop((int(initial_x), int(initial_y), int(final_x), int(final_y)))
    im.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Invalid argument, execute with tweet link')
        exit

    try:
        # Set chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Get webdriver
        driver = webdriver.Chrome(options=chrome_options)
        url = sys.argv[1]
        print_tweet(url, driver)
    except:
        print('Something goes wrong')
        print(sys.exc_info()[1])
    finally:
        driver.quit()
