from flask import Flask, render_template, session, redirect, url_for
from database import get_db, close_db
from flask_session import Session
import crud
from forms import SearchForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "Ruairi's Key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["WTF_CSRF_ENABLED"] = False
Session(app)
app.teardown_appcontext(close_db)

@app.route("/search")
def search():
    db = get_db()
    albums = crud.search_all(db)
    titles = [album["title"] for album in albums]
    return render_template("index.html", titles=titles)

@app.route("/search_by" , methods=["POST", "GET"])    
def search_by():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        db = get_db()
        artist_results = crud.search_artist(db, query)
        album_results = crud.search_album(db, query)
        

        results = artist_results + album_results 

        return render_template("index.html", results=results, form=form)
    return render_template("index.html", results=[], form=form)
        
