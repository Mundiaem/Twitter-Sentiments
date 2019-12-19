import csv
import re

import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "nncHfvEB8YChjTS0dXY5Lqgih"
        consumer_secret = "boF0r6XawJKr1aP75Fwh9MnJspEO3d6f0ifr02z2or40cTy0sk"
        access_token = "1862787229-YQWKemIrdFLZ8DHMxJHK8cMRN7igzKjiUTCi5ly"
        access_token_secret = "3A7FZuoAz2WfGv3Gm9homkAD8G5bqa9FQeymlWCO7I3Xu"

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+) ", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query='Kenya', count=1000)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # picking neautral tweets
    neautraltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    neutral_tweets = (len(tweets) - len(ntweets) - len(ptweets))
    print("Neutral tweets percentage: {} % ".format(100 * neutral_tweets / len(tweets)))
    csv_rowlist = [["id", "label", "tweet"]]
    p = 1
    with open('protagonist.csv', 'w+') as file:
        file.close()
    for tweet in ptweets:
        csv_rowlist.append([p, 1, tweet['text']])
        with open('protagonist.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_rowlist)
            p += 1
    for tweet in ntweets:
        csv_rowlist.append([p, -1, tweet['text']])
        with open('protagonist.csv', 'w') as file:
            writer = csv.writer(file)

            writer.writerows(csv_rowlist)
            p += 1
    for tweet in neautraltweets:
        csv_rowlist.append([p, 0, tweet['text']])
        with open('protagonist.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_rowlist)
            p += 1

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")

    for tweet in ptweets[:1000]:
        print("{} {}".format(p, tweet['text']))

    # printing first 5 neutral tweets
    print("\n\nNeutral tweets:")
    ne = 1

    for tweet in neautraltweets[:1000]:
        print("{}  {}".format(ne, tweet['text']))

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    n = 1
    for tweet in ntweets[:1000]:
        print("{}  {}".format(n, tweet['text']))

        n += 1


if __name__ == "__main__":
    # calling main function
    main()
