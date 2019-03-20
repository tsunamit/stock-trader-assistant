import requests
from bs4 import BeautifulSoup

def main():
    url = 'https://twitter.com/search?q=tesla'

    page_contents = fetch_page(url)
    if (page_contents == None):
        exit(1)

    print("Successfully fetched page contents.")

    soup = BeautifulSoup(page_contents, 'lxml')
    # TODO: check for error page

    tweets = find_all_tweets(soup)
    print("Found {} tweets.".format(len(tweets)))
    for tweet in tweets:
        print("TWEET: {}".format(tweet))
    
    print("Assistant signing off. You should be studying")


def find_all_tweets(soup):
    tweets = []
    # TODO can't seem to find these html list tweet items
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    print(len(tweets))
    scraped_tweet_text = []
    for tweet in tweets:
        print("Found a tweet. Parsing...")
        tweet_data = None
        tweet_data = get_tweet_content(tweet)
        scraped_tweet_text.append(tweet_data)

    return scraped_tweet_text

def get_tweet_content(tweet_li_elt):
    tweet_text_box = tweet_li_elt.find("p", {"class": "TweetTextSize  js-tweet-text "
                     "tweet-text"})
    tweet_text = tweet_text_box.text

    # TODO support image content

    return tweet_text

def fetch_page(url):
    r = None
    try:
        r = requests.get(url)
    except Exception as e:
        print(repr(e)) 
        repr("Request error returning nothing")
    
    if (r):
        return r.text
    else:
        return None


if __name__ == '__main__':
    main()