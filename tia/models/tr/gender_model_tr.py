# Using this script to create gender_model_tr.pkl to avoid errors caused by
# turning ipynb to pickle.
#
# See gender_model_tr.ipynb to better understand the reasoning of the code below.

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

df = pd.read_csv("C:/Users/Ümit/PycharmProjects/TIA/tia/models/datasets/twitter_gender_tr.csv")
df.dropna(inplace=True)

X = df["text"]
y = df["Gender"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

nltk.download("punkt")

gender_model_tr = Pipeline([('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer)),
                             ('classifier', LogisticRegression())])
gender_model_tr.fit(X, y)

pickle.dump(gender_model_tr, open("gender_model_tr.pkl", "wb"))
