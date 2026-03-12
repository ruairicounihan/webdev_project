DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS favorites;

CREATE TABLE albums
(
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    release_date TEXT,
    genres TEXT,
    user_score REAL,
    rating_count INTEGER
);

CREATE TABLE favorites
(
    user_id INTEGER NOT NULL ,
    album_id INTEGER NOT NULL
);