"""
database.py

This file sets up the connection to the PostgreSQL database using SQLModel.
It creates the database engine and provides helper functions to get a
database session that can be used inside route functions, services, and
NiceGUI pages.
"""

import os

from sqlmodel import SQLModel, create_engine, Session

# ---------------------------------------------------------------------------
# Database connection settings
# ---------------------------------------------------------------------------
# For a college project we keep this simple: read the connection details
# from environment variables if they exist, otherwise fall back to sensible
# local defaults. This means you do not NEED to set environment variables to
# run the project on your own machine, but you CAN override them if needed
# (for example, if your PostgreSQL password is different).
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "timetable_db")

# The full database URL used by SQLAlchemy/SQLModel to connect to Postgres.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = create_engine(DATABASE_URL, echo=False)

# The "engine" is the object SQLModel uses to talk to the database.
# echo=False keeps the console clean; set it to True if you want to see
# every SQL statement that gets executed (useful for learning/debugging).
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """
    Create all database tables based on the SQLModel models.
    This is called once when the application starts up.
    It will NOT recreate tables that already exist, so it is safe to call
    every time the app starts.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    A generator function that yields a new database session.
    FastAPI can use this as a dependency with `Depends(get_session)`.
    """
    with Session(engine) as session:
        yield session


def get_db_session() -> Session:
    """
    Convenience helper that returns a plain Session object (not a generator).
    This is used inside the NiceGUI UI code and inside route functions where
    a simple `with get_db_session() as session:` block is easier to read
    than a FastAPI dependency.
    """
    return Session(engine)
