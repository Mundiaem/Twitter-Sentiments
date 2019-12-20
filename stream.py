import re
import sys

import tweepy
# authorization tokens
from textblob import TextBlob

consumer_key = "nncHfvEB8YChjTS0dXY5Lqgih"
consumer_secret = "boF0r6XawJKr1aP75Fwh9MnJspEO3d6f0ifr02z2or40cTy0sk"
access_key = "1862787229-YQWKemIrdFLZ8DHMxJHK8cMRN7igzKjiUTCi5ly"
access_secret = "3A7FZuoAz2WfGv3Gm9homkAD8G5bqa9FQeymlWCO7I3Xu"

num = 0


def generate_incrementer(start):
    num = start

    def incrementer():
        nonlocal num
        num += 1
        return num

    return incrementer


# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+) |(?<!\s[\dA-Z]),(?!\s+\d,?)", " ",
                               tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def on_status(self, status):

        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        tweet = self.clean_tweet(text)
        count = 1
        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s\n" % (status.id_str, self.get_tweet_sentiment(tweet), tweet))
            count += 1

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    with open("out.csv", "w", encoding='utf-8') as f:
        f.write("id,label,tweet\n")
    tags = ["hate speech"]
    stream.filter(track=tags)
