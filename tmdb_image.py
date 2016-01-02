import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from config import DATABASE, APPIMG, CONFIG_PATTERN, APIKEY


def _get_json(url, params=None):
    r = requests.get(url)
    return r.json()


def download_images(movieobj, base_url, size, output, poster=True, backdrop=True):
    for movie in movieobj:
        if poster and movie.Poster is not None:
            img_url = '{0}{1}{2}'.format(base_url, size, movie.Poster)
            r = requests.get(img_url)

            imgtype = 'poster'
            filetype = movie.Poster.split('.')[1]
            filename = '{title}_{year}_{img}.{file}'.format(title=movie.Title, year=movie.Year, img=imgtype,
                                                            file=filetype)
            filepath = os.path.join(output, filename)
            with open(filepath, 'wb') as w:
                w.write(r.content)
            print('{} created at {}.'.format(filename, output))
        if backdrop and movie.Backdrop is not None:
            img_url = '{0}{1}{2}'.format(base_url, size, movie.Backdrop)
            r = requests.get(img_url)

            imgtype = 'backdrop'
            filetype = movie.Backdrop.split('.')[1]
            filename = '{title}_{year}_{img}.{file}'.format(title=movie.Title, year=movie.Year, img=imgtype,
                                                            file=filetype)
            filepath = os.path.join(output, filename)
            with open(filepath, 'wb') as w:
                w.write(r.content)
            print('{} created at {}.'.format(filename, output))


if __name__ == '__main__':
    config = _get_json(CONFIG_PATTERN.format(key=APIKEY))
    base_url = config['images']['secure_base_url']
    size = 'original'
    output = APPIMG

    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    movies = session.query(MovieList).order_by(MovieList.Title).all()

    download_images(movies, base_url, size, output)
