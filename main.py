import re
import pandas as pd
import numpy as np
import seaborn as sns
import string
import nltk
from nltk.stem.porter import *

train = pd.read_csv('/Users/mundiaem/PycharmProjects/twitter-sentiments/train_E6oV3lV.csv')

print(train.head())


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


print('\n\nRemoving  Twitter Handles \n\n')
train['tidy_tweet'] = np.vectorize(remove_pattern)(train['tweet'], "@[\w]*")

print(train['tidy_tweet'].head())

print('\n\nRemoving Short Words\n\n')

train['tidy_tweet'] = train['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))

print(train['tidy_tweet'].head())

print('\n\nTweet Tokenization\n\n')
tokenized_tweet = train['tidy_tweet'].apply(lambda x: x.split())
print(tokenized_tweet.head())

print('\n\nStemming\n\n')

stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])
# stemming
print(tokenized_tweet.head())

