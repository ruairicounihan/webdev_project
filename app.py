from flask import Flask, render_template, request, session, redirect, url_for, g
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import crud
from forms import SearchForm, RegistrationForm, LoginForm, ReviewForm
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "Ruairi's Key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view


@app.route("/" , methods=["POST", "GET"])  
@login_required  
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
        user_id = g.user
        artist_results = crud.search_artist(db, query)
        album_results = crud.search_album(db, query)
        results = artist_results + album_results 
        favorite_ids = crud.get_favorite_album_ids(db, user_id)

        return render_template("index.html", results=results, form=form, query=query, favorite_ids=favorite_ids)
    return render_template("index.html", results=[], form=form, query="", favorite_ids=set())
        
        
#returns a users entire fav list up to this point.
@app.route("/get_favorites")
@login_required 
def get_favorites():
    db = get_db()
    user_id = g.user
    favorites = crud.get_favorites(db, user_id)
    return render_template("favorites.html", favorites=favorites)

@app.route("/add_favorite", methods=["POST"])
@login_required 
def add_favorite():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = g.user
    crud.add_fav(db, user_id, album_id)
    return redirect(url_for("search", query=query))


@app.route("/remove_favorites", methods=["POST"])
@login_required 
def remove_favorite():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = g.user
    crud.remove_fav(db, user_id, album_id)
    return redirect(url_for("search", query=query))


@app.route("/updated_favorites", methods=["POST"])
@login_required 
def updated_favorites():
    db = get_db()
    album_id = request.form.get("album_id", type=int)
    query = request.form.get("query", "").strip()
    user_id = g.user
    crud.remove_fav(db, user_id, album_id)
    return redirect(url_for("get_favorites", query=query))


@app.route("/review_page/<int:album_id>", methods=["GET", "POST"])
@login_required
def review_page(album_id):
    db = get_db()
    form = ReviewForm()
    album = crud.get_album(db, album_id)
    reviews = crud.get_album_reviews(db, album_id)
    
    if form.validate_on_submit():
        user_id = g.user
        crud.add_review(db, user_id, album_id, form.rating.data, form.comment.data)
        return redirect(url_for("review_page", album_id=album_id))
    
    return render_template("reviews.html", album=album, reviews=reviews, form=form)

@app.route("/my_reviews" ,methods=["POST", "GET"])
@login_required
def my_reviews():
    db = get_db()
    user_id = g.user
    my_reviews = crud.get_my_reviews(db, user_id)
    return render_template("my_reviews.html", my_reviews=my_reviews)
    

    """User Functions from labs"""
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        existing_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?;""", 
                                      (user_id,)).fetchone()
        if existing_user is not None:
            form.user_id.errors.append("User ID already exists")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                          VALUES (?, ?);""", 
                          (user_id, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?;""", 
                                      (user_id,)).fetchone()
        if matching_user is None:
            form.user_id.errors.append("Unknown user ID")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("search")
            return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("search"))