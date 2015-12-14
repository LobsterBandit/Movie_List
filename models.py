from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Cast(Base):
    __tablename__ = 'Cast'

    Cast_ID = Column(Integer, primary_key=True)
    tmdb_cast_id = Column(Integer)
    Cast_Name = Column(Text)
    Cast_Char = Column(Text)
    Cast_Order = Column(Integer)
    Profile = Column(Text)
    Movie_id = Column(ForeignKey('Movie_List.id'), nullable=False)
    Date_Updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    Date_Added = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    Movie = relationship('MovieList')


class Genre(Base):
    __tablename__ = 'Genre'

    Genre_ID = Column(Integer, primary_key=True)
    tmdb_genre_id = Column(Integer)
    Genre_Desc = Column(Text)
    Movie_id = Column(ForeignKey('Movie_List.id'), nullable=False)
    Date_Updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    Date_Added = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    Movie = relationship('MovieList')


class MovieList(Base):
    __tablename__ = 'Movie_List'

    id = Column(Integer, primary_key=True)
    Filename = Column(Text)
    Size = Column(Float)
    Path = Column(Text)
    Title = Column(Text, index=True)
    Year = Column(Integer, index=True)
    tmdb_id = Column(Integer, index=True)
    Overview = Column(Text)
    imdb_id = Column(Text)
    Rating = Column(Float)
    Runtime = Column(Float)
    Release_Date = Column(Text)
    Poster = Column(Text)
    Backdrop = Column(Text)
    Tagline = Column(Text)
    Date_Updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    Date_Added = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Video(Base):
    __tablename__ = 'Video'

    Video_ID = Column(Integer, primary_key=True)
    Type = Column(Text)
    Key = Column(Text)
    Name = Column(Text)
    Size = Column(Integer)
    Site = Column(Text)
    Movie_id = Column(ForeignKey('Movie_List.id'), nullable=False)
    Date_Updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    Date_Added = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    Movie = relationship('MovieList')
