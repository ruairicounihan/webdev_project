from flask import Flask, render_template, request, session, redirect, url_for
from database import get_db, close_db
from flask_session import Session
import crud
from forms import SearchForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "Ruairi's Key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
app.teardown_appcontext(close_db)

@app.route("/search" , methods=["POST", "GET"])    
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        db = get_db()
        artist_results = crud.search_artist(db, query)
        album_results = crud.search_album(db, query)
        

        results = artist_results + album_results 

        return render_template("index.html", results=results, form=form)
    return render_template("index.html", results=[], form=form)
        
        
#returns a users entire fav list up to this point.
@app.route("/get_favorites")
def get_favorites():
    db = get_db()
    favorites = crud.get_favorites(db)
    return render_template("favorites.html", favorites=favorites)

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    print(album_id)
    query = request.form.get("query", "".strip())
    print(query)
    user_id = 4
    crud.add_fav(db, user_id, album_id)
    return redirect(url_for("search", query=query))




@app.route("/review_page")
def review_page():
    pass