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
    print("inside search")
    print(albums)
    return albums

#search just albums
def search_album(db, query):
    
    query_small_cap = f"%{query.lower()}%"
    
    albums = db.execute(""" SELECT * FROM albums
                            WHERE LOWER(title) LIKE ?; """
                            , (query_small_cap,)).fetchall()
    print("inside search")
    print(albums)
    return albums

#search just songs
def search_song(search=False):
    pass

#rates an album with a score and allows comment
def rate_album(rating, review, album_id):
    pass


#gets all albums. Returns everything if year is not set. Can be used to categorise. 
def get_all_albums(year=False):
    pass



######## USER RELATED ##########


def register_user(email, password):
    pass

def check_password(password):
    pass

def add_favorites(album_id):
    pass

def get_favorites():
    pass




if __name__ == "__main__":
    search_all()