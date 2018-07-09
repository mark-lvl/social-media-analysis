from textblob import TextBlob
import numpy as np


def sentiment_analysis(data):

    output = {}
    neutral = 0
    positive = 0
    negative = 0


    for tweet_id, tweet in data.items():

        analysis = TextBlob(tweet['text'])

        # print(analysis.sentiment)  # print tweet's polarity
        # polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
        #

        if -0.2 <= analysis.sentiment.polarity <= 0.2:
            neutral += 1
        elif analysis.sentiment.polarity > 0.2:
            positive += 1
        elif analysis.sentiment.polarity < -0.2:
            negative += 1

        output[tweet['text']] = analysis.polarity

    percentages = np.array([negative, neutral, positive]) / len(data)

    return output, percentages
