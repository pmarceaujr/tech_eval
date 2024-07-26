from fastapi import Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database import get_db, engine
from app import models, schemas
from datetime import date

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.get("/welcome")
def welcome():
    return {"message": "Welcome the music project, the server and API are running fine."}

@app.get("/artists/", response_model=list[schemas.Artist])
def list_artists(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    artists = db.query(models.Artist).limit(limit).offset(offset).all()
    return artists

@app.get("/artists_albums/", response_model=list[schemas.ArtistAlbum])
def list_artists_with_albums(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    artists = db.query(models.Artist).limit(limit).offset(offset).all()
    return artists



@app.get("/albums/", response_model=list[schemas.AlbumBase])
def list_albums(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    albums = db.query(models.Album).limit(limit).offset(offset).all()
    return albums


@app.post('/artist', status_code=status.HTTP_201_CREATED)
def create_artist(payload: schemas.ArtistCreate, db: Session = Depends(get_db)):
    artist = models.Artist(**payload.model_dump())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist

@app.post('/artist/{artist_id}/album', status_code=status.HTTP_201_CREATED)
def create_album(artist_id: int, payload: schemas.AlbumCreate, db: Session = Depends(get_db)):
    album = models.Album(**payload.model_dump(), artist_id=artist_id)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@app.get("/albums/{artist_id}", response_model=list[schemas.Album])
def get_artist_albums(artist_id: int,  db: Session = Depends(get_db), limit: int = 10, offset: int = 0, release_date: date = None, price: int = None):
    # items = crud.get_itemss_by_user(user_id, db)
    filters = []
    if release_date:
        print("Date")
        filters.append(models.Album.release_date == release_date)
    if price:
        print("Price)")
        filters.append(models.Album.price == price))

    albums = db.query(models.Album).\
        filter(models.Album.artist_id == artist_id).\
        filter(
            or_(filters)).\
        limit(limit).offset(offset).all()
    return albums

