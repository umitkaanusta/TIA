# Using this script to create gender_model_en.pkl to avoid errors caused by
# turning ipynb to pickle.
#
# See gender_model_en.ipynb to better understand the reasoning of the code below.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import string
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from tia.stalk.util import stemming_tokenizer
import pickle

df = pd.read_csv("C:/Users/Ümit/PycharmProjects/TIA/tia/models/datasets/twitter_gender.csv", encoding="latin")
df = df[["text", "gender"]]
df = df.loc[df["gender"].isin(["male", "female", "brand"])]

df.dropna(inplace=True)
df.reset_index(inplace=True)

X = df[["text"]]
y = df[["gender"]]

nltk.download("punkt")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

gender_model_en = Pipeline([('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer)),
                            ('classifier', LogisticRegression())])
gender_model_en.fit(X["text"], y["gender"])

pickle.dump(gender_model_en, open("gender_model_en.pkl", "wb"))
