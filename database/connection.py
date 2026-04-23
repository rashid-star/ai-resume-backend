import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Free-hosting friendly default: use a local SQLite file if DATABASE_URL
    # isn't provided (e.g., Render free tier without managed DB).
    DATABASE_URL = "sqlite:///./app.db"

engine_kwargs = {"pool_pre_ping": True}

# SQLite needs a special flag for multi-threaded FastAPI usage.
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()