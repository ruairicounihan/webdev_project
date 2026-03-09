DROP TABLE IF EXISTS albums;

CREATE TABLE albums
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    release_date TEXT,
    genres TEXT,
    user_score REAL,
    rating_count INTEGER
);