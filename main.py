import sys
import src.twitter_client as tw
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

    twitter = tw.Twitter()

    if args.func == 'sentiment':
        # input for term to be searched and how many tweets to search
        term = input("Enter Keyword/Tag to search about: ")
        num_tweets = int(input("Enter how many tweets to search: "))
        read_from_cache = bool(int(input("Reading from cache?")))

        tweets, percentages = sentiment.sentiment_analysis(twitter.search_tweets(term,
                                                                                 num_tweets,
                                                                                 export=True,
                                                                                 cache_only=read_from_cache))

        # print percentages in console and draw graph
        sentiment.sentiment_report(percentages, graph=True, phrase=term, phrase_count=len(tweets))

    elif args.func == 'user':
        # input for term to be searched and how many tweets to search
        user = input("Enter user name to search about: ")
        num_tweets = int(input("Enter how many tweets to search: "))
        read_from_cache = bool(int(input("Reading from cache?")))

        tweets = twitter.fetch_user_tweets(user,
                                           num_tweets,
                                           export=True,
                                           cache_only=read_from_cache)

        print(len(tweets))
        for tweet_id, tweet in tweets.items():
            print(tweet_id, ":", tweet['text'])

    elif args.func == 'stream':
        term = input("Enter Keyword/Tag to live search about: ")
        num_tweets = int(input("Enter how many tweets to receive: "))
        twitter.get_stream_tweets(term, num_tweets)