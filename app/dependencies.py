from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core import config

# Create the database engine from the URL in the config
engine = create_engine(config.DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Dependency function that provides a database session to an API endpoint
    and ensures it's closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
