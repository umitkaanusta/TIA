from tia.stalk import URL_ROOT
from tia.stalk.user import User
from tia.stalk.util import txt_to_list
import pandas as pd


def get_following(user):
    # Returns a list - won't be used in this version
    path = f"{URL_ROOT}stalk/{user.dir_name}/following.txt"
    return txt_to_list(path)


def get_followers(user):
    # won't be used in this version
    path = f"{URL_ROOT}stalk/{user.dir_name}/followers.txt"
    return txt_to_list(path)


def get_f2f(user):
    # Gets users both in followers and followed
    following = get_following(user)
    followers = get_followers(user)
    f2f = list(set(following).intersection(followers))
    return f2f


def get_tweets(user):
    # Returns a pandas dataframe of tweets of the given user
    path = f"{URL_ROOT}stalk/{user.dir_name}/tweets.csv"
    df = pd.read_csv(path)
    return df


def get_mentioned(user):
    # Returns tweets you're mentioned in as a pandas df
    path = f"{URL_ROOT}stalk/{user.dir_name}/mentioned.csv"
    df = pd.read_csv(path)
    df = df[df["username"] != user.username.lower()].iloc[0:500]
    return df


def get_top_mentions(user):
    # Returns top 5 mentioned users as a list
    mention_list = []
    mentions = get_tweets(user)["mentions"]
    # Converting string representation of list to an actual list
    for _, val in mentions.items():
        val = val.strip("][' ").split(", ")
        for user in val:
            if user != "":
                mention_list.append(user.strip("'"))
    top_users = list(pd.Series(mention_list).value_counts().iloc[0:5].index)
    # First converted mention_list to pandas series to get the value counts
    # Then indexed the top 5 and got their usernames
    # Then reconverted to list
    return top_users


def get_top_user_mentioned(user):
    # Returns top 5 users mentioned you as a list
    mentions = get_mentioned(user)
    mentions = mentions.loc[mentions["username"] != user.username.lower()]
    mentions = mentions["username"]
    top_users = list(mentions.value_counts().iloc[0:5].index)
    return top_users
