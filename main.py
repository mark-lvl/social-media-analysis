import sys
import src.twitter_client as api_client
import src.sentiment as sentiment
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='main',
                                     usage='%(prog)s func [options]',
                                     description='Tweets analysis')
    parser.add_argument(
        'func',
        choices=['sentiment',
                 'user',
                 'stream'],
        help='choose the method to call')

    args = parser.parse_args()

    if args.func == 'sentiment':
        # input for term to be searched and how many tweets to search
        phrase = input("Enter Keyword/Tag to search about: ")
        phrase_count = int(input("Enter how many tweets to search: "))

        tweets, percentages = sentiment.sentiment_analysis(api_client.get_tweets(phrase,
                                                                                 phrase_count,
                                                                                 cache=True,
                                                                                 fetch_new=False))

        # print percentages in console and draw graph
        sentiment.sentiment_report(percentages, graph=True, phrase=phrase, phrase_count=len(tweets))

    if args.func == 'user':
        # input for term to be searched and how many tweets to search
        user = input("Enter user name to search about: ")
        phrase_count = int(input("Enter how many tweets to search: "))
        fetch_new = int(input("Fetching new tweets and append to cache?"))

        tweets = api_client.get_user_tweets(user, phrase_count, cache=True, fetch_new=fetch_new)

        print(len(tweets))
        # for tweet_id, tweet in tweets.items():
        #     print(tweet_id, ":", tweet['text'])

    if args.func == 'stream':
        phrase = input("Enter Keyword/Tag to live search about: ")
        api_client.get_stream(phrase)