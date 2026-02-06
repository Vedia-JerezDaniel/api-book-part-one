from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.sql import text

import psycopg2 as pg
from urllib.parse import urlparse

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:root@localhost:5432/traveltech?options=-csearch_path%3Dtravel"
)
engine = create_engine(
    DATABASE_URL,
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



def get_connection():
    """Crea conexión directa con psycopg2."""
    try:
        # Parsear la URL de conexión
        parsed = urlparse(DATABASE_URL)
        
        conn = pg.connect(
            host=parsed.hostname or "localhost",
            port=parsed.port or 5432,
            database=parsed.path[1:] if parsed.path else "traveltech",  # Eliminar el '/' inicial
            user=parsed.username or "postgres",
            password=parsed.password or "root",
            options=f"-c search_path=travel"  # Establecer schema
        )
        
        print("✅ Conection granted with psycopg2")
        return conn
        
    except Exception as e:
        print(f"❌ Error conectando con psycopg2: {e}")
        raise