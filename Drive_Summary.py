import csv
import os
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from movies import file_details
from config import EXTENSIONS, DATABASE


def csv_output(result, csv_dir='c:\\users\\darin\\desktop', csv_file='query_result.csv'):
    output = os.path.join(csv_dir, csv_file)
    fields = list(result[0].keys())
    with open(output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in result:
            writer.writerow(item)


if __name__ == '__main__':
    location = ['F:\\']
    extensions = EXTENSIONS

    # set up sqlalchemy database connection
    engine = create_engine('sqlite:///{}'.format(DATABASE))
    Base.metadata.bind = engine
    session = scoped_session(sessionmaker(bind=engine))

    klist = file_details(location, extensions)

    csv_output(klist, csv_file='file_result.csv')

    for movie in klist:
        try:
            attribs = session.query(MovieList).filter(
                and_(MovieList.Title == movie['title'], MovieList.Size == movie['size'])).first()

            if attribs.imdb_id:
                movie['imdb_id'] = attribs.imdb_id
            else:
                movie['imdb_id'] = None
            if attribs.Runtime:
                movie['runtime'] = attribs.Runtime
            else:
                movie['runtime'] = None
            if attribs.Rating:
                movie['rating'] = attribs.Rating
            else:
                movie['rating'] = None
        except AttributeError as e:
            movie['imdb_id'] = None
            movie['runtime'] = None
            movie['rating'] = None

    csv_output(klist)
