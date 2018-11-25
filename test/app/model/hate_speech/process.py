from classifier import get_tweets_predictions
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import os
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from textstat.textstat import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VS
import nltk.data


class Analyzer(object):
    def __init__(self, ):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        self.model = joblib.load(os.path.join(cur_path, 'final_model.pkl'))
        self.tf_vectorizer = joblib.load(os.path.join(cur_path, 'final_tfidf.pkl'))
        self.idf_vector = joblib.load(os.path.join(cur_path, 'final_idf.pkl'))
        self.pos_vectorizer = joblib.load(os.path.join(cur_path, 'final_pos.pkl'))

        self.stemmer = PorterStemmer()
        self.sentiment_analyzer = VS()

    @staticmethod
    def preprocess(text_string):
        """
        Accepts a text string and replaces:
        1) urls with URLHERE
        2) lots of whitespace with one instance
        3) mentions with MENTIONHERE

        This allows us to get standardized counts of urls and mentions
        Without caring about specific people mentioned
        """
        space_pattern = '\s+'
        giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                           '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        mention_regex = '@[\w\-]+'
        parsed_text = re.sub(space_pattern, ' ', text_string)
        parsed_text = re.sub(giant_url_regex, 'URLHERE', parsed_text)
        parsed_text = re.sub(mention_regex, 'MENTIONHERE', parsed_text)
        # parsed_text = parsed_text.code("utf-8", errors='ignore')
        return parsed_text

    def tokenize(self, tweet):
        """Removes punctuation & excess whitespace, sets to lowercase,
        and stems tweets. Returns a list of stemmed tokens."""
        tweet = " ".join(re.split("[^a-zA-Z]*", tweet.lower())).strip()
        # tokens = re.split("[^a-zA-Z]*", tweet.lower())
        tokens = [self.stemmer.stem(t) for t in tweet.split()]
        return tokens

    @staticmethod
    def basic_tokenize(tweet):
        """Same as tokenize but without the stemming"""
        tweet = " ".join(re.split("[^a-zA-Z.,!?]*", tweet.lower())).strip()
        return tweet.split()

    def get_pos_tags(self, contents):
        tweet_tags = []
        for t in contents:
            tokens = self.basic_tokenize(self.preprocess(t))
            tags = nltk.pos_tag(tokens)
            tag_list = [x[1] for x in tags]
            # for i in range(0, len(tokens)):
            tag_str = " ".join(tag_list)
            tweet_tags.append(tag_str)
        return tweet_tags

    def other_features_(self, tweet):
        """This function takes a string and returns a list of features.
        These include Sentiment scores, Text and Readability scores,
        as well as Twitter specific features.

        This is modified to only include those features in the final
        model."""

        sentiment = self.sentiment_analyzer.polarity_scores(tweet)

        words = self.preprocess(tweet)  # Get text only

        syllables = textstat.syllable_count(words)  # count syllables in words
        num_chars = sum(len(w) for w in words)  # num chars in words
        num_chars_total = len(tweet)
        num_terms = len(tweet.split())
        num_words = len(words.split())
        avg_syl = round(float((syllables + 0.001)) / float(num_words + 0.001), 4)
        num_unique_terms = len(set(words.split()))

        # Modified FK grade, where avg words per sentence is just num words/1
        FKRA = round(float(0.39 * float(num_words) / 1.0) + float(11.8 * avg_syl) - 15.59, 1)
        # Modified FRE score, where sentence fixed to 1
        FRE = round(206.835 - 1.015 * (float(num_words) / 1.0) - (84.6 * float(avg_syl)), 2)

        twitter_objs = self.count_twitter_objs(tweet)  # Count #, @, and http://
        features = [FKRA, FRE, syllables, num_chars, num_chars_total, num_terms, num_words,
                    num_unique_terms, sentiment['compound'],
                    twitter_objs[2], twitter_objs[1], ]
        # features = pandas.DataFrame(features)
        return features

    @staticmethod
    def count_twitter_objs(text_string):
        """
        Accepts a text string and replaces:
        1) urls with URLHERE
        2) lots of whitespace with one instance
        3) mentions with MENTIONHERE
        4) hashtags with HASHTAGHERE

        This allows us to get standardized counts of urls and mentions
        Without caring about specific people mentioned.

        Returns counts of urls, mentions, and hashtags.
        """
        space_pattern = '\s+'
        giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                           '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        mention_regex = '@[\w\-]+'
        hashtag_regex = '#[\w\-]+'
        parsed_text = re.sub(space_pattern, ' ', text_string)
        parsed_text = re.sub(giant_url_regex, 'URLHERE', parsed_text)
        parsed_text = re.sub(mention_regex, 'MENTIONHERE', parsed_text)
        parsed_text = re.sub(hashtag_regex, 'HASHTAGHERE', parsed_text)
        return parsed_text.count('URLHERE'), parsed_text.count('MENTIONHERE'), parsed_text.count('HASHTAGHERE')

    def get_oth_features(self, tweets):
        """Takes a list of tweets, generates features for
        each tweet, and returns a numpy array of tweet x features"""
        feats = []
        for t in tweets:
            feats.append(self.other_features_(t))
        return np.array(feats)

    def transform_inputs(self, tweets):
        """
        This function takes a list of tweets, along with used to
        transform the tweets into the format accepted by the model.

        Each tweet is decomposed into
        (a) An array of TF-IDF scores for a set of n-grams in the tweet.
        (b) An array of POS tag sequences in the tweet.
        (c) An array of features including sentiment, vocab, and readability.

        Returns a pandas dataframe where each row is the set of features
        for a tweet. The features are a subset selected using a Logistic
        Regression with L1-regularization on the training data.

        """
        tf_array = self.tf_vectorizer.fit_transform(tweets).toarray()
        tfidf_array = tf_array * self.idf_vector
        print "Built TF-IDF array"

        pos_tags = self.get_pos_tags(tweets)
        pos_array = self.pos_vectorizer.fit_transform(pos_tags).toarray()
        print "Built POS array"

        oth_array = self.get_oth_features(tweets)
        print "Built other feature array"

        M = np.concatenate([tfidf_array, pos_array, oth_array], axis=1)
        return pd.DataFrame(M)

    def predictions(self, X):
        """
        This function calls the predict function on
        the trained model to generated a predicted y
        value for each observation.
        """
        return self.model.predict(X)

    def get_text_predictions(self, string, ignore_pos=True):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        string = tokenizer.tokenize(string)
        print string
        return self._text_predictions(string, ignore_pos=ignore_pos)

    def _text_predictions(self, content, ignore_pos=True):
        fixed_content = []
        for idx, t_orig in enumerate(content):
            s = t_orig
            try:
                s = s.encode("latin1")
            except:
                try:
                    s = s.encode("utf-8")
                except UnicodeEncodeError as e:
                    raise e

            if type(s) != unicode:
                fixed_content.append(unicode(s, errors="ignore"))
            else:
                fixed_content.append(s)
        content = fixed_content
        X = self.transform_inputs(content)

        predicted_class = self.predictions(X).tolist()
        if ignore_pos:
            result = [(content[idx], label) for idx, label in enumerate(predicted_class) if label != 2]
        else:
            result = [(content[idx], label) for idx, label in enumerate(predicted_class)]
        return result

    def get_url_predictions(self, url, ignore_pos=True):
        html = urlopen(url)
        soup = BeautifulSoup(html.read())
        data = []
        for string in soup.strings:
            string = " ".join(re.split("[^a-zA-Z.,!?]*", string.lower())).strip()
            data.append(string)
        return self._text_predictions(data, ignore_pos=ignore_pos)


class WordMasker(object):
    def __init__(self):
        # TODO true corpus
        self.corpus = {'fuck', 'dick'}

    def get_masked_text(self, text, mask='*'):
        res = map(lambda word: text.replace(word, mask * len(word)), self.corpus)
        return res


def analyze_content(_str):
    print 'warning, deprecated'
    _str = str(_str)
    html = urlopen(_str)
    soup = BeautifulSoup(html.read())
    data = []
    for string in soup.strings:
        string = " ".join(re.split("[^a-zA-Z.,!?]*", string.lower())).strip()
        data.append(string)
    return get_tweets_predictions(data).tolist()


if __name__ == '__main__':
    from classifier import tokenize as tokenize, preprocess
    test_str = "https://en.wikipedia.org/wiki/Twitter"
    print type(test_str)
    result = analyze_content(test_str)
    print result
    count = 0
    for i in result:
        count = count + 1
        if i != 2:
            print i, count
