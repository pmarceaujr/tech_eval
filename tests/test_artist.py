import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from app.main import app
from app import schemas
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import event
from app.database import get_db
from app import models


SQLITE_DATABASE_URL = "sqlite:///./bay_music_test.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
models.Base.metadata.create_all(bind=engine)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =  declarative_base()
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))


@pytest.fixture(scope="module")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)  
    db = SessionLocalTest()
    try:
        yield db
    finally:
        db.close()      

@pytest.fixture(scope="module")
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def test_artists(session):
    pass


def test_welcome(client):
    res = client.get("/welcome")
    assert res.status_code == 200

@pytest.mark.parametrize("end_point,  expected_response",[
    ("/artists", 200 ),
    ("/artists_albums/", 200 ),
    ("/artists_albums_songs/",  200 ),
    ("/albums/", 200 ),
    ("/songs/",  200 ),
])
def test_all_gets(client, end_point, expected_response):
    res = client.get(end_point)
    assert res.status_code == expected_response 


@pytest.mark.parametrize("artist_name, genre, expected, expected_response",[
    ("Motley Crue", "Rock", "Motley Crue", 201 ),
    # Error Entry
    ("Motley Crue", "Rock", "Motley Crue", 409 ),
    ("Luke Combs", "Country", "Luke Combs", 201 ),
    ("Van Halen",  "Rock", "Van Halen", 201 ),
    ("Steve Miller Band", "Rock", "Steve Miller Band", 201 ),
    ("Dave Matthews Band",  "Rock", "Dave Matthews Band", 201 ),
    ("Lee Brice", "Country", "Lee Brice", 201 )
])
def test_create_artist(client, artist_name, genre, expected, expected_response):
    res = client.post("/artist", json={"name": artist_name, "genre": genre})
    assert res.status_code == expected_response 


@pytest.mark.parametrize("album_name, release_date, price, artist_id, expected, status_code",[
    ("Too Fast for Love", "1981-11-10", 12.99, 1, "Too Fast for Love", 201 ),
    ("Shout at the Devil", "1983-09-23", 13.99, 1, "Shout at the Devil", 201 ),
    ("Growin' Up", "2022-06-24", 12.99, 2, "Growin' Up", 201 ),
    # Error entry
    ("Growin' Up123", "2022-00-24", 12.99, 2, "Growin Up", 422 ),
    ("Van Halen", "1978-02-10", 9.99, 3, "Van Halen", 201 ),
    ("Van Halen II", "1979-03-23", 8.99, 3, "Van Halen II", 201 ),
    ("Fair Warning", "1982-04-29", 12.99, 3, "Fair Warning", 201 ),
    ("Children of the Future", "1968-06-01", 7.99, 4, "Children of the Future", 201 ),
    ("Brave New World", "1970-01-01", 12.99, 4, "Brave New World", 201 ),
    ("Rock Love", "1971-01-01", 11.99, 4, "Rock Love", 201 ),
    ("Under the Table and Dreaming", "1994-01-01", 12.99, 5, "Under the Table and Dreaming", 201 ),
    ("Crash", "1996-01-01", 13.99, 5, "Crash", 201 ),
    # Error entry
    ("Stand Up123", "005-01-01", 14.99, 5, "Stand Up", 422 ),
    ("Love Like Crazy", "2010-01-01", 13.99, 61231, "Love Like Crazy", 201 ),
    ("Hard 2 Love", "2012-01-01", 13.99, 6, "Hard 2 Love", 201 ),
])
def test_create_album(client, album_name, release_date, price, artist_id, expected, status_code):
    res = client.post(f"/artist/{artist_id}/album", json={"name": album_name, "release_date": release_date, "price": price, "artist_id": artist_id})
    assert res.status_code == status_code     



@pytest.mark.parametrize("song_name, duration, album_id, status_code",[
    ("Too Fast for Love",  4.36, 1, 201 ),
    ("Shout at the Devil",  4.49, 1, 201 ),
    ("Growin' Up",  3.45, 2, 201 ),
    # Error entry
    ("Growin' Up123",  "1r.99", 2, 422 ),
])
def test_create_song(client, song_name, duration,  album_id, status_code):
    res = client.post(f"/album/{album_id}/song", json={"name": song_name, "duration": duration, "album_id": album_id})
    assert res.status_code == status_code