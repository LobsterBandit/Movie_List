import pprint
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from config import DATABASE


def omdb(movie):
    base_url = 'http://www.omdbapi.com/?'
    payload = {
        'i': movie.imdb_id,
        'type': 'movie',
        'tomatoes': 'true'
    }

    r = requests.get(base_url, params=payload).json()
    pprint.pprint(r, indent=4)


if __name__ == '__main__':
    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    movies = session.query(MovieList).filter(MovieList.Title=='Gladiator').all()
    for movie in movies:
        omdb(movie)
