from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt


def sentiment_analysis(tweets):

    output = {}
    neutral = 0
    positive = 0
    negative = 0

    for tweet_id, tweet in tweets.items():

        # analysis = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
        #
        # if analysis.sentiment.p_pos >= 0.6:
        #     positive += 1
        # elif analysis.sentiment.p_neg >= 0.6:
        #     negative += 1
        # else:
        #     neutral += 1
        #
        # output[tweet['text']] = analysis.sentiment.p_pos

        analysis = TextBlob(tweet['text'])
        if -0.1 <= analysis.sentiment.polarity <= 0.1:
            neutral += 1
        elif analysis.sentiment.polarity > 0.1:
            positive += 1
        elif analysis.sentiment.polarity < -0.1:
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
        patches, texts, pct = plt.pie(sizes,
                                      colors=colors,
                                      startangle=90,
                                      autopct='%1.1f%%')
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + kwargs['phrase'] + ' by analyzing ' +
                  str(kwargs['phrase_count']) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
