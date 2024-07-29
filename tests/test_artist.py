import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
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
    assert res.json().get('message') == 'Welcome the music project, the server and API are running fine.'
    assert res.status_code == 200


@pytest.mark.parametrize("artist_name, expected",[
    ("Motley Crue", "Motley Crue" ),
    ("Luke Combs", "Luke Combs"),
    ("Van Halen", "Van Halen"),
    ("Steve Miller Band", "Steve Miller Band"),
    ("Dave Matthews Band", "Dave Matthews Band"),
    ("Lee Brice", "Lee Brice")
])
def test_create_artist(client, artist_name, expected):
    res = client.post("/artist", json={"name": artist_name})
    new_artist = schemas.Artist(**res.json())
    assert new_artist.name == expected
    assert res.status_code == 201 

@pytest.mark.parametrize("album_name, release_date, price, artist_id, expected, status_code",[
    ("Too Fast for Love", "1981-11-10", 12.99, 1, "Too Fast for Love", 201 ),
    ("Shout at the Devil", "1983-09-23", 13.99, 1, "Shout at the Devil", 201 ),
    ("Theatre of Pain", "1985-06-24", 14.99, 1, "Theatre of Pain", 201 ),
    ("This Ones for You", "2017-06-02", 19.99, 2, "This Ones for You", 201 ),
    ("What You See Is What You Get", "2019-11-08", 19.99, 2, "What You See Is What You Get", 201 ),
    ("Growin' Up", "2022-06-24", 12.99, 2, "Growin' Up", 201 ),
    # Error entry
    ("Growin' Up123", "2022-00-24", 12.99, 2, "Growin Up", 201 ),
    ("Gettin Old", "2023-03-24", 12.99, 2, "Gettin Old", 201 ),
    ("Van Halen", "1978-02-10", 9.99, 3, "Van Halen", 201 ),
    ("Van Halen II", "1979-03-23", 8.99, 3, "Van Halen II", 201 ),
    ("Women and Children First", "1980-03-26", 10.99, 3, "Women and Children First", 201 ),
    ("Fair Warning", "1982-04-29", 12.99, 3, "Fair Warning", 201 ),
    ("Children of the Future", "1968-06-01", 7.99, 4, "Children of the Future", 201 ),
    ("Sailor", "1969-01-01", 12.99, 4, "Sailor", 201 ),
    ("Brave New World", "1970-01-01", 12.99, 4, "Brave New World", 201 ),
    ("Rock Love", "1971-01-01", 11.99, 4, "Rock Love", 201 ),
    ("Under the Table and Dreaming", "1994-01-01", 12.99, 5, "Under the Table and Dreaming", 201 ),
    ("Crash", "1996-01-01", 13.99, 5, "Crash", 201 ),
    ("Before These Crowded Streets", "1998-01-01", 14.99, 5, "Before These Crowded Streets", 201 ),
    ("Stand Up", "2005-01-01", 14.99, 5, "Stand Up", 201 ),
    # Error entry
    ("Stand Up123", "005-01-01", 14.99, 5, "Stand Up", 201 ),
    ("Love Like Crazy", "2010-01-01", 13.99, 6, "Love Like Crazy", 201 ),
    ("Hard 2 Love", "2012-01-01", 13.99, 6, "Hard 2 Love", 201 ),
    ("Lee Brice", "2017-01-01", 15.99, 6, "Lee Brice", 201 ),
    ("Hey World", "2020-01-01", 14.99, 6, "Hey World", 201 )

])
def test_create_album(client, album_name, release_date, price, artist_id, expected, status_code):
    res = client.post(f"/artist/{artist_id}/album", json={"name": album_name, "release_date": release_date, "price": price, "artist_id": artist_id})
    new_album = schemas.Album(**res.json())
    # assert new_album.name == expected
    assert res.status_code == status_code     