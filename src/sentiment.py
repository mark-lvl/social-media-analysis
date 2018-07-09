from textblob import TextBlob
import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt


def sentiment_analysis(tweets):

    output = {}
    neutral = 0
    positive = 0
    negative = 0

    for tweet_id, tweet in tweets.items():

        analysis = TextBlob(tweet['text'])

        if -0.2 <= analysis.sentiment.polarity <= 0.2:
            neutral += 1
        elif analysis.sentiment.polarity > 0.2:
            positive += 1
        elif analysis.sentiment.polarity < -0.2:
            negative += 1

        output[tweet['text']] = analysis.polarity

    percentage = namedtuple('Percentage', ['negative', 'neutral', 'positive'])

    return output, percentage(negative=negative/len(tweets), positive=positive/len(tweets), neutral=neutral/len(tweets))


def sentiment_report(percentages, graph=False, **kwargs):
    print()
    print("Detailed Report: ")
    print('Positive:{0:.2f}'.format(percentages.positive))
    print('Neutral:{0:.2f}'.format(percentages.neutral))
    print('Negative:{0:.2f}'.format(percentages.negative))

    if graph:
        labels = ['Negative', 'Neutral', 'Positive']
        sizes = list(percentages)
        colors = ['red', 'gray', 'green']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + kwargs['phrase'] + ' by analyzing ' +
                  str(kwargs['phrase_count']) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()