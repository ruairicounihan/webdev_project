from flask import Flask, render_template, session, redirect, url_for
from database import get_db, close_db
from flask_session import Session
import crud
from forms import SearchForm

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)

@app.route("/search")
def search():
    db = get_db()
    albums = crud.search_all(db)
    titles = [album["title"] for album in albums]
    return "\n".join(titles)

@app.route("/search_by" , methods=["GET", "POST"])    
def search_by():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        db = get_db()
        results = crud.search_artist(db, query)
        titles = [album["title"] for album in results]
    return "\n".join(titles)
        
    

    