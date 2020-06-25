from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
from tia.forms import StalkForm
from tia.stalk.user import User
from tia.stalk.profile_info import *
from tia.stalk.predictive_models import *
from tia.stalk.visualize import *
import os

app = Flask(__name__, static_url_path="/static")
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

USERNAME = ""
lang = ""


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    global USERNAME, lang
    form = StalkForm()
    if form.validate_on_submit():
        USERNAME = form.username.data
        lang = form.language.data
        if lang == "tr":
            return redirect(url_for("get_report_tr"))
        elif lang == "en":
            return redirect(url_for("get_report_en"))
    return render_template("home.html", form=form)


# Separated the turkish-english part due to differences such as gender-predicting
# The english model predicts whether the user is male, female or brand
# The data for the turkish model only predicts whether the user is male or female
# Due to such problems, I created separate pages and routes for turkish and english

@app.route("/stalk/turkish")
def get_report_tr():
    user = User(USERNAME)
    user_data = {
        "username": user.username,
        "followers": len(get_followers(user)),
        "following": len(get_following(user)),
        "f2f": len(get_f2f(user)),
        "polarity_score": get_polarity_score_tr(user),
        "subjectivity_score": get_subjectivity_score_tr(user),
        "gender_prediction": get_gender_pred_tr(user),
        "top_mentions": get_top_mentions(user),
        "top_mentioned": get_top_user_mentioned(user),
        "wordclouds": create_wordclouds(user),
        "freq_date": plot_tweet_frequency_date(user),
        "freq_hours": plot_tweet_frequency_hours(user)
    }
    return render_template("results_tr.html", user_data=user_data)


@app.route("/stalk/english")
def get_report_en():
    user = User(USERNAME)
    user_data = {
        "username": user.username,
        "followers": len(get_followers(user)),
        "following": len(get_following(user)),
        "f2f": len(get_f2f(user)),
        "polarity_score": get_polarity_score_en(user),
        "subjectivity_score": get_subjectivity_score_en(user),
        "gender_prediction": get_gender_pred_en(user),
        "top_mentions": get_top_mentions(user),
        "top_mentioned": get_top_user_mentioned(user),
        "wordclouds": create_wordclouds(user),
        "freq_date": plot_tweet_frequency_date(user),
        "freq_hours": plot_tweet_frequency_hours(user),
        "polarity_date": plot_polarity_date_en(user),
        "polarity_hours": plot_polarity_hourly_en(user),
        "subjectivity_date": plot_subjectivity_date_en(user),
        "subjectivity_hours": plot_subjectivity_hourly_en(user)
    }
    return render_template("results_en.html", user_data=user_data)
