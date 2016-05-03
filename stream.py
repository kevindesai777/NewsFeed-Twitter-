import time
import os
import reading as rd
from preprocess import get_text,english,parse,valid,Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


# User Credentials
access_token = "****"
access_token_secret = "****"
consumer_key = "****"
consumer_secret = "****"

start_time = time.time() 
keyword_list = ['politics', 'sports', 'game', 'trump', 'finance'] 

#Feature Generation
vectorizer_tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5,tokenizer=Tokenizer(), lowercase=True, strip_accents='unicode', stop_words='english', ngram_range=(1, 3))
## Choose your model here. For this demo, we chose Multinomial 
clf = MultinomialNB(alpha=0.01) 
train = vectorizer_tfidf.fit_transform(rd.dataset)
clf.fit(train,rd.target)
# Model can be pickled as well. 

class StdOutListener(StreamListener):
    tweet_count = 0

    def on_data(self, data):
        json_tweet = parse(data)
        print json_tweet['text']
        
        tweet = get_text(json_tweet)
        tweet = [tweet]
        test_tweet = vectorizer_tfidf.transform(tweet)
        pred = clf.predict(test_tweet)
        print get_category(pred[0])
        print "\n"

        StdOutListener.tweet_count = StdOutListener.tweet_count + 1
        time.sleep(5)
        if StdOutListener.tweet_count < 20:
            return True
        return False

    def on_error(self, status):
        time.sleep(3000)
        print status

#Predicting Category.
def get_category(x):
    ans = ''
    if x == 0:
        ans = 'politics'
    elif x==1:
        ans = 'sports'
    elif x==2:
        ans = 'technology'
    elif x==3:
        ans = 'entertainment'
    elif x==4:
        ans = 'finance'

    return ans


if __name__ == '__main__':    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=keyword_list, languages = ['en'])