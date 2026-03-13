from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange

class SearchForm(FlaskForm):
    query = StringField("Search:", validators=[InputRequired()])
    submit = SubmitField("Search")
    
class RegistrationForm(FlaskForm):
    user_id = StringField("User id:",
                          validators=[InputRequired()])
    password = PasswordField("Password:",
                             validators=[InputRequired()])
    password2 = PasswordField("Confirm password:",
                              validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    user_id = StringField("User id:",
                          validators=[InputRequired()])
    password = PasswordField("Password:",
                             validators=[InputRequired()])
    submit = SubmitField("Submit")
    
    
class ReviewForm(FlaskForm):
    rating = IntegerField("Rate This Album:",
                          validators=[InputRequired(), NumberRange(0, 100)])
    comment = StringField("Leave A Comment:")
    submit = SubmitField("Submit")