from tia.stalk import URL_ROOT
from tia.stalk.user import User
from tia.stalk.util import txt_to_list, tweets_to_string, get_polarity_en, get_subjectivity_en, get_hours
from tia.stalk.profile_info import get_tweets, get_mentioned
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from wordcloud import WordCloud, STOPWORDS


def create_wordclouds(user):
    # Returns the path for wordclouds for tweets and mentioned
    path_tw = f"{URL_ROOT}static/images/{user.username}_tw_wordcloud.png"
    path_ment = f"{URL_ROOT}static/images/{user.username}_ment_wordcloud.png"
    path_stopwords_tr = f"{URL_ROOT}models/datasets/stopwords-tr.txt"
    stopwords_tr = txt_to_list(path_stopwords_tr) \
        + ["bi", "var", "yok", "sadece", "bence", "sence", "bi", "evet", "hayır", "peki", "tamam",
            "başka", "aynı", "lazım", "yav", "lan", "la", "olm"]
    stopwords_tr_en = list(STOPWORDS) + stopwords_tr
    if os.path.isfile(path_tw):
        os.remove(path_tw)
    if os.path.isfile(path_ment):
        os.remove(path_ment)
    tw_str = tweets_to_string(get_tweets(user))
    ment_str = tweets_to_string(get_mentioned(user))
    cloud_tw = WordCloud(stopwords=set(stopwords_tr_en))
    cloud_tw.generate(tw_str)
    cloud_tw.to_file(path_tw)
    ment_tw = WordCloud(stopwords=set(stopwords_tr_en))
    ment_tw.generate(ment_str)
    ment_tw.to_file(path_ment)
    return {"tweet_wordcloud": path_tw, "ment_wordcloud": path_ment}


def plot_tweet_frequency_date(user):
    # Returns a plot showing the frequency of last 500 tweets with respect to date
    # The scale of the date changes according to the tweet frequency of the user
    path = f"{URL_ROOT}/static/images/{user.username}_frequency_date.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    first_date, last_date = pd.to_datetime(df["date"].iloc[-1]), pd.to_datetime(df["date"].iloc[0])
    date_range = pd.date_range(first_date, last_date).tolist()
    daily_tweet_count = []
    for date in date_range:
        daily_tweet_count.append(len(df[pd.to_datetime(df["date"]) <= date]))
    plt.plot(date_range, daily_tweet_count)
    plt.title("Tweeting frequency for the last 500 tweets")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.ylabel("Total number of tweets")
    plt.tight_layout(h_pad=9, w_pad=8)
    plt.savefig(path)
    plt.clf()
    return path


def plot_tweet_frequency_hours(user):
    # Plots tweet frequency of last 500 tweets within 24h scale
    path = f"{URL_ROOT}/static/images/{user.username}_frequency_hourly.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    time_list = list(df["time"])
    counts = [0] * 24
    hours = np.arange(0, 24, 1)
    for t in time_list:
        counts[int(str(t)[0:2])] += 1
    plt.bar(hours, counts)
    plt.title("Tweeting frequency within 24h scale (for the last 500 tweets)")
    plt.xticks(hours)
    plt.xlabel("Hours (00:00 to 23:00)")
    plt.ylabel("Number of tweets")
    plt.savefig(path)
    plt.clf()
    return path


def plot_polarity_date_en(user):
    path = f"{URL_ROOT}/static/images/{user.username}_polarity_date.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    polarity = df["tweet"].apply(get_polarity_en)
    polarity = polarity.apply(lambda x: x * 100)
    plt.bar(df["date"][::-1], polarity)
    plt.title("Polarity score for the last 500 tweets")
    plt.xticks([df["date"].iloc[-1], df["date"].iloc[0]], rotation=90)
    plt.yticks(np.arange(-100, 110, 10))
    plt.xlabel("Date")
    plt.ylabel("Polarity score")
    plt.tight_layout(h_pad=9, w_pad=8)
    plt.savefig(path)
    plt.clf()
    return path


def plot_polarity_hourly_en(user):
    path = f"{URL_ROOT}/static/images/{user.username}_polarity_hourly.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    df["polarity"] = df["tweet"].apply(get_polarity_en)
    df["polarity"] = df["polarity"].apply(lambda x: x * 100)
    df["hour"] = df["time"].apply(get_hours)
    hours = np.arange(0, 24, 1)
    sums = [0] * 24
    counts = [0] * 24
    for t in list(df["time"]):
        counts[int(str(t)[0:2])] += 1
    for i in range(0, len(df)):
        sums[int(str(df["time"].iloc[i][0:2]))] += df["polarity"].iloc[i]
    # To avoid zero-division:
    for i in range(0, len(counts)):
        if counts[i] == 0:
            counts[i] += 1
    means = np.array(sums) / np.array(counts)
    plt.scatter(df["hour"], df["polarity"], alpha=0.50)
    plt.plot(hours, means, color="red")
    plt.title("Distribution of polarity score within 24h scale")
    plt.xticks(hours)
    plt.yticks(np.arange(-100, 110, 10))
    plt.xlabel("Hours (00:00 - 23:00)")
    plt.ylabel("Average polarity score")
    plt.savefig(path)
    plt.clf()
    return path


def plot_subjectivity_date_en(user):
    path = f"{URL_ROOT}/static/images/{user.username}_subjectivity_date.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    subjectivity = df["tweet"].apply(get_subjectivity_en)
    subjectivity = subjectivity.apply(lambda x: x * 100)
    plt.bar(df["date"][::-1], subjectivity)
    plt.title("Subjectivity score for the last 500 tweets")
    plt.xticks([df["date"].iloc[-1], df["date"].iloc[0]], rotation=90)
    plt.yticks(np.arange(0, 110, 10))
    plt.xlabel("Date")
    plt.ylabel("Subjectivity score")
    plt.tight_layout(h_pad=9, w_pad=8)
    plt.savefig(path)
    plt.clf()
    return path


def plot_subjectivity_hourly_en(user):
    path = f"{URL_ROOT}/static/images/{user.username}_subjectivity_hourly.png"
    if os.path.isfile(path):
        os.remove(path)
    df = get_tweets(user)
    df["subjectivity"] = df["tweet"].apply(get_subjectivity_en)
    df["subjectivity"] = df["subjectivity"].apply(lambda x: x * 100)
    df["hour"] = df["time"].apply(get_hours)
    hours = np.arange(0, 24, 1)
    sums = [0] * 24
    counts = [0] * 24
    # Implementing df.groupby manually to avoid NaN values that are caused by df.groupby in this case
    for t in list(df["time"]):
        counts[int(str(t)[0:2])] += 1
    for i in range(0, len(df)):
        sums[int(str(df["time"].iloc[i][0:2]))] += df["subjectivity"].iloc[i]
    # To avoid zero-division:
    for i in range(0, len(counts)):
        if counts[i] == 0:
            counts[i] += 1
    means = np.array(sums) / np.array(counts)
    plt.scatter(df["hour"], df["subjectivity"], alpha=0.50)
    plt.plot(hours, means, color="red")
    plt.title("Distribution of subjectivity score within 24h scale")
    plt.xticks(hours)
    plt.yticks(np.arange(0, 100, 10))
    plt.xlabel("Hours (00:00 - 23:00)")
    plt.ylabel("Average subjectivity score")
    plt.savefig(path)
    plt.clf()
    return path
