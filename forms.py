from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    query = StringField("Search:", validators=[InputRequired()])
    submit = SubmitField("Search")