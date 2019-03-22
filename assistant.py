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
    url = 'https://twitter.com/search?q=tesla&src=typd'

    browser, body = fetch_page(url)
    if (browser == None):
        exit(1)

    print("Successfully fetched page contents.")

    tweets = browser.find_elements_by_class_name("tweet-text")

    for tweet in tweets:
        print("TWEET: \n{}\n\n".format(tweet.text))

    # TODO: check for error page

    # tweets = find_all_tweets(soup)
    # print("Found {} tweets.\n\n".format(len(tweets)))
    # for tweet in tweets:
    #     print("TWEET: {}\n".format(tweet))

    # print("Assistant signing off. You gotta give me a name or something")


def scrape_profile(soup):
    tweets = find_all_tweets(soup)
    print("Found {} tweets.\n\n".format(len(tweets)))
    for tweet in tweets:
        print("TWEET: {}\n".format(tweet))


def find_all_tweets(soup):
    tweets = []
    # TODO can't seem to find these html list tweet items
    tweets = soup.find_all("p", {"class": "tweet-text"})
    scraped_tweet_text = []
    for tweet in tweets:
        # print("Found a tweet. Parsing...")
        tweet_data = tweet.text 
        scraped_tweet_text.append(tweet_data)

    return scraped_tweet_text

def fetch_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(url)

    body = browser.find_element_by_tag_name('body')

    for _ in range(PAGES_TO_SCROLL):
        body.send_keys(Keys.PAGE_DOWN)
        console_update("Fetching page {}/{}".format(_, PAGES_TO_SCROLL))

    return browser, body

    # r = None
    # try:
    #     r = requests.get(url)
    #     time.sleep(1)
    # except Exception as e:
    #     print(repr(e)) 
    #     repr("Request error returning nothing")
    
    # return r.text if r else None


def console_update(s):
    sys.stdout.write("\r{}".format(s))
    sys.stdout.flush()


if __name__ == '__main__':
    main()