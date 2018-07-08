import sys
import src.twitter_client as api_client
import time

# if __name__ == '__main__':
#     client = get_twitter_client()
#
#     with open('home_timeline.jsonl', 'w') as f:
#         for page in Cursor(client.home_timeline, count=200, include_rts=True).pages(4):
#             for status in page:
#                 # Process a single status
#                 f.write(json.dumps(status._json)+"\n")





if __name__ == '__main__':

    # input for term to be searched and how many tweets to search
    searchTerm = input("Enter Keyword/Tag to search about: ")
    NoOfTerms = int(input("Enter how many tweets to search: "))
    #
    tweets = api_client.get_tweets(searchTerm, NoOfTerms, dump=True)
    # output = {}
    # for tweet in tweets:
    #     output[tweet.id] = tweet._json

    for key, value in tweets.items():
        print(key, '\n', list(value))


    #api_client.friends()


    # t = Tweets()
    # t.get_user_timeline(sys.argv[1])

    # user = sys.argv[1]
    # client = get_twitter_client()
    #
    # fname = "user_timeline_{}.jsonl".format(user)
    # with open(fname, 'w') as f:
    #     for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
    #         for status in page:
    #             f.write(json.dumps(status._json)+"\n")user = sys.argv[1]
    # client = get_twitter_client()
    #
    # fname = "user_timeline_{}.jsonl".format(user)
    # with open(fname, 'w') as f:
    #     for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
    #         for status in page:
    #             f.write(json.dumps(status._json)+"\n")