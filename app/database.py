

'''
Here is the code for a standard connecion to a SLite database using SQLAlchemy.
    - SQLITE_DATABASE_URL: is the parameter to specify the type of DB, in this example it is SQLite 
                            and the name of the db is bay_music.db, located in the app directory

'''

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import event

SQLITE_DATABASE_URL = "sqlite:///./bay_music.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
Base =  declarative_base()
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

