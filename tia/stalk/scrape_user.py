from tia.stalk import URL_ROOT
from tia.stalk.user import User
import twint as tw
import os
import shutil
import time

# Currently scrape_user.py is not used in the app, you can use this as a supplementary script to get the necessary
# files to stalk your target.


def create_user_dir(user):
    # Creates a folder like jack_username
    # The folder will contain the tweets and favorites of the given user
    current = os.getcwd()
    path = os.path.join(current, user.dir_name)
    try:
        os.makedirs(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.makedirs(path)


def get_following_txt(user):
    path = f"{URL_ROOT}stalk/{user.dir_name}/following.txt"
    if os.path.isfile(path):
        os.remove(path)
    c = tw.Config
    c.Username = user.username
    c.Output = path
    c.Format = ""
    tw.run.Following(c)


def get_followers_txt(user):
    path = f"{URL_ROOT}stalk/{user.dir_name}/followers.txt"
    if os.path.isfile(path):
        os.remove(path)
    c = tw.Config
    c.Username = user.username
    c.Output = path
    c.Format = ""
    tw.run.Followers(c)


def get_tweets_csv(user):
    # Get last 500 tweets of the user
    path = f"{URL_ROOT}stalk/{user.dir_name}/tweets.csv"
    if os.path.isfile(path):
        os.remove(path)
    c = tw.Config
    c.Username = user.username
    c.Store_csv = True
    c.Limit = 500
    c.Format = "-"
    c.Output = path
    tw.run.Search(c)


# Twint does not scrape favs for now, this will be "activated" later
# def get_favs_csv(user):
#    path = f"{URL_ROOT}stalk/{user.dir_name}/favs.csv"
#    if os.path.isfile(path):
#        os.remove(path)
#    c = tw.Config
#    c.Username = user.username
#    c.Store_csv = True
#    c.Limit = 500
#    c.Format = "-"
#    c.Output = path
#    tw.run.Favorites(c)


def get_user_mentioned_csv(user):
    # c.To returns tweets that are tweeted by the user themself as well
    # Therefore I removed c.Limit as a band-aid solution
    # This issue will be considered in future updates
    path = f"{URL_ROOT}stalk/{user.dir_name}/mentioned.csv"
    if os.path.isfile(path):
        os.remove(path)
    c = tw.Config
    c.To = user.username
    c.Store_csv = True
    c.Format = "-"
    c.Output = path
    tw.run.Search(c)


def scrape_user(user):
    create_user_dir(user)
    get_following_txt(user)
    time.sleep(60)  # We put time.sleep() to avoid suspicious requesting
    get_followers_txt(user)
    time.sleep(60)
    get_tweets_csv(user)
    time.sleep(60)
    get_user_mentioned_csv(user)
    time.sleep(60)


# How to use the script?
# Create a user instance with the username, like uka = User("umitkaanusta")
# Then scrape_user(uka)
#
# Sometimes problems occur due to the Twint library.
# In that case, execute the functions in scrape_user step by step.
#
# Successful case:
# umitkaanusta_scraped /
#   following.txt
#   followers.txt
#   tweets.csv
#   mentioned.csv
