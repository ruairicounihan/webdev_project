### creating crud.py file to keep my app.py clean###
### can also use to test against DB without worrying about bringing the whole flask app up ###
import os
import sqlite3

#searches DB for given string for artists, albums and songs
def search_all(db, search=False):
    albums = db.execute( """ SELECT * FROM albums;""").fetchall()
  # print(type(albums))    
    return albums
    

#search just artists
def search_artist(db, query):
    
    query_small_cap = f"%{query.lower()}%"
    
    albums = db.execute(""" SELECT * FROM albums
                            WHERE LOWER(artist) LIKE ?; """
                            , (query_small_cap,)).fetchall()
    print("inside search artist")
    print(albums)
    return albums

#search just albums
def search_album(db, query):
    
    query_small_cap = f"%{query.lower()}%"
    
    albums = db.execute(""" SELECT * FROM albums
                            WHERE LOWER(title) LIKE ?; """
                            , (query_small_cap,)).fetchall()
    print("inside search album")
    print(albums)
    return albums


def get_album(db, album_id):
    return db.execute(""" SELECT * FROM albums WHERE album_id = ?; """, (album_id,)).fetchone()



def get_album_reviews(db, album_id):
    return db.execute(""" SELECT * FROM reviews WHERE album_id = ?;""", (album_id,)).fetchall()










#gets all albums. Returns everything if year is not set. Can be used to categorise. 
def get_all_albums(year=False):
    pass



######## USER RELATED ##########
def add_fav(db, user_id, album_id):
    print(f"add_fav called with user_id={user_id}, album_id={album_id}")

    existing = db.execute(
        """
        SELECT * FROM favorites WHERE user_id = ? AND album_id = ?;
        """,(user_id, album_id),).fetchone()

    if existing is None:
        db.execute(
            """
            INSERT INTO favorites (user_id, album_id)
            VALUES (?, ?);
            """,
            (user_id, album_id),
        )
        db.commit()

def remove_fav(db, user_id, album_id):
        db.execute(""" DELETE FROM favorites WHERE user_id = ? AND album_id = ?; """,(user_id, album_id),)
        db.commit()
        
        
def get_favorite_album_ids(db, user_id):
    favorites = db.execute(""" SELECT album_id FROM favorites WHERE user_id = ?; """, (user_id,),).fetchall()
    return {row["album_id"] for row in favorites}


def get_favorites(db, user_id):  
    favorites = db.execute("""SELECT albums.* FROM albums JOIN favorites ON albums.album_id = favorites.album_id
                              WHERE favorites.user_id = ?;""", (user_id,)).fetchall()
    return favorites
    

def add_review(db, user_id, album_id, rating, comment):
    db.execute(""" INSERT INTO reviews (user_id, album_id, rating, comment) VALUES (?,?,?,?);""",(user_id, album_id, rating, comment))
    db.commit()
 
def get_my_reviews(db, user_id):
    myReviews = db.execute(""" SELECT albums.title, albums.artist, reviews.rating, reviews.comment, reviews.time, reviews.user_id FROM albums JOIN reviews ON albums.album_id = reviews.album_id
                    WHERE reviews.user_id = ?;""", (user_id,)).fetchall()
    return myReviews


""" Testing...
"""
if __name__ == "__main__":
    database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "reviews.db")
    db = sqlite3.connect(database_path)
    db.row_factory = sqlite3.Row

    print("Connected to:", database_path)

    albums = db.execute("SELECT album_id, title, artist FROM albums LIMIT 5;").fetchall()

    print("\nSample albums:")
    for row in albums:
        print(dict(row))

    db.close()
