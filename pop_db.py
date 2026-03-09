from database import get_db, close_db
import csv
import os
import sqlite3

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "reviews.db")

def init_db():
    db = get_db()
    
    with open(SQL_FILE, "r") as sql_schema:
        sql_script = sql_schema.read()

    # execute SQL commands
    db.executescript(sql_script)
    print("Database initialized.")
    
    
def get_db():
    
    db = sqlite3.connect(DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db


def add_album(db, title,artist,release_date,genres,user_score,rating_count):
    print(title,artist,release_date,genres,user_score,rating_count)
    sql_statement ='''INSERT INTO albums (title, artist, release_date, genres, user_score, rating_count)
                    VALUES (?, ?, ?, ?, ?, ?)'''
    
    db.execute(sql_statement, (title,artist,release_date,genres,user_score,rating_count))
    db.commit()


if __name__ == "__main__":
    init_db()
    
    db = get_db()

    with open("aoty.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            add_album(db, row["title"],row["artist"],row["release_date"],row["genres"],row["user_score"],row["rating_count"])
    
        

