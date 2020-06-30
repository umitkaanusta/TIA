# Utilities for functions in scrape.py
from textblob import TextBlob
import time
import numpy as np
from nltk.stem import PorterStemmer
from nltk import word_tokenize


def tweets_to_string(df):
    # Gets a tweets dataframe, and converts it to a single string to be used in creating wordclouds
    tw_str = ""
    remove = "'.,?:;@1234567890-_=/!()[]{}&%+^$€~`₺£<>|*¨"
    for tweet in df["tweet"]:
        tw_str += tweet + " "
    tw_str = tw_str.lower()
    for char in remove:
        tw_str = tw_str.replace(char, "")
    return tw_str


def txt_to_list(path):
    # Reads a txt file's each line, puts it in a list
    f = open(path, "r", encoding="utf-8")
    txt_list = f.read().split()
    return txt_list


def get_polarity_en(text):
    # Gets polarity for a text (EN)
    # What's polarity? - Check get_polarity_score_en method under predictive_models.py
    return TextBlob(text).sentiment.polarity


def get_subjectivity_en(text):
    # Gets subjectivity for a text (EN)
    # What's subjectivity? - Check get_subjectivity_score_en method under predictive_models.py
    return TextBlob(text).sentiment.subjectivity


def get_hours(tweet_time):
    return int(tweet_time[0:2])


def stemming_tokenizer(text):
    # This is here for nlp models (will be relocated)
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]
