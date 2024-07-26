
'''
Here is the code for a standard Pydantic models.  These models are used for the data validation, 
conversion, and documentation of classes.  Pydantic is used to define and enforce the schema or 
struture of the tables.

In this project, we will use the BaseModel model.
'''

from pydantic import BaseModel
from datetime import date


class AlbumBase(BaseModel):
    name: str
    release_date: date 
    price: float

class AlbumArtist(BaseModel):
    name: str
    release_date: date 
    price: float


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    artist_id: int

    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    name: str

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int


class ArtistAlbum(ArtistBase):
    id: int
    album: list[Album] = []

    class Config:
        orm_mode = True