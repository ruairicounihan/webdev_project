from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

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