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

@app.route("/" , methods=["POST", "GET"])    
def search():
    form = SearchForm()
    query = ""
    
    if request.method == "POST" and form.validate_on_submit():
        query = form.query.data
    elif request.method == "GET":
        query = request.args.get("query", "").strip()
        form.query.data = query
        
    if query:
        db = get_db()
        user_id = 4 ## remove later
        artist_results = crud.search_artist(db, query)
        album_results = crud.search_album(db, query)
        results = artist_results + album_results 
        favorite_ids = crud.get_favorite_album_ids(db, user_id)

        return render_template("index.html", results=results, form=form, query=query, favorite_ids=favorite_ids)
    return render_template("index.html", results=[], form=form, query="", favorite_ids=set())
        
        
#returns a users entire fav list up to this point.
@app.route("/get_favorites")
def get_favorites():
    db = get_db()
    user_id = 4    # remove
    favorites = crud.get_favorites(db, user_id)
    return render_template("favorites.html", favorites=favorites)

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = 4
    crud.add_fav(db, user_id, album_id)
    return redirect(url_for("search", query=query))


@app.route("/remove_favorites", methods=["POST"])
def remove_favorite():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = 4
    crud.remove_fav(db, user_id, album_id)
    return redirect(url_for("search", query=query))


@app.route("/updated_favorites", methods=["POST"])
def updated_favorites():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = 4
    crud.remove_fav(db, user_id, album_id)
    return redirect(url_for("get_favorites", query=query))


@app.route("/review_page")
def review_page():
    pass