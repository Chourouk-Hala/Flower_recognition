from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = './database.db'  # Update with your database URL

def get_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()
