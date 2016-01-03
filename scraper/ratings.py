import pprint
import os
import json
import requests
import requests_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from config import DATABASE, CACHELOC


def omdb(movies):
    ratings = []
    base_url = 'https://www.omdbapi.com/?'

    for movie in movies:
        mdict = {}
        payload = {
            'i': movie.imdb_id,
            'type': 'movie',
            'tomatoes': 'true'
        }
        r = requests.get(base_url, params=payload).json()
        # pprint.pprint(r, indent=4)

        keys = ['imdbRating', 'imdbVotes', 'tomatoRating', 'tomatoReviews', 'tomatoFresh', 'tomatoRotten',
                'tomatoMeter', 'tomatoConsensus', 'tomatoImage', 'tomatoUserMeter', 'tomatoUserRating',
                'tomatoUserReviews', 'tomatoURL']

        mdict['Movie_id'] = movie.id

        for key in keys:
            if key in r.keys():
                result = r[key]
            else:
                result = None
            mdict[key] = result

        ratings.append(mdict)

    return ratings


def json_output(result, json_file=os.path.join(os.path.abspath(os.path.dirname(__file__)),'OMDb_Ratings.txt')):
    """
    Output 'result' as JSON to the specified file
        - filename defaults to that supplied by config.py
    """
    with open(json_file, 'w') as f:
        json.dump(result, f, indent=4)
    print('Query output created at {}'.format(json_file))


if __name__ == '__main__':
    requests_cache.install_cache(CACHELOC, backend='sqlite', expire_after=432000)

    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    # movies = session.query(MovieList).filter(MovieList.Title=='Gladiator')
    movies = session.query(MovieList).order_by(MovieList.Title).all()
    ratings = omdb(movies)
    # pprint.pprint(ratings, indent=4)
    json_output(ratings)
