import sqlite3
from config import DATABASE


def upsert_db(movie_list, database=DATABASE):
    try:
        db = sqlite3.connect(database)
        cur = db.cursor()

        for movie in movie_list:
            cur.execute("""
            insert or replace into Movie_List (id, Filename, Size, Path, Title,
                                                Year, tmdb_id, Overview, imdb_id,
                                                Rating, Runtime, Poster, Backdrop,
                                                Release_Date, Tagline, Date_Added)
            values ((select id from Movie_List where tmdb_id = ? and size = ?)
                    ,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                    (select Date_Added from Movie_List where tmdb_id = ? and size = ?))
            """, (movie['tmdb_id'], movie['size'], movie['filename'], movie['size'], movie['root'], movie['title'],
                  movie['year'], movie['tmdb_id'], movie['overview'], movie['imdb_id'], movie['vote_average'],
                  movie['runtime'], movie['poster_path'], movie['backdrop_path'], movie['release_date'],
                  movie['tagline'], movie['tmdb_id'], movie['size'])
            )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
