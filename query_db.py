from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, MovieList
from config import DATABASE


engine = create_engine('sqlite:///{}'.format(DATABASE))
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

like_result = session.query(MovieList).filter(MovieList.Title.like('G%')).order_by(MovieList.Title).all()
for x in like_result:
    print('{} {}'.format(x.Title, x.Year))
