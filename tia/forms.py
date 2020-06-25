from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class StalkForm(FlaskForm):
    username = StringField("",
                           validators=[DataRequired(message="This field must be filled")],
                           render_kw={"placeholder": "Enter a Twitter username without @"})
    language = SelectField("Language of the tweets",
                           choices=[("en", "English"), ("tr", "Turkish")],
                           validators=[DataRequired(message="This field must be filled")])
    submit = SubmitField("Stalk")

