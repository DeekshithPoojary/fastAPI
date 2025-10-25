from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try: 
        yield db
    finally:
        db.close()


'''
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database = 'fastAPI', user = 'postgres', password = 'deekshithpoojary', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!!!")
        break
    except Exception as error:
        print("Connecting to database is failed....")
        print("Error: ", error)
        time.sleep(2)
'''