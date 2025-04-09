# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite DB location
DATABASE_URL = "sqlite:///reviews.db"

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
