import configparser
from src import helpers as h
import os
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import Stream
# import time
import json


class Twitter(object):

    def __init__(self):
        config = configparser.ConfigParser()

        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))

        if 'twitter.api' not in config.sections():
            raise ValueError("Config file not found.")

        config_ini = config['twitter.api']

        self.auth = OAuthHandler(config_ini['ConsumerKey'], config_ini['ConsumerSecret'])
        self.auth.set_access_token(config_ini['AccessTokenKey'], config_ini['AccessTokenSecret'])

        self.api = API(self.auth)

    def search_tweets(self, term, num_tweets, export=False, cache_only=True):
        # looking for cache
        cached_tweets = h.load_output(term, path='output/tweets')

        if cached_tweets and cache_only:
            return cached_tweets

        # query term to fetch tweets
        query_results = Cursor(self.api.search, q=term, lang="en").items(num_tweets)

        # construct tweets dictionary
        tweets = {tweet.id: tweet._json for tweet in query_results}

        # merge cached and recent tweets if there are any
        if cached_tweets:
            tweets = {**tweets, **cached_tweets}

        # casting key to int in order to silent sorting error
        tweets = {int(k): v for k, v in tweets.items()}

        if export:
            h.dump_output(tweets, term, path='output/tweets')

        return tweets

    def fetch_user_tweets(self, user, num_tweets, export=False, cache_only=True):
        # looking for cache
        cached_tweets = h.load_output(user, path='output/user')

        if cached_tweets and cache_only:
            return cached_tweets

        page_count = 1
        if num_tweets > 200:
            page_count = int(num_tweets / 200) + 1
            num_tweets = 200

        # query phrase to fetch tweets
        query_results = Cursor(self.api.user_timeline, screen_name=user, count=num_tweets).pages(page_count)

        # construct tweets dictionary
        tweets = {tweet.id: tweet._json for page in query_results for tweet in page}

        # merge cached and recent tweets if there are any
        if cached_tweets:
            tweets = {**tweets, **cached_tweets}

        # casting key to int in order to silent sorting error
        tweets = {int(k): v for k, v in tweets.items()}

        if export:
            h.dump_output(tweets, user, path='output/user')

        return tweets

    def get_stream_tweets(self, term, num_tweets):
        twitter_stream = Stream(self.auth, TwitterListener(num_tweets=num_tweets))
        try:
            twitter_stream.filter(track=[term], async=True)
        except Exception as e:
            print(e.__doc__)

        # lang, top_lang, top_tweets = self.stats.get_stats()
        # print(Counter(lang))
        # print(Counter(top_lang))
        # print(top_tweets)

# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             time.sleep(15 * 60)
#
#


class TwitterListener(StreamListener):
    def __init__(self, num_tweets=100):
        self.counter = 0
        self.num_tweets = num_tweets

    def on_data(self, data):
        try:
            j = json.loads(data)
            print('='*40)
            print(j["text"])
            self.counter += 1
            if self.counter == self.num_tweets:
                return False
            return True
        except:
            pass

    def on_error(self, status):
        print(status)


def get_stream(phrase, phrase_count=100):
    twitter_stream = Stream(get_twitter_auth(), TwitterListener(num_tweets=phrase_count))
    try:
        twitter_stream.filter(track=[phrase], async=True)
    except Exception as e:
        print(e.__doc__)
