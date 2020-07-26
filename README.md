# TIA - Your Advanced Twitter stalking tool
![GitHub license](https://img.shields.io/badge/python-v3.7-blue)
![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)

![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)

TIA uses machine learning models to create an advanced stalking report. If the user has
a public Twitter account, the rest is easy for TIA. (Twint package is used in the data
gathering process.)

**Contact me at u.kaanusta@gmail.com for any personal/business inquiries or if you want to contribute.** 

# What does TIA do?
- Predicts the gender of a user based on their tweets (TR/EN)
- Shows the positivity/negativity in user's tweets with a score (TR/EN)
- Shows the subjectivity in user's tweets with a score (TR/EN)
- Shows the user's most frequent mentions (TR/EN)
- Creates word clouds from the user's tweets and tweets to the user (TR/EN)
- Creates date-wise/hourly plots for the user's **tweeting frequency** (TR/EN)
- Creates date-wise/hourly plots for the user's **polarity(sentiment)** (EN)
- Creates date-wise/hourly plots for the user's **subjectivity** (EN)

# Demo video
![TIA v0.1 Demo](https://i.imgur.com/4g8K1Sa.gif)

# How can I install?
- Git clone
- Download the needed packages used in the project, PyCharm will help you on that
- Change the URL_ROOT variable in tia/stalk/init.py
- Scrape the user with scrape_user.py script
- Run run.py

## Issues/Warnings
- The script scrape_user.py gives an ImportError in Linux since TIA is written in Windows.
  - Contributions are welcome to solve the issue!
