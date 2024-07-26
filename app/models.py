'''
Here is the code for a standard SQLAlchemy models.  These models are used by SQLAlchemy to interact 
with the database.  These calsses are how SQLAlchemy builds the tables as defined in the following code.

In this project, we will use the Base model.

'''

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    album = relationship("Album", back_populates="artist")


class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    release_date = Column(Date, index=True, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_date = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
    artist_id = Column(Integer, ForeignKey("artist.id"))
    artist = relationship("Artist", back_populates="album")