from tia.stalk import URL_ROOT
from tia.stalk.profile_info import get_tweets
from tia.stalk.util import get_polarity_en, get_subjectivity_en, tweets_to_string
from tia.stalk.user import User
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob
from googletrans import Translator


def get_gender_pred_tr(user):
    # We only have male and female for the turkish model
    model_path = f"{URL_ROOT}models/tr/gender_model_tr.pkl"
    model = pickle.load(open(model_path, "rb"))
    tweets = tweets_to_string(get_tweets(user))
    gender_pred = model.predict_proba((pd.Series(tweets)))
    male_pred = gender_pred[:, 0]
    male_score = int(male_pred * 100)
    female_score = 100 - male_score
    return {"male": male_score, "female": female_score}


def get_gender_pred_en(user):
    model_path = f"{URL_ROOT}models/en/gender_model_en.pkl"
    model = pickle.load(open(model_path, "rb"))
    tweets = tweets_to_string(get_tweets(user))
    gender_pred = model.predict_proba((pd.Series(tweets)))
    male_pred = gender_pred[:, 0]
    brand_pred = gender_pred[:, 2]
    male_score = int(male_pred * 100)
    brand_score = int(brand_pred * 100)
    female_score = 100 - male_score - brand_score
    return {"male": male_score, "female": female_score, "brand": brand_score}


def get_polarity_score_en(user):
    # Gets polarity score (is the tweet negative, positive or neutral?) for EN tweets
    # -100 is the negative end, 100 is the positive end
    tweets = get_tweets(user)
    tweets_text = tweets_to_string(tweets)
    return int(TextBlob(tweets_text).sentiment.polarity * 100)


def get_subjectivity_score_en(user):
    # Gets subjectivity score for EN tweets
    # 0 is the factual end, 100 is the subjective end
    tweets = get_tweets(user)
    tweets_text = tweets_to_string(tweets)
    return int(TextBlob(tweets_text).sentiment.subjectivity * 100)


def get_polarity_score_tr(user):
    # Gets polarity score for TR tweets
    # -100 is the negative end, 100 is the positive end
    tr = Translator()
    score = 0
    tweets = get_tweets(user)
    tweets_text = tweets_to_string(tweets)
    text_list = []
    for i in range(0, len(tweets_text), 15000):
        text_list.append(tweets_text[i: i + 15000])
    translations = tr.translate(text_list)
    for translation in translations:
        score += int(TextBlob(translation.text).sentiment.polarity * 100)
    score = int(score / len(text_list))
    return score


def get_subjectivity_score_tr(user):
    # Gets subjectivity score for TR tweets
    # -100 is the negative end, 100 is the positive end
    tr = Translator()
    score = 0
    tweets = get_tweets(user)
    tweets_text = tweets_to_string(tweets)
    text_list = []
    for i in range(0, len(tweets_text), 15000):
        text_list.append(tweets_text[i: i + 15000])
    translations = tr.translate(text_list)
    for translation in translations:
        score += int(TextBlob(translation.text).sentiment.subjectivity * 100)
    score = int(score / len(text_list))
    return score
