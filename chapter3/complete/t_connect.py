from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.sql import text
import psycopg2

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:root@localhost:5432/traveltech?options=-csearch_path%3Dtravel"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,                    # Connection pool size
    max_overflow=30,                 # Max overflow connections
    pool_pre_ping=True,              # Verify connections before using
    echo=False,                      # Set to True for SQL debugging
    echo_pool=False,                 # Log connection pool events
    future=True                      # Use SQLAlchemy 2.0 style
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Better control over object expiration
)

Base = declarative_base()