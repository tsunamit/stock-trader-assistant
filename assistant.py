import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

PAGES_TO_SCROLL = 50

def main():
    print("Assistant online...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1080x1080")

    print("Initializing Chrome driver...")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    print("Chrome browser initialized. Fetching URL...")

    tweets = search_twitter("quotation", browser, PAGES_TO_SCROLL)

    save_tweets_to_csv(tweets, 'out.csv')

    print("Assistant offline... Goodbye!")

    

def search_twitter(search_terms, browser, scroll_dist=10):
    search_query = search_terms.replace(" ", "%20")
    url = "https://twitter.com/search?q={}".format(search_query)

    tweets = scrape_page_for_tweets(url, browser, scroll_dist)    
    return tweets
    
 

def scrape_page_for_tweets(url, browser, scroll_dist=10):
    '''
    Call this function with a URL to scrape the page for tweets
    '''
    html = __fetch_twitter_page(url, scroll_dist, browser)
    print()

    if (html == None):
        exit(1)
    print("Successfully fetched page contents.")
    return  __get_tweet_info(html)


def save_tweets_to_csv(tweets, filename):
    '''
    Take tweets and save to a csv in following format:
    id, user, favorites, retweets, timestamp, content 
    '''
    print("Saving tweet data to {}...".format(filename))
    with open(filename, 'w') as fd:
        # Print col descriptors
        print("{},{},{},{},{},{},{}"
              .format(
                    'id',
                    'timestamp',
                    'user',
                    'user_followers',
                    'favorites',
                    'retweets',
                    'content'
              ), file=fd)
        for tweet in tweets:
            print("{},{},{},{},{},{},{}"
                  .format(
                      tweet['id'],
                      tweet['timestamp'],
                      tweet['user'],
                      tweet['user_followers'],
                      tweet['favorites'],
                      tweet['retweets'],
                      ("\"{}\"".format(tweet['content']
                        .replace('\n', ' ')
                        .replace('"', '""')
                      ))
                  ), file=fd)
    print("Done!")

     


def __get_tweet_info(html):
    '''
    Given the browser which has fetched the page already, return the
    tweets
    '''
    benchmark_start = time.time()

    soup = BeautifulSoup(html, 'lxml')
    tweets_html = soup.find_all("div", {"class": "tweet"})
    tweets = []     # Holds dict entries for each tweet which contains 
                    # id, timestamp, username, favorites, retweets, content
    print("Found {} tweets. Parsing...".format(len(tweets_html)))

    c = 0   # simple counter
    for tweet_html in tweets_html:
        console_update("Parsing tweet {}/{}".format(c+1, len(tweets_html)))
        tweet_id = tweet_html.get("data-tweet-id")
        tweet_username = tweet_html.get("data-screen-name")

        # Get timestamp
        time_html = tweet_html.find("span", {"class": "_timestamp"})
        tweet_timestamp = int(time_html.get("data-time"))

        # Get favorites 
        favorites_div_html = tweet_html.find("div", 
                         {"class": "ProfileTweet-action--favorite"})
        favorites_html = favorites_div_html.find("span", {"class":
                         "ProfileTweet-actionCountForPresentation"})
        tweet_favorites = (0 if favorites_html.text == "" 
                          else __convert_twitter_str_to_num(
                              favorites_html.text))

        # Get retweets
        retweets_div_html = tweet_html.find("div", 
                         {"class": "ProfileTweet-action--retweet"})
        retweets_html = retweets_div_html.find("span", {"class": 
                        "ProfileTweet-actionCountForPresentation"})
        tweet_retweets = (0 if retweets_html.text == ""
                         else __convert_twitter_str_to_num(
                             retweets_html.text))
        

        # Get content
        tweet_content_html = tweet_html.find("p", {"class", "tweet-text"})
        tweet_content = tweet_content_html.text

        # Get user followers... right now it's a bottleneck
        # user_followers = __get_twitter_user_info(tweet_username)
        user_followers = 0

        tweets.append({
            "id": tweet_id,
            "timestamp": tweet_timestamp,
            "user": tweet_username,
            "user_followers": user_followers,
            "favorites": tweet_favorites,
            "retweets": tweet_retweets,
            "content": tweet_content,
        })
        
        c += 1  
    print()

    benchmark_end = time.time()
    log_benchmark_time_per_tweet(benchmark_start, benchmark_end, len(tweets))
        
    return tweets



def __get_twitter_user_info(username):
    user_page_url = "https://twitter.com/{}".format(username)
    soup = BeautifulSoup(__requests_fetch_page(user_page_url), 'lxml')
    
    # Get follwers count: li class=ProfileNav-item--followers
    followers_li_elt = soup.find("li", {"class":
                       "ProfileNav-item--followers"})
    followers_span_elt = followers_li_elt.find("span", 
                         {"class" : "ProfileNav-value"})
    follower_count = int(followers_span_elt.get('data-count'))

    return {
        "follower_count": follower_count
    } 



def __requests_fetch_page(url):
    '''
    Requests API fetch page. Designed to be used with Beautiful Soup
    '''
    r = None
    try:
        r = requests.get(url)
    except Exception as e:
        print(repr(e))
    return r.text if r else None



def __fetch_twitter_page(url, scroll_dist, browser):
    '''
    Given url, use selenium to fetch the twitter page and scroll
    '''
    benchmark_start = time.time()

    browser.get(url)

    body = browser.find_element_by_tag_name('body')
    print("Scanning twitter page: {}".format(str_header(url)))
    for _ in range(scroll_dist):
        body.send_keys(Keys.PAGE_DOWN)
        console_update(str_bold("Scan progress: {}/{}"
                                .format(_ + 1, scroll_dist)))
    print()
    html = browser.page_source

    benchmark_end = time.time()
    benchmark_delta = benchmark_end - benchmark_start 
    print(str_green("Fetched twitter page in {} seconds"
                   .format(benchmark_delta)))

    return html


def __convert_twitter_str_to_num(num_str):
    multiplier = 1
    if num_str[-1] == 'K':
        multiplier = 1000
    elif num_str[-1] == 'M':
        multiplier = 1000000
    elif num_str[-1] == 'B':
        multiplier = 1000000000
        
    num = 0
    if multiplier == 1:
        num = int(num_str)
    else:
        num = int(num_str[:1]) * multiplier
    return num




def log_benchmark_time_per_tweet(start, end, num_tweets_processed):
    delta = end - start
    print(str_green("Processed {} tweets in {} seconds"
                   .format(num_tweets_processed, delta)))
    print(str_green("Processing speed: {} tweets/second \n{} seconds/tweet"
                    .format(num_tweets_processed / delta, 
                    delta / num_tweets_processed)))


class term_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def str_bold(s):
    return ("{}{}{}".format(term_colors.BOLD, s, term_colors.ENDC))

def str_header(s):
    return ("{}{}{}".format(term_colors.HEADER, s, term_colors.ENDC))

def str_blue(s):
    return ("{}{}{}".format(term_colors.OKBLUE, s, term_colors.ENDC))

def str_green(s):
    return ("{}{}{}".format(term_colors.OKGREEN, s, term_colors.ENDC))

def str_fail(s):
    return ("{}{}{}".format(term_colors.FAIL, s, term_colors.ENDC))


def console_update(s):
    sys.stdout.write("\r{}".format(s))
    sys.stdout.flush()



if __name__ == '__main__':
    main()