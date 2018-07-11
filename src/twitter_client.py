import configparser
from src import helpers as h
import os
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
# import tweepy
# from tweepy.streaming import StreamListener
# from tweepy import Stream
# import time
# import json


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

# def get_twitter_auth():
#     """Setup Twitter authentication.
#     Return: tweepy.OAuthHandler object
#     """
#     try:
#         consumer_key = config.TWITTER_CONFIG['consumer_key']
#         consumer_secret = config.TWITTER_CONFIG['consumer_secret']
#         access_token = config.TWITTER_CONFIG['access_token_key']
#         access_secret = config.TWITTER_CONFIG['access_token_secret']
#     except KeyError:
#         sys.stderr.write("TWITTER_* environment variables not set\n")
#         sys.exit(1)
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_secret)
#     return auth

# def get_twitter_auth():
#     """Setup Twitter authentication.
#     Return: tweepy.OAuthHandler object
#     """
#     try:
#         config_file = configparser.ConfigParser()
#         config_file.read('./config.ini')
#         config = config_file['DEFAULT']
#     except KeyError:
#         sys.stderr.write("TWITTER_* environment variables not set\n")
#         sys.exit(1)
#     auth = OAuthHandler(config['ConsumerKey'], config['ConsumerSecret'])
#     auth.set_access_token(config['AccessTokenKey'], config['AccessTokenSecret'])
#     return auth
#
# def get_twitter_client():
#     """Setup Twitter API client.
#     Return: tweepy.API object
#     """
#     auth = get_twitter_auth()
#     client = API(auth)
#     return client


# def get_twitter_client():
#     """Setup Twitter API client.
#     Return: tweepy.API object
#     """
#     auth = get_twitter_auth()
#     client = API(auth)
#     return client


# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             time.sleep(15 * 60)


# def get_tweets(phrase, num_tweets, cache=False, fetch_new=False):
#     # looking for cache
#     cached_tweets = h.load_output(phrase, path='output/tweets')
#
#     if cached_tweets and not fetch_new:
#         return cached_tweets
#
#     # query phrase to fetch tweets
#     query_results = Cursor(get_twitter_client().search, q=phrase, lang="en").items(num_tweets)
#
#     # construct tweets dictionary
#     tweets = {tweet.id: tweet._json for tweet in query_results}
#
#     # merge cached and recent tweets if there are any
#     if cached_tweets:
#         tweets = {**tweets, **cached_tweets}
#
#     # casting key to int in order to silent sorting error
#     tweets = {int(k): v for k, v in tweets.items()}
#
#     if cache:
#         h.dump_output(tweets, phrase, path='output/tweets')
#
#     return tweets


# def get_user_tweets(user, num_tweets, cache=False, fetch_new=False):
#     # looking for cache
#     cached_tweets = h.load_output(user, path='output/user')
#
#     if cached_tweets and not fetch_new:
#         return cached_tweets
#
#     page_count = 1
#     if num_tweets > 200:
#         page_count = int(num_tweets / 200) + 1
#         num_tweets = 200
#
#     # query phrase to fetch tweets
#     query_results = Cursor(get_twitter_client().user_timeline, screen_name=user, count=num_tweets).pages(page_count)
#
#     # construct tweets dictionary
#     tweets = {tweet.id: tweet._json for page in query_results for tweet in page}
#
#     # merge cached and recent tweets if there are any
#     if cached_tweets:
#         tweets = {**tweets, **cached_tweets}
#
#     # casting key to int in order to silent sorting error
#     tweets = {int(k): v for k, v in tweets.items()}
#
#     if cache:
#         h.dump_output(tweets, user, path='output/user')
#
#     return tweets
#
#
# class TwitterListener(StreamListener):
#     def __init__(self, num_tweets=100):
#         self.counter = 0
#         self.num_tweets = num_tweets
#
#     def on_data(self, data):
#         try:
#             j = json.loads(data)
#             print('='*40)
#             print(j["text"])
#             self.counter += 1
#             if self.counter == self.num_tweets:
#                 return False
#             return True
#         except:
#             pass
#
#     def on_error(self, status):
#         print(status)
#
#
# def get_stream(phrase, phrase_count=100):
#     twitter_stream = Stream(get_twitter_auth(), TwitterListener(num_tweets=phrase_count))
#     try:
#         twitter_stream.filter(track=[phrase], async=True)
#     except Exception as e:
#         print(e.__doc__)
