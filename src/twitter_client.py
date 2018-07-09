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


def get_tweets(phrase, tweets_count, dump=False):
    # first check for existing output file
    output = h.load_output(phrase)
    if output:
        return output

    results = Cursor(get_twitter_client().search, q=phrase, lang="en").items(tweets_count)

    tweets = {tweet.id:tweet._json for tweet in results}

    if dump:
        h.dump_output(tweets, phrase)

    return tweets




