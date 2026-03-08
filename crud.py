### creating crud.py file to keep my app.py clean###
### can also use to test against DB without worrying about bringing the whole flask app up ###



#searches DB for given string for artists, albums and songs
def search_all(search=False):
    pass

#search just artists
def search_artist(search=False):
    pass

#search just albums
def search_album(search=False):
    pass

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