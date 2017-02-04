import requests
import datetime
import sqlite3

from config import APIURL, APIKEY, HEADERS, DATABASE


def fetch_genres():
    genre_url = '{url}genre/movie/list?api_key={key}'.format(url=APIURL, key=APIKEY)
    try:
        genre_res = requests.get(genre_url, headers=HEADERS, verify=False)
        genre_json = genre_res.json()

        # for genre in genre_json['genres']:
        #     print('Id: {0}, Name: {1}'.format(genre['id'], genre['name']))

    except Exception as e:
        print(e)

    return genre_json['genres'] if genre_json['genres'] else None


def update_genrelist_db(genres, source='TMDb'):
    try:
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()

        for genre in genres:
            r = genre_exists(genre, source)

            if r is not None and genre['name'] == r['GenreName'] and source == r['Source']:
                continue
            elif r is not None and (genre['name'] != r['GenreName'] or source != r['Source']):
                # genre id exists in database but name or source is different, update record
                cur.execute("""
                    update GenreList
                    set GenreName = ?,
                        Source = ?,
                        DateUpdated = ?
                    where GenreId = ?
                """, (genre['name'], source, datetime.datetime.utcnow(), genre['id'])
                )
            else:
                # genre does not exist in database, insert new record
                cur.execute("""
                    insert into GenreList (GenreId, GenreName, Source)
                    values (?, ?, ?)
                """, (genre['id'], genre['name'], source)
                )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def select_genrelist_db(genre, source):
    try:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        cur = db.cursor()

        cur.execute('select * from GenreList where GenreId = ?', (genre['id'],))
        # cur.execute('select * from GenreList where GenreId = 12')
        r = cur.fetchone()
        print(r.keys())
        for member in r:
            print(member)
        print(r['GenreId'])
        print(r['GenreId'] == genre['id'])
        if r is not None:
            ziptie = zip([genre['id'], genre['name'], source], r)
            comp = [(a == b) for a, b in ziptie]
            print(comp)

    except Exception as e:
        raise e
    finally:
        db.close()


def genre_exists(genre, source):
    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        c = con.cursor()

        c.execute('select GenreId, GenreName, Source from GenreList where GenreId = ?', (genre['id'],))
        r = c.fetchone()

    except Exception as e:
        raise e
    finally:
        con.close()

    # r is None if the row does not exist
    return r


genre_list = fetch_genres()
update_genrelist_db(genre_list)
# select_genrelist_db(genre_list[0], 'TMDb')
