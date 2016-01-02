import sqlite3

from config import DATABASE


def create_db(db_name):
    try:
        db = sqlite3.connect(db_name)
        cur = db.cursor()

        # cur.execute("""
        # CREATE TABLE Movie_List (
        # id	INTEGER PRIMARY KEY AUTOINCREMENT,
        # Filename		TEXT,
        # Size			REAL,
        # Path			TEXT,
        # Title			TEXT,
        # Year			INTEGER,
        # tmdb_id			INTEGER,
        # Overview		TEXT,
        # imdb_id			TEXT,
        # Rating			REAL,
        # Runtime 		REAL,
        # Release_Date    TEXT,
        # Poster          TEXT,
        # Backdrop        TEXT,
        # Tagline         TEXT,
        # Date_Updated	TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        # Date_Added      TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        # )
        # """)
        #
        # cur.execute("""
        # CREATE TABLE Genre (
        # Genre_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
        # tmdb_genre_id   INTEGER,
        # Genre_Desc      TEXT,
        # Movie_id        INTEGER NOT NULL,
        # Date_Updated    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # Date_Added      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # FOREIGN KEY(Movie_id) REFERENCES Movie_List(id) ON UPDATE CASCADE
        # )
        # """)
        #
        # cur.execute("""
        # CREATE TABLE Cast (
        # Cast_ID         INTEGER PRIMARY KEY AUTOINCREMENT,
        # tmdb_cast_id    INTEGER,
        # Cast_Name       TEXT,
        # Cast_Char       TEXT,
        # Cast_Order      INTEGER,
        # Profile         TEXT,
        # Movie_id        INTEGER NOT NULL,
        # Date_Updated    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # Date_Added      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # FOREIGN KEY(Movie_id) REFERENCES Movie_List(id) ON UPDATE CASCADE
        # )
        # """)
        #
        # cur.execute("""
        # CREATE TABLE Video (
        # Video_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
        # Type            TEXT,
        # Key             TEXT,
        # Name            TEXT,
        # Size            INTEGER,
        # Site            TEXT,
        # Movie_id        INTEGER NOT NULL,
        # Date_Updated    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # Date_Added      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        # FOREIGN KEY(Movie_id) REFERENCES Movie_List(id) ON UPDATE CASCADE
        # )
        # """)

        cur.execute("""
        CREATE TABLE Ratings (
        Rating_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
        imdb_rating         REAL,
        imdb_votes          INTEGER,
        tomato_rating       REAL,
        tomato_reviews      INTEGER,
        tomato_fresh        INTEGER,
        tomato_rotten       INTEGER,
        tomato_meter        INTEGER,
        tomato_consensus    TEXT,
        tomato_image        TEXT,
        tomato_user_meter   INTEGER,
        tomato_user_rating  REAL,
        tomato_user_reviews INTEGER,
        tomato_url          TEXT,
        Movie_id            INTEGER NOT NULL,
        Date_Updated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Date_Added          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(Movie_id) REFERENCES Movie_List(id) ON UPDATE CASCADE
        )
        """)

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == '__main__':
    db_name = DATABASE
    create_db(db_name)
