import sqlite3
import datetime
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
                                                Release_Date, Tagline, Date_Added, Genre)
            values ((select id from Movie_List where tmdb_id = ? and size = ?)
                    ,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                    (select Date_Added from Movie_List where tmdb_id = ? and size = ?), ?)
            """, (movie['tmdb_id'], movie['size'], movie['filename'], movie['size'], movie['root'], movie['title'],
                  movie['year'], movie['tmdb_id'], movie['overview'], movie['imdb_id'], movie['vote_average'],
                  movie['runtime'], movie['poster_path'], movie['backdrop_path'], movie['release_date'],
                  movie['tagline'], movie['tmdb_id'], movie['size'], movie['genres'])
            )

            # for genre in movie['genres']:
            #     cur.execute("""
            #         insert or replace into Genre (Id, GenreId, Source, MovieId)
            #         values ((select Id from Genre
            #                             where MovieId = (select id from Movie_List where tmdb_id = ? and size = ?)
            #                             and GenreId = ?
            #                             and Source = ?)
            #                 ,?, ?, (select id from Movie_List where tmdb_id = ? and size = ?))
            #     """, (movie['tmdb_id'], movie['size'], genre['id'], 'TMDb', genre['id'], 'TMDb', movie['tmdb_id'], movie['size'])
            #     )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def upsert_videos(video_list, database=DATABASE):
    try:
        db = sqlite3.connect(database)
        cur = db.cursor()

        for video in video_list:
            cur.execute("""
            insert or replace into Video (Video_ID, Type, Key, Name, Size, Site, Movie_id, Date_Added)

            values ((select Video_ID from Video where Movie_id = ? and Key = ?),
                    ?,?,?,?,?,?,
                    (select Date_Added from Video where Movie_id = ? and Key = ?))
            """, (video['movie_id'], video['key'], video['type'], video['key'], video['name'], video['size'],
                  video['site'], video['movie_id'], video['movie_id'], video['key'])
            )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
