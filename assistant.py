from cmd import Cmd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import term_colors, str_bold, str_header, str_blue, str_green, \
    str_fail, console_update
from webscraper import (search_twitter, 
                        scrape_page_for_tweets,
                        save_tweets_to_csv)

PAGES_TO_SCROLL = 50

class AssistantCmdLine(Cmd):
    prompt = str_header("Assistant > ")
    intro = ("Assistant online.\n"
             "Type 'help' to list available commands")
    browser = None    
    tweets_last_searched = []

    def __init_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1080x1080")
        print("Initializing Chrome driver...")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        print("Chrome browser initialized.")


    def do_search(self, inp):
        '''
        Search twitter
        Usage: "search my_search_terms"
        Example: "search elongated muskrat"
                 => Searches twitter for "elongated muskrat"
        '''
        if self.browser == None:
            self.__init_browser()
        print("Searching twitter for: {}".format(inp))
        self.tweets_last_searched = search_twitter(inp, self.browser,
                                    PAGES_TO_SCROLL)
    
    # TODO: do_set enable setting of search settings

    def do_print(self, inp):
        '''
        Print all collected tweets
        '''
        if self.tweets_last_searched == None:
            print("No tweets collected!")
            return
        print_tweets(self.tweets_last_searched)


    def do_exit(self, inp):
        '''
        Type to exit assitant
        '''
        print("Assistant going offline.\nGoodbye!")
        if (self.browser != None):
            self.browser.quit()
        return True

    do_EOF = do_exit

def main():
    AssistantCmdLine().cmdloop()
    

def print_tweets(tweets):
    for tweet in tweets:
        print("{}: {}\n"
            .format(
                str_blue(tweet["user"]),
                tweet["content"])
            )

if __name__ == '__main__':
    main()
