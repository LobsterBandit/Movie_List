import pprint
import time
import requests
import requests_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from config import DATABASE, CACHELOC, APIKEY, APIURL, HEADERS
from update_db import upsert_videos


def _get_tmdb_video(movies):
    """
    Retrieve video data based on TMDb ID
    """
    video_list = []
    search_type = 'movie'
    payload = {
        'append_to_response': 'videos'
    }

    for movie in movies:
        tmdb_id = movie.tmdb_id
        search_pattern = '{0}{1}/{2}?api_key={3}'.format(APIURL, search_type, tmdb_id, APIKEY)
        video_resp = requests.get(search_pattern, headers=HEADERS, params=payload)

        if not video_resp.from_cache:
            remain = video_resp.headers['X-RateLimit-Remaining']
            print(remain)
        else:
            remain = None

        if remain == '39':
            starttime = time.time()
            print(starttime)

        # pprint.pprint(video_resp.json())
        video_resp = video_resp.json()

        if 'results' in video_resp['videos'].keys():
            for video in video_resp['videos']['results']:
                if video['iso_639_1'] == 'en':
                    if video['type']:
                        vtype = video['type']
                    else:
                        vtype = None
                    if video['key']:
                        vkey = video['key']
                    else:
                        vkey = None
                    if video['name']:
                        vname = video['name']
                    else:
                        vname = None
                    if video['size']:
                        vsize = video['size']
                    else:
                        vsize = None
                    if video['site']:
                        vsite = video['site']
                    else:
                        vsite = None

                    video_list.append(dict(movie_id=movie.id,
                                           type=vtype,
                                           key=vkey,
                                           name=vname,
                                           size=vsize,
                                           site=vsite))

        if remain is not None and remain == '0':
            endtime = time.time()
            if starttime is not None:
                delta = endtime - starttime
            else:
                delta = 0
            if delta < 10:
                sleep = 11 - delta
                print('0 requests left.  Sleeping for {} seconds.'.format(sleep))
                time.sleep(sleep)

    return video_list


if __name__ == '__main__':
    requests_cache.install_cache(CACHELOC, backend='sqlite', expire_after=864000)

    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    # movies = session.query(MovieList).filter(MovieList.Title=='Gladiator')
    movies = session.query(MovieList).order_by(MovieList.Title).all()
    vlist = _get_tmdb_video(movies)
    # pprint.pprint(vlist)
    upsert_videos(vlist)
