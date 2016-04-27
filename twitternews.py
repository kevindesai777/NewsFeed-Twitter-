import requests
from requests_oauthlib import OAuth1
from StringIO import StringIO
from time import sleep
import json
import os



fname = "twitternews.config"
CON = json.load(file(fname, 'r'))


class Fetch_news(object):
    def __init__(self, consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None):
        self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def fetch_tweets(self, params=None):                
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        self.response = requests.get(url, params=params, auth=self.auth, timeout=CON["timeout"])


def main():
    
    news = Fetch_news(CON["key"], CON["secret"], CON["token"], CON["token_secret"])

    # Initialize the previous id to 0
    last_id = {account["name"]: 0 for account in CON["accounts"]}

    # Perform read loop
    while True:
        try:
            for account in CON["accounts"]:
                name = account["name"]
                file_name = account["file"]

                params = {'screen_name':name, 'exclude_replies':'true', 'count':'200'}
                if last_id[name] > 0:
                    params['max_id'] = last_id[name]
                news.fetch_tweets(params)
                posts = json.load(StringIO(news.response.content))

                # if there is any error with the response, log it and try next news_source
                if news.response.status_code != 200:
                    continue

                # append tweets to file
                with file(file_name, "a+") as output_stream:
                    for item in posts:
                        output_stream.write(json.dumps(item))
                        output_stream.write("\n")
                        if last_id[name] == 0:
                            last_id[name] = item['id']-1
                        else:
                            last_id[name] = min(last_id[name], item['id']-1)

        except Exception as e:
            print "Error"


if __name__ == "__main__":
    main()

