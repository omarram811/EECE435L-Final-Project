"""
Database Initialization Module.

This module configures the SQLite database engine and provides a session factory
for database interactions.

Attributes:
    DATABASE_URL (str): The URL for connecting to the SQLite database.
    engine (Engine): The SQLAlchemy engine for managing connections to the database.
    SessionLocal (sessionmaker): A session factory for creating database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///ecommerce.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
