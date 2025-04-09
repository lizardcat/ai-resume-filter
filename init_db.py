# init_db.py
from db import engine
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created.")
