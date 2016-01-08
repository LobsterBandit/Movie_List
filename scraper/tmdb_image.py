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


def scan_static_img(loc=APPIMG):
    imglist = []
    for root, dirs, files in os.walk(loc):
        for file in files:
            imgfile = '{}_{}_{}'.format(file.split('_')[0], file.split('_')[1], file.split('_')[2][:-4])
            print(imgfile)
            imglist.append(imgfile)
    return imglist


if __name__ == '__main__':
    config = _get_json(CONFIG_PATTERN.format(key=APIKEY))
    base_url = config['images']['secure_base_url']
    size = 'original'
    output = APPIMG

    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    # all images
    movies = session.query(MovieList).order_by(MovieList.Title).all()

    imgs = scan_static_img()

    getlist = []
    for movie in movies:
        poster = '{title}_{year}_poster'.format(title=movie.Title, year=movie.Year)
        backdrop = '{title}_{year}_backdrop'.format(title=movie.Title, year=movie.Year)
        if poster.lower() in [img.lower() for img in imgs]:
            getposter = False
            print('{} poster already downloaded'.format(movie.Title))
        else:
            getposter = True
        if backdrop.lower() in [img.lower() for img in imgs]:
            getbackdrop = False
            print('{} backdrop already downloaded'.format(movie.Title))
        else:
            getbackdrop = True
        if getposter or getbackdrop:
            getlist.append(movie)
            print('Queued {} for download'.format(movie.Title))

    # print(getlist)
    # one image based on imdb_id
    # getlist = session.query(MovieList).filter(MovieList.imdb_id=='tt2503944').all()

    download_images(getlist, base_url, size, output)
