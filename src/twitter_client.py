from src import config
from src import helpers as h
import sys
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
import tweepy
import time


def get_twitter_auth():
    """Setup Twitter authentication.
    Return: tweepy.OAuthHandler object
    """
    try:
        consumer_key = config.TWITTER_CONFIG['consumer_key']
        consumer_secret = config.TWITTER_CONFIG['consumer_secret']
        access_token = config.TWITTER_CONFIG['access_token_key']
        access_secret = config.TWITTER_CONFIG['access_token_secret']
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    """Setup Twitter API client.
    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


def get_tweets(phrase, tweets_count, cache=False, fetch_new=False):
    # looking for cache
    cached_tweets = h.load_output(phrase)

    if cached_tweets and not fetch_new:
        return cached_tweets

    # query phrase to fetch tweets
    query_results = Cursor(get_twitter_client().search, q=phrase, lang="en").items(tweets_count)

    # construct tweets dictionary
    tweets = {tweet.id:tweet._json for tweet in query_results}

    # merge cached and recent tweets if there are any
    if cached_tweets:
        tweets = {**tweets, **cached_tweets}

    # casting key to int in order to silent sorting error
    tweets = {int(k): v for k, v in tweets.items()}

    if cache:
        h.dump_output(tweets, phrase)

    return tweets




