import requests
from requests_oauthlib import OAuth1
from StringIO import StringIO
import json

fname = "app.config"
CON = json.load(file(fname, 'r'))

class Fetch_news(object):
    def __init__(self, consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None):
        self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def fetch_tweets(self, params=None):                
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        self.response = requests.get(url, params=params, auth=self.auth, timeout=10)

def main():
      
    key = "xxxx"
    secret = "xxxx"
    token = "xxxx"
    token_secret ="xxxx"
    news = Fetch_news(key, secret, token, token_secret)
    id = {account["name"]: 0 for account in CON["accounts"]}

    while True:
        try:
            for account in CON["accounts"]:
                name = account["name"]
                file_name = account["file"]
                params = {'screen_name':name, 'exclude_replies':'true', 'count':'200'}
                
                if id[name] > 0:
                    params['max_id'] = id[name]
                news.fetch_tweets(params)
                tweets = json.load(StringIO(news.response.content))
               
                if news.response.status_code != 200:
                    continue

                with file(file_name, "a+") as output_stream:
                    for t in tweets:
                        output_stream.write(json.dumps(t))
                        output_stream.write("\n")
                        if id[name] == 0:
                            id[name] = t['id']-1
                        else:
                            id[name] = min(id[name], t['id']-1)

        except Exception as e:
            print "Error"

if __name__ == "__main__":
    main()

