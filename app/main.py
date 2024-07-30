from fastapi import Depends, FastAPI, status, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database import get_db, engine
from app import models, schemas
from datetime import date

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.get("/welcome")
def welcome():
    try:
        return {"message": "Welcome the music project, the server and API are running fine."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e    


@app.get("/artists/", response_model=list[schemas.Artist])
def list_artists(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    try:
        artists = db.query(models.Artist).limit(limit).offset(offset).all()
        return artists
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e


@app.get("/artists_albums/", response_model=list[schemas.ArtistAlbum])
def list_artists_with_albums(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    try:
        artists = db.query(models.Artist).limit(limit).offset(offset).all()
        return artists
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e

@app.get("/artists_albums_songs/", response_model=list[schemas.ArtistAlbumSongs])
def list_artists_with_albums_songs(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    try:
        artists = db.query(models.Artist).limit(limit).offset(offset).all()
        return artists
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e    


@app.get("/albums/", response_model=list[schemas.AlbumBase])
def list_albums(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    try:
        albums = db.query(models.Album).limit(limit).offset(offset).all()
        return albums
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e


@app.get("/songs/", response_model=list[schemas.SongBase])
def list_songs(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    try:
        songs = db.query(models.Song).limit(limit).offset(offset).all()
        return songs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e    


@app.post('/artist', status_code=status.HTTP_201_CREATED)
def create_artist(payload: schemas.ArtistCreate, db: Session = Depends(get_db)):
    try:
        artist = models.Artist(**payload.model_dump())
        db.add(artist)
        db.commit()
        db.refresh(artist)
        return artist
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Artist with name: {artist.name} already exists.",
        ) from e
    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the new artist.",
        ) from e


@app.post('/artist/{artist_id}/album', status_code=status.HTTP_201_CREATED)
def create_album(artist_id: int, payload: schemas.AlbumCreate, db: Session = Depends(get_db)):
    try:
        album = models.Album(**payload.model_dump(), artist_id=artist_id)
        db.add(album)
        db.commit()
        db.refresh(album)
        return album
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The followig error occured: {e}.",
        ) from e    
    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the new album.",
        ) from e    

@app.post('/album/{album_id}/song', status_code=status.HTTP_201_CREATED)
def create_song(album_id: int, payload: schemas.SongCreate, db: Session = Depends(get_db)):
    try:
        album = models.Song(**payload.model_dump(), album_id=album_id)
        db.add(album)
        db.commit()
        db.refresh(album)
        return album
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The followig error occured: {e}.",
        ) from e    
    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the new song.",
        ) from e        


@app.get("/albums/{artist_id}", response_model=list[schemas.Album])
def get_artist_albums(artist_id: int,  db: Session = Depends(get_db), limit: int = 100, offset: int = 0, release_date: date = None, price: float = None):
    # items = crud.get_itemss_by_user(user_id, db)
    try:
        filter = db.query(models.Album).filter(models.Album.artist_id == artist_id).limit(limit).offset(offset)
        if release_date and price:
            print("Date and Price")
            filter = db.query(models.Album).filter(models.Album.artist_id == artist_id).\
                        filter(or_(models.Album.release_date == release_date, models.Album.price == price)).\
                        limit(limit).offset(offset)
            
        if release_date and not price:
            print("Date and No  Price")
            filter = db.query(models.Album).filter(models.Album.artist_id == artist_id).\
                        filter(models.Album.release_date == release_date).\
                        limit(limit).offset(offset)        
            
        if not release_date and price:
            print("No Date and Price")
            filter = db.query(models.Album).filter(models.Album.artist_id == artist_id).\
                        filter(models.Album.price == price).\
                        limit(limit).offset(offset)
            
        albums = filter.all()
        return albums
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The followig error occured: {e}.",
        ) from e
# db.query(models.Album).filter(models.Album.artist_id == artist_id).filter(or_(models.Album.release_date == release_date,models.Album.price == price)).limit(limit).offset(offset).all()
