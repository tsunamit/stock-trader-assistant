import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

PAGES_TO_SCROLL = 100

def main():
    url = 'https://twitter.com/elonmusk'
    # url = 'https://twitter.com/search?q=tesla&src=typd'
    url = "https://twitter.com/ryantsang11"

    browser = fetch_page(url)
    if (browser == None):
        exit(1)
    print("Successfully fetched page contents.")

    tweets = browser.find_elements_by_class_name("tweet-text")
    for tweet in tweets:
        print("TWEET: \n{}\n\n".format(tweet.text))
    print("Assistant signing off. You gotta give me a name or something")



def fetch_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1080x1080")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)

    body = browser.find_element_by_tag_name('body')

    for _ in range(PAGES_TO_SCROLL):
        body.send_keys(Keys.PAGE_DOWN)
        console_update("Fetching page {}/{}".format(_, PAGES_TO_SCROLL))
    print()

    return browser 



def console_update(s):
    sys.stdout.write("\r{}".format(s))
    sys.stdout.flush()


if __name__ == '__main__':
    main()