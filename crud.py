### creating crud.py file to keep my app.py clean###
### can also use to test against DB without worrying about bringing the whole flask app up ###

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


#rates an album with a score and allows comment
def rate_album(rating, album_id):
    pass

def comment(db, album_id, user_comment):
    pass

#gets all albums. Returns everything if year is not set. Can be used to categorise. 
def get_all_albums(year=False):
    pass



######## USER RELATED ##########


def register_user(email, password):
    pass

def check_password(password):
    pass

def add_fav(db, user_id, album_id):
    print(f"DEBUG: Attempting to add {album_id} for user {user_id}") 
    
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

def remove_favorite(db, user_id, album_id):
        db.execute(""" DELETE FROM favorites WHERE user_id = ? AND album_id = ?; """,(user_id, album_id),)
        db.commit()
        
        
def get_favorites(db):  
    user_id = 1
    
    
    favorites = db.execute("""
        SELECT albums.* FROM albums
        JOIN favorites ON albums.id = favorites.album_id
        WHERE favorites.user_id = ?;
    """, (user_id,)).fetchall()

    return favorites



if __name__ == "__main__":
    search_all()